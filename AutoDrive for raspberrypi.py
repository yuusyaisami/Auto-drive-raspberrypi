import gui
import pygame as pg
import driver as dr
import variables as vr
import numpy as np
import pygame.mouse as ms
import socket
import Mineswepper

import time
import random
import item 
from picarx import Picarx
from time import sleep
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import keyboard
class socketclass:
    def __init__(self):
        IPADDR = "10.0.16.70"
        PORT = 5555
        # ソケット作成
        self.sock = socket.socket(socket.AF_INET)
        # サーバーへ接続
        self.sock.connect((IPADDR, PORT))
sockets = socketclass()
pg.init()
np.map = [ [99,99,99,99,99,99, 99,99, 99],
        [99, 0, 0, 0, 0, 0,  0, 0, 99],
        [99, 0,99, 0,99, 0, 99, 0, 99],
        [99, 0, 0, 0, 0, 0,  0, 0, 99],
        [99, 0,99, 0,99, 0, 99, 0, 99],
        [99, 0, 0, 0, 0, 0, 0 , 0, 99],
        [99, 0,99, 0,99, 0, 99, 0, 99],
        [99, 0, 0, 0, 0, 0, 0 , 0, 99],
        [99,99,99,99,99,99, 99,99, 99]]
var = vr.Variables() # 初期値
driver = dr.Driver(1,4,0,np.map) # 走行車関係の変数
shorter = dr.MazeShortest() # 最短距離の計算クラス

kernel_5 = np.ones((5,5),np.uint8)
px = Picarx()
px.set_grayscale_reference(1400)
color_dict = {'red':[0,4],'orange':[5,18],'yellow':[22,37],'green':[42,85],'blue':[92,110],'purple':[115,165],'red_2':[165,180]}

pg.display.set_caption("drivers")
# ウィンドウのアイコンを設定
icon_image = pg.image.load("icon.png")  # アイコンとして使用する画像をロード
pg.display.set_icon(icon_image)

class Car:
    # ルール
    # initialは開始するとき、Trueにして、処理を停止させるときはinitialでない同じ名前の変数をFalseにしてください
    def __init__(self, angle, speed):
        self.angle = angle
        self.speed = speed
        self.black_reflectance = 50
        self.initial_Determined = False # Carの処理を開始するときはこの変数をTrueにする
        self.Determined = False # Carの処理を停止するときはこの変数をFalseにする
        
        self.turned_direction = 0

        self.linetrace = True # ライントレースをするか
        self.backtime = 0
        self.car_direction = 0 # ライントレーサーのTuning処理時に使用する
        
        self.Tuning_start_time = 2
        self.Tuning_start_count = 0
        
        self.do_Tuning = True # コースアウト時チューニング処理を挟むか
        self.Tuning = False 
        self.TuningCount = 0
        
        self.curve = False 
        self.initial_curve = False
        self.curve_count = 0 # ハンドリング時の微調整

        self.aftertreatment = False # コーナー後のちょっとした前進
        self.aftercount = 0
        
        self.back = False
        self.backcount = 0
        
        px.set_camera_servo2_angle(-50)
        px.set_camera_servo1_angle(10)
    def color_detect(self, img,color_name):
        red_x = []
        red_y = []
        # 青色域は照明条件によって異なり、フレキシブルに調整できる。 H：彩度、S：彩度 v：明度
        resize_img = cv2.resize(img, (160,120), interpolation=cv2.INTER_LINEAR)  # 計算量を減らすため、画像のサイズを(160,120)に縮小している。
        hsv = cv2.cvtColor(resize_img, cv2.COLOR_BGR2HSV)              # BGRからHSVへの変換
        color_type = color_name

        mask = cv2.inRange(hsv,np.array([min(color_dict[color_type]), 60, 60]), np.array([max(color_dict[color_type]), 255, 255]) ) # inRange()：下/上の間を白、それ以外を黒にする
        if color_type == 'red':
                mask_2 = cv2.inRange(hsv, (color_dict['red_2'][0],0,0), (color_dict['red_2'][1],255,255)) 
                mask = cv2.bitwise_or(mask, mask_2)

        morphologyEx_img = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel_5,iterations=1) #画像に対してオープン操作を行う

        # morphologyEx_imgで輪郭を検索し、面積の小さいものから大きいものまで輪郭を並べる。
        _tuple = cv2.findContours(morphologyEx_img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)      
        # opencv3.x および openc4.x と互換性がある。
        if len(_tuple) == 3:
            _, contours, hierarchy = _tuple
        else:
            contours, hierarchy = _tuple

        color_area_num = len(contours) # 輪郭の数を数える

        if color_area_num > 0: 
            for i in contours:    # すべての輪郭を縦断する
                x,y,w,h = cv2.boundingRect(i)      # 輪郭を左上隅の座標と認識オブジェクトの幅と高さに分解する。

                # 画像に矩形を描く（画像、左上隅座標、右下隅座標、色、線幅）
                if w >= 8 and h >= 8: # 画像は元のサイズの4分の1に縮小されるため、元の画像に長方形を描いてターゲットを囲もうとすると、x、y、w、hを4倍しなければならない。
                    x = x * 4
                    y = y * 4 
                    w = w * 4
                    h = h * 4
                    cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)  # 長方形の枠を描く
                    cv2.putText(img,color_type,(x,y), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),2)# キャラクターの説明を追加
                    red_x.append(x + ( w / 2 ))
                    red_y.append(y + ( h / 2 ))

        #      画像  色の数      色のx  色のy
        return img, len(red_x), red_x, red_y

    def update(self, direction, img):
        # イニシャライズ処理
        if self.initial_Determined:
            self.initial_Determined = False
            self.aftertreatment = False
            self.Determined = True
            self.backcount = 0
            # 前進のみの場合 赤テープの部分でコースアウト判定になるので、ライントレースはチューニング処理を入れないことにする
            if direction == 0:
                self.do_Tuning = False
                print("前進")
            print("イニシャライズメイン処理")
            self.turned_direction = 0
            
        # main処理
        if self.Determined:
            
            img,redflag,x,y =  self.color_detect(img,'red_2')
            cv2.imshow("color detect camera", img)
            self.LineTrace()
            self.LineTuning()
            # 前進でない場合
            if direction != 0:
                self.After()
            # 前進の時は後処理の前進時間を伸ばす
            else:
                self.After(10)
            self.Curve(direction)
            self.Back()
            for count in range(redflag):
                if y[count] > 160 and not self.curve and not self.aftertreatment and direction != 0 and not self.back:
                    self.back = True
                    self.backtime = y[count]
                if y[count] > 108 and not self.curve and not self.aftertreatment:
                    #前進以外は曲がる処理を必要とする
                    if direction != 0:
                        self.initial_curve = True
                    else:
                        print("detect red")
                        self.aftertreatment = True
        else:
            #処理命令が下されていない場合、数値を初期値にリセットする
            self.linetrace = True # ライントレースをするか

            self.car_direction = 0 # ライントレーサーのTuning処理時に使用する
            self.do_Tuning = True # コースアウト時チューニング処理を挟むか
            self.Tuning = False 
            self.TuningCount = 0

            self.curve = False 
            self.initial_curve = False
            self.curve_count = 0 # ハンドリング時の微調整

            self.aftertreatment = False # コーナー後のちょっとした前進
            self.aftercount = 0

    def Back(self):
        if self.back:
            px.set_dir_servo_angle(0)
            print("back")
            self.backcount += 25
            self.linetrace = False
            px.backward(self.speed)
            if self.backcount > self.backtime / 3:
                self.backcount = 0
                self.back = False
                self.initial_curve = True
                
    def LineTrace(self):
        # ライントレース
        if self.linetrace:
            reflectance = px.get_grayscale_data()
            print(reflectance)
            if reflectance[0] < self.black_reflectance and reflectance[1] < self.black_reflectance and reflectance[2] < self.black_reflectance and not self.Tuning:
                px.forward(self.speed)
                px.set_dir_servo_angle(0)
                self.car_direction = self.Tuning_start_count = 0
            elif reflectance[0] < self.black_reflectance and not self.Tuning:
                px.forward(self.speed)
                px.set_dir_servo_angle(-self.angle)
                self.car_direction = -1
                self.Tuning_start_count = 1
            elif reflectance[2] < self.black_reflectance and not self.Tuning:
                px.forward(self.speed)
                px.set_dir_servo_angle(self.angle)
                self.car_direction = self.Tuning_start_count = 1
            elif reflectance[0] > self.black_reflectance and reflectance[1] < self.black_reflectance and reflectance[2] > self.black_reflectance and not self.Tuning:
                px.forward(self.speed)
                px.set_dir_servo_angle(0)
                self.car_direction = 0
            elif not self.Tuning:
                print("tunig")
                if self.do_Tuning:
                    self.Tuning_start_count += 1
                    if self.Tuning_start_count > self.Tuning_start_time:
                        #ラインから外れた tuning処理
                        self.Tuning = True
                        self.linetrace = False
                        self.Tuning_start_count = 0
                        print("Tuning start")
    def LineTuning(self):
        if self.Tuning:
            on_line = False
            px.forward(self.speed)
            if self.car_direction == -1:
                px.set_dir_servo_angle(-self.angle - 16)
            if self.car_direction == 1:
                px.set_dir_servo_angle(self.angle + 16)
            reflectance = px.get_grayscale_data()
            if reflectance[0] < self.black_reflectance or reflectance[1] < self.black_reflectance or reflectance[2] < self.black_reflectance:
                self.TuningCount += 1
                on_line = True
            # ラインに復帰する
            if self.TuningCount > 2 or on_line:
                if self.car_direction == -1:
                    px.set_dir_servo_angle(self.angle - 5)
                elif self.car_direction == 1:
                    px.set_dir_servo_angle(-self.angle + 5)
                else:
                    if self.turned_direction == -1:
                        px.set_dir_servo_angle(self.angle - 5)
                    elif self.turned_direction == 1:
                        px.set_dir_servo_angle(-self.angle + 5)
                # 初期値に戻す
                print("Tuning Stop")
                self.Tuning = False
                self.linetrace = True
                self.TuningCount = 0
        
        
    def Curve(self, direction):
        #コーナーカーブ 初回
        if self.initial_curve and not self.Tuning:
            if  direction == -1:
                px.forward(self.speed)
                px.set_dir_servo_angle(-self.angle - 20)
                self.car_direction = -1
            if direction == 1:
                px.forward(self.speed)
                px.set_dir_servo_angle(self.angle + 20)
                self.car_direction = 1
            self.curve = True
            self.initial_curve = not self.initial_curve
            self.do_Tuning = False
            self.linetrace = False
            self.curve_count = 0
            print("Curve start")
            self.turned_direction = direction
        # コーナー処理
        if self.curve:
            reflectance = px.get_grayscale_data()
            self.curve_count += 1
            # ラインに乗ったかつ、初回時から50countした
            if (reflectance[0] < self.black_reflectance or reflectance[1] < self.black_reflectance or reflectance[2] < self.black_reflectance) and self.curve_count > 8:
                self.curve = False
                self.aftertreatment = True
                self.linetrace = True
                self.do_Tuning = True
                self.aftercount = 0
                print("Curve stop")
    def After(self, n = 5):
        if self.aftertreatment:
            self.aftercount += 1
            if self.aftercount > n:
                if not self.Tuning:
                    self.Determined = False
                    px.stop()
                    self.aftercount = 0
                    print("After stop")
                else:
                    self.aftercount = 4
# 信号のクラス
class Traffic:
    def __init__(self, rect, w,h, greentime, redtime, direction, map_x, map_y, count = 0):
        self.rect = rect
        self.dx = rect.x
        self.dy = rect.y
        self.dw = w
        self.dh = h
        self.greentime = greentime
        self.redtime = redtime
        self.color = pg.Color('green')
        self.statue = 0
        self.traffic_direction = direction
        self.count = count
        self.map_x = map_x
        self.map_y = map_y
        self.visible = True
    def update(self):
        if self.visible:
            self.count = self.count + 1
            if self.count == self.greentime + self.redtime: # 緑
                self.statue = 0
                self.count = 0 # リセット
                self.color = pg.Color('green')
            elif self.count == self.greentime: # 赤
                self.statue = 1
                self.color = pg.Color('red')
    def draw(self, screen):
        if self.visible:
            # 信号の設置向きによって、座標を変える
            if self.traffic_direction == 0:
                self.rect.y = self.dy - (self.rect.h / 2)
                self.rect.x = self.dx + ((self.dw / 2) - self.rect.w / 2)
            elif self.traffic_direction == 1:
                self.rect.x = self.dx + self.dw - (self.rect.w / 2)
                self.rect.y = self.dy + ((self.dh / 2) - self.rect.h / 2)
            elif self.traffic_direction == 2:
                self.rect.y = self.dy - (self.rect.h / 2) + self.dh
                self.rect.x = self.dx + ((self.dw / 2) - self.rect.w / 2)
            elif self.traffic_direction == 3:
                self.rect.y = self.dy + ((self.dh / 2) - self.rect.h / 2)
                self.rect.x = self.dx - (self.rect.w / 2)
        pg.draw.rect(screen, self.color, self.rect, 0)
    def send(self, sock, command, x, y, direction, stute):
        x = str(x)
        y = str(y)
        direction = str(direction)
        stute = str(stute)
        sock.send(("type:" + command + ",x:" + str(x) + ",y:" + str(y) + ",direction:" + str(direction) + ",stute:" + str(stute)).encode("utf-8"))
# 自動走行のクラス
class DriverMap:
    def __init__(self):
        self.init_run = False
        self.run = False
        self.simulation_count = 0
        self.car = Car(10,10)
        self.direction = 0
    def handle_event(self, event):
        pass
    def update(self):
        if main_scene.menu_file.clicked_index != -1:
            pass
        if main_scene.menu_edit.clicked_index != -1:
            pass
        #--------------------------------------------------自動走行処理--------------------------------------------------
        if main_scene.run_button.clicked:
            self.init_run = True
        if self.init_run:
            driver.map = shorter.ResetMaze(driver.map) # マップを初期に戻す
            driver.map = shorter.MazeWaterValue(driver.map, driver) # プライオリティーインデックスを振り分ける
            driver.map[driver.goal_y][driver.goal_x] = 98 # ゴール地点を座標に入れる
            driver.map, error = shorter.MazeShortestRoute(driver.map, driver) # マップの最適ルートを検索する
            if error == 1:
                print("error : 目的地に到達できません")
                self.init_run = False
                return
            # エラーなし
            self.run = True
            self.init_run = False
            self.simulation_count = 0
        # 走行RUN
        if self.run:
            if not driver.traffic_stop() and not self.car.Determined:
                driver.map, driver.x, driver.y, self.direction, driver.direction = shorter.DriverDirection(driver.map, driver) # 次の移動先とその方向
                # 移動が終わったら実行する
                if self.direction == -2:
                    driver.map = shorter.ResetMaze(driver.map)
                    driver.map[driver.y][driver.x] = 1 # 自身の位置
                    self.run = False # 処理終了
                else:
                    self.car.initial_Determined = True
            self.car.update(self.direction,driver.img)
    
    def draw(self, screen):
        pass
class Maps:
    def __init__(self, rect, size, width):
        self.rect = rect
        self.size = size
        self.width = width
        self.mapbox = []
        self.row = []
        self.mouse_position_x_y = [0,0, 0, 0]
        self.rightbar_back = False
        self.visible = True

        for y in range(driver.map_y): # MapBoxをマップのサイズ分作成する
            for x in range(driver.map_x):
                self.row.append(DriverMapBox(pg.Rect(self.rect.x + x * size,self.rect.y + y * size, self.width, self.width),x,y))
            self.mapbox.append(self.row)
            self.row = []
        pass
    def handle_event(self, event):
        if self.visible:
            for y in range(len(self.mapbox)):
                for x in range(len(self.mapbox[0])):
                    self.mapbox[y][x].handle_event(event)


    def update(self):
        if self.visible:
            if main_scene.createflag:  # MapBoxを再作成
                self.mapbox = []
                self.row = []
                try: # 目的地をマップに追加
                    driver.map[driver.goal_y][driver.goal_x] = 90
                except: # 目的地がマップ外になったら
                    driver.map[1][2] = 90
                    driver.goal_y = 1
                    driver.goal_x = 2
                    print("ゴール地点が範囲")
                try:
                    driver.map[driver.y][driver.x] = 1
                except:
                    driver.map[2][1] = 1
                    driver.goal_y = 2
                    driver.goal_x = 1
                    print("スタート地点が範囲")
                for y in range(driver.map_y): # MapBoxをマップのサイズ分作成する
                    for x in range(driver.map_x):
                        self.row.append(DriverMapBox(pg.Rect(self.rect.x + x * self.size,self.rect.y + y * self.size, self.width, self.width),x,y))
                    self.mapbox.append(self.row)
                    self.row = []
            #選択されたボックスの更新がなければ、-1(選択なし)
            for y in range(len(self.mapbox)):
                for x in range(len(self.mapbox[0])):
                    self.mapbox[y][x].update()
    def exist_rightclick(self):
        for y in range(len(self.mapbox)):
            for x in range(len(self.mapbox[0])):
                if self.mapbox[y][x].rightclicked and self.mapbox[y][x].selectme:
                    return True
        return False
    def draw(self, screen):
        if self.visible:
            self.rightbar_back = False
            rightbar = False
            tx = -1
            ty = -1
            for y in range(len(self.mapbox)):
                for x in range(len(self.mapbox[0])):
                    self.mapbox[y][x].draw(screen)
                    if self.mapbox[y][x].x == driver.rightclick_x and self.mapbox[y][x].y == driver.rightclick_y: # 右クリックしたボックス
                        rightbar = True # 右クリックされた
                        tx = x # 右クリックされた、ボックスのインデックスを代入
                        ty = y
            for traffic in driver.traffic:
                    traffic.draw(screen)
            if self.rightbar_back:
                gui.tetragon(pg.Rect(self.mouse_position_x_y[0],self.mouse_position_x_y[1],140,len(self.mapbox[self.mouse_position_x_y[3]][self.mouse_position_x_y[2]].rightbar.elements) * self.mapbox[self.mouse_position_x_y[3]][self.mouse_position_x_y[2]].rightbar.size),var.COLOR_BACK,0,10,screen)
                self.mapbox[self.mouse_position_x_y[3]][self.mouse_position_x_y[2]].rightbar.draw(screen)
            if rightbar:
                if not(tx == -1 and ty == -1):
                    #pg.draw.rect(screen, var.COLOR_INACTIVE, self.mapbox[ty][tx].cube, 0)
                    self.mapbox[ty][tx].rightbar.draw(screen)



class DriverMapBox:
    def __init__(self,rect, x, y, width = 1):
        self.rect = rect
        self.x = x
        self.y = y
        self.cube = rect
        self.width = width
        self.color = var.COLOR_INACTIVE
        #self.color_wall = var.COLOR_INACTIVE
        #self.color_road = var.COLOR_INACTIVE
        #self.color_goal = var.COLOR_GOAL
        #self.color_start = var.COLOR_START
        #self.color_select = var.COLOR_SELECT
        #self.color_track = var.COLOR_TRACK
        #self.color_next = var.COLOR_NEXT
        self.selectme = False
        self.rightclicked = False
        self.release_count = 0
        self.release_flag = False
        self.rightbar = gui.RowText(pg.Rect(0,0,0,0),["1"],var.FONT,False)

        self.visible = True
    def handle_event(self, event):
        if self.visible:
            x, y = ms.get_pos()
            self.rightbar.handle_event(event)
            self.rightbar.update()
            #-----------------右クリックバー----------------
            if self.rightbar.clicked_index != -1:
                if self.rightbar.clicked_name == "road":
                    driver.map[self.y][self.x] = 0
                elif self.rightbar.clicked_name == "wall":
                    driver.map[self.y][self.x] = 99
                elif self.rightbar.clicked_name == "goal":
                    startx, starty = driver.search_map_value(98)
                    if startx != -1:
                        driver.map[starty][startx] = 0

                    driver.goal_x = self.x
                    driver.goal_y = self.y
                    driver.map[self.y][self.x] = 98
                elif self.rightbar.clicked_name == "start":
                    startx, starty = driver.search_map_value(1)
                    if startx != -1:
                        driver.map[starty][startx] = 0

                    driver.x = self.x
                    driver.y = self.y
                    driver.map[self.y][self.x] = 1
                elif self.rightbar.clicked_name == "cross traffic":
                    driver.traffic.append(Traffic(pg.Rect(self.rect.x,self.rect.y,var.TRAFFIC_SIZE, var.TRAFFIC_SIZE),self.rect.w,self.rect.h,60,60,0,self.x,self.y))
                    driver.traffic.append(Traffic(pg.Rect(self.rect.x,self.rect.y,var.TRAFFIC_SIZE, var.TRAFFIC_SIZE),self.rect.w,self.rect.h,60,60,2,self.x,self.y))
                    driver.traffic.append(Traffic(pg.Rect(self.rect.x,self.rect.y,var.TRAFFIC_SIZE, var.TRAFFIC_SIZE),self.rect.w,self.rect.h,60,60,1,self.x,self.y ,60))
                    driver.traffic.append(Traffic(pg.Rect(self.rect.x,self.rect.y,var.TRAFFIC_SIZE, var.TRAFFIC_SIZE),self.rect.w,self.rect.h,60,60,3,self.x,self.y, 60))
                    
                elif self.rightbar.clicked_name == "over traffic":
                    driver.traffic.append(Traffic(pg.Rect(self.rect.x,self.rect.y,var.TRAFFIC_SIZE, var.TRAFFIC_SIZE),self.rect.w,self.rect.h,60,60,0,self.x,self.y))
                    driver.traffic.append(Traffic(pg.Rect(self.rect.x,self.rect.y,var.TRAFFIC_SIZE, var.TRAFFIC_SIZE),self.rect.w,self.rect.h,60,60,2,self.x,self.y))
                elif self.rightbar.clicked_name == "delete traffic":
                    driver.trafic_delete(self.x,self.y)
            #------------おわり  右クリックバー------------
            if event.type == pg.MOUSEBUTTONDOWN:
                # ユーザーがDriverMapBoxをクリックしたとき
                if self.rect.collidepoint(event.pos):
                    if event.button == 1: # 左クリック
                        if driver.rightclick_x == -1:
                            driver.select_box_x = self.x
                            driver.select_box_y = self.y
                        driver.rightclick_x = driver.rightclick_y = -1
                    elif event.button == 3: # 右クリック
                        driver.rightclick_x = self.x
                        driver.rightclick_y = self.y
                        driver.select_box_x = self.x
                        driver.select_box_y = self.y
                        self.rightbar = gui.RowText(pg.Rect(x + 5,y - 5,140,32), ["road", "wall", "goal", "start", "cross traffic", "over traffic", "delete traffic"], var.FONT_SMALL,True,False,30,140,var.COLOR_INACTIVE,var.COLOR_ACTIVE,var.COLOR_ACTIVE,True,False )
                        if self.rightbar.rect.y + self.rightbar.size * len(self.rightbar.elements) > var.WINDOWNSIZE_Y:
                            y = var.WINDOWNSIZE_Y - self.rightbar.size * len(self.rightbar.elements)
                            self.rightbar = gui.RowText(pg.Rect(x + 5,y - 5,140,32), ["road", "wall", "goal", "start", "cross traffic", "over traffic", "delete traffic"], var.FONT_SMALL,True,False,30,140,var.COLOR_INACTIVE,var.COLOR_ACTIVE,var.COLOR_ACTIVE,True,False )
                elif driver.select_box_x == self.x and driver.select_box_y == self.y and driver.rightclick_x == self.x and driver.rightclick_y == self.y:
                    driver.select_box_x = driver.select_box_y = driver.rightclick_x = driver.rightclick_y = -1
                    self.rightbar = gui.RowText(pg.Rect(0,0,0,0),["1"],var.FONT,False)
            if event.type == pg.KEYDOWN and driver.select_box_x == self.x and driver.select_box_y == self.y:
                keys = pg.key.get_pressed()
                if keys[pg.K_UP] and keys[pg.K_LCTRL] and keys[pg.K_x]:
                    index = driver.search_traffic(self.map_x, self.map_y, 0, True)
                    try:
                        del driver.traffic[index] 
                    except:
                        print("選択されてない")
                if keys[pg.K_RIGHT] and keys[pg.K_LCTRL] and keys[pg.K_x]:
                    index = driver.search_traffic(self.map_x, self.map_y, 1, True)
                    try:
                        del driver.traffic[index] 
                    except:
                        print("選択されてない")
                if keys[pg.K_DOWN] and keys[pg.K_LCTRL] and keys[pg.K_x]:
                    index = driver.search_traffic(self.map_x, self.map_y, 2, True)
                    try:
                        del driver.traffic[index] 
                    except:
                        print("選択されてない")
                if keys[pg.K_LEFT] and keys[pg.K_LCTRL] and keys[pg.K_x]:
                    index = driver.search_traffic(self.map_x, self.map_y, 3, True)
                    try:
                        del driver.traffic[index] 
                    except:
                        print("選択されてない")
                elif keys[pg.K_UP] and keys[pg.K_c]:
                    driver.traffic.append(Traffic(pg.Rect(self.rect.x,self.rect.y,var.TRAFFIC_SIZE, var.TRAFFIC_SIZE),self.rect.w,self.rect.h,var.TRAFFIC_TIME,var.TRAFFIC_TIME,0,self.x, self.y))
                elif keys[pg.K_RIGHT] and keys[pg.K_c]:
                    driver.traffic.append(Traffic(pg.Rect(self.rect.x,self.rect.y,var.TRAFFIC_SIZE, var.TRAFFIC_SIZE),self.rect.w,self.rect.h,var.TRAFFIC_TIME,var.TRAFFIC_TIME,1,self.x, self.y))
                elif keys[pg.K_DOWN] and keys[pg.K_c]:
                    driver.traffic.append(Traffic(pg.Rect(self.rect.x,self.rect.y,var.TRAFFIC_SIZE, var.TRAFFIC_SIZE),self.rect.w,self.rect.h,var.TRAFFIC_TIME,var.TRAFFIC_TIME,2,self.x, self.y))
                elif keys[pg.K_LEFT] and keys[pg.K_c]:
                    driver.traffic.append(Traffic(pg.Rect(self.rect.x,self.rect.y,var.TRAFFIC_SIZE, var.TRAFFIC_SIZE),self.rect.w,self.rect.h,var.TRAFFIC_TIME,var.TRAFFIC_TIME,3,self.x, self.y))
                elif (keys[pg.K_UP] and keys[pg.K_v]) or (keys[pg.K_UP] and keys[pg.K_v]):
                    driver.traffic.append(Traffic(pg.Rect(self.rect.x,self.rect.y,var.TRAFFIC_SIZE, var.TRAFFIC_SIZE),self.rect.w,self.rect.h,var.TRAFFIC_TIME,var.TRAFFIC_TIME,0,self.x, self.y))
                    driver.traffic.append(Traffic(pg.Rect(self.rect.x,self.rect.y,var.TRAFFIC_SIZE, var.TRAFFIC_SIZE),self.rect.w,self.rect.h,var.TRAFFIC_TIME,var.TRAFFIC_TIME,2,self.x, self.y))
                elif (keys[pg.K_LEFT] and keys[pg.K_v]) or (keys[pg.K_RIGHT] and keys[pg.K_v]):
                    driver.traffic.append(Traffic(pg.Rect(self.rect.x,self.rect.y,var.TRAFFIC_SIZE, var.TRAFFIC_SIZE),self.rect.w,self.rect.h,var.TRAFFIC_TIME,var.TRAFFIC_TIME,1,self.x, self.y))
                    driver.traffic.append(Traffic(pg.Rect(self.rect.x,self.rect.y,var.TRAFFIC_SIZE, var.TRAFFIC_SIZE),self.rect.w,self.rect.h,var.TRAFFIC_TIME,var.TRAFFIC_TIME,3,self.x, self.y))
                elif keys[pg.K_t]:
                    driver.traffic.append(Traffic(pg.Rect(self.rect.x,self.rect.y,var.TRAFFIC_SIZE, var.TRAFFIC_SIZE),self.rect.w,self.rect.h,var.TRAFFIC_TIME,var.TRAFFIC_TIME,0,self.x, self.y,var.TRAFFIC_TIME))
                    driver.traffic.append(Traffic(pg.Rect(self.rect.x,self.rect.y,var.TRAFFIC_SIZE, var.TRAFFIC_SIZE),self.rect.w,self.rect.h,var.TRAFFIC_TIME,var.TRAFFIC_TIME,2,self.x, self.y,var.TRAFFIC_TIME))
                    driver.traffic.append(Traffic(pg.Rect(self.rect.x,self.rect.y,var.TRAFFIC_SIZE, var.TRAFFIC_SIZE),self.rect.w,self.rect.h,var.TRAFFIC_TIME,var.TRAFFIC_TIME,1,self.x, self.y))
                    driver.traffic.append(Traffic(pg.Rect(self.rect.x,self.rect.y,var.TRAFFIC_SIZE, var.TRAFFIC_SIZE),self.rect.w,self.rect.h,var.TRAFFIC_TIME,var.TRAFFIC_TIME,3,self.x, self.y))
                elif keys[pg.K_s]:
                    startx, starty = driver.search_map_value(1)
                    if startx != -1:
                        driver.map[starty][startx] = 0

                    driver.x = self.x
                    driver.y = self.y
                    driver.map[self.y][self.x] = 1
                elif keys[pg.K_w]:
                    driver.map[self.y][self.x] = 99
                elif keys[pg.K_r]:
                    driver.map[self.y][self.x] = 0
                elif keys[pg.K_g]:
                    startx, starty = driver.search_map_value(98)
                    if startx != -1:
                        driver.map[starty][startx] = 0

                    driver.goal_x = self.x
                    driver.goal_y = self.y
                    driver.map[self.y][self.x] = 98
    def update(self):
        if self.visible:
            if driver.map[self.y][self.x] == 99:
                self.color = var.COLOR_INACTIVE
                self.width = 0
            elif driver.map[self.y][self.x] == 0:
                self.color = var.COLOR_INACTIVE
                self.width = 2
            elif driver.map[self.y][self.x] == 1:
                self.color = var.COLOR_START
                self.width = 2
            elif driver.map[self.y][self.x] == 90:
                self.color = var.COLOR_NEXT
                self.width = 2
            elif driver.map[self.y][self.x] == 98:
                self.color = var.COLOR_GOAL
                self.width = 2
            elif driver.map[self.y][self.x] == 80:
                self.color = var.COLOR_TRACK
                self.width = 2
            if self.x == driver.rightclick_x and self.y == driver.rightclick_y:
                self.color = var.COLOR_SELECT
            if driver.select_box_x == self.x and driver.select_box_y == self.y:
                self.color = var.COLOR_SELECT

            

    def draw(self, screen):
        #テトラゴンは処理が重くなるからだめ
        # gui.tetragon(self.rect, self.color, self.width, 5, screen)
        pg.draw.rect(screen, self.color,self.rect, self.width)
        
        if driver.rightclick_x == self.x and driver.rightclick_y == self.y:
            pass
        else:
            self.rightbar = gui.RowText(pg.Rect(0,0,0,0),["1"],var.FONT,False)


# 大まかな処理のクラス
class MainScene:
    def __init__(self):
        self.createflag = False
        self.visible = True
        self.visible_handle_event_and_update = True
        self.createmap_flag = False
        self.createmap_range = [9,9]
        self.variable_view = VariableView(pg.Rect(var.WINDOWNSIZE_X - 180,60,0,0),False)
        # ダウンボックスのインスタンスを作成
        self.menu_file = gui.Menubar(pg.Rect(20,10,75,32),"file",["new create","save", "setting", "mineswepper","close Window"],var.FONT,True,False,32,170,var.COLOR_INACTIVE,var.COLOR_ACTIVE,var.COLOR_ACTIVE,True, True)
        self.menu_edit = gui.Menubar(pg.Rect(80,10,75,32),"edit",["road","wall", "start", "goal", "traffic add", "up/down traffic add", "right/left traffic add", "all traffic add", "traffic delete"],var.FONT,True,False,32,210,var.COLOR_INACTIVE,var.COLOR_ACTIVE,var.COLOR_ACTIVE,True, True)
        self.menu_view = gui.Menubar(pg.Rect(140,10,75,32),"view",["theme","variable view", "variable editer"],var.FONT,True,False,32,170,var.COLOR_INACTIVE,var.COLOR_ACTIVE,var.COLOR_ACTIVE,True, True)
        self.run_button = gui.Button(pg.Rect(var.WINDOWNSIZE_X - 100,10,75,32),"Run(F5)",var.FONT,True,var.COLOR_INACTIVE,var.COLOR_ACTIVE,var.COLOR_INACTIVE,True)
        self.menu_line = gui.Line(pg.Rect(0, 50,0,0),pg.Rect(1280,50,0,0),True,3)
        self.driver_map = DriverMap()
        self.maps = Maps(pg.Rect(20,100,var.BOXSIZE,var.BOXSIZE),var.BOXSPACE,var.BOXSIZE)
         # minigame mineswepperを追加
        self.mineswepper = Mineswepper.gamescene
        #self.mineswepper.d_x = self.maps.mapbox[0][0].rect.x
        #self.mineswepper.d_y = self.maps.mapbox[0][0].rect.y

        self.mineswepper.d_x = self.maps.mapbox[0][0].rect.y
        self.mineswepper.d_y = self.maps.mapbox[0][0].rect.x


        self.mineswepper.map_box_size_x = self.mineswepper.map_box_size_y = var.BOXSIZE
        self.mineswepper.map_box_space_x = self.mineswepper.map_box_space_y = var.BOXSPACE

        self.objects = [self.menu_line,self.menu_file,self.menu_edit,self.menu_view, self.run_button] 
    def handle_event(self, event):
        if self.visible and self.visible_handle_event_and_update:
            for object in self.objects:
                object.handle_event(event)
            self.mineswepper.handle_event(event)
            self.driver_map.handle_event(event)
            self.maps.handle_event(event)
            self.variable_view.handle_event(event)
    def update(self):
        if self.visible and self.visible_handle_event_and_update:
            for object in self.objects:
                object.update()
            self.driver_map.update()
            self.maps.update()
            self.createflag = False
            #---------menu bar  file----------
            if self.menu_file.clicked_index != -1:
                if self.menu_file.clicked_name == "new create":
                    main_scene.visible = False
                    setting_scene.visible = False
                    textbox_scene.visible = True
                    driver.screen = pg.display.set_mode((580, 380))
                elif main_scene.menu_file.clicked_name == "save":
                    var.save_box(driver.x, driver.y)
                elif main_scene.menu_file.clicked_name == "setting":
                    main_scene.visible = False
                    setting_scene.visible = True
                    textbox_scene.visible = False
                    driver.screen = pg.display.set_mode((720, 480))
                elif main_scene.menu_file.clicked_name == "mineswepper":
                    self.mineswepper.map_box_size_x = self.mineswepper.map_box_size_y = var.BOXSIZE
                    self.mineswepper.map_box_space_x = self.mineswepper.map_box_space_y = var.BOXSPACE
                    self.mineswepper.map_size_x = driver.map_x
                    self.mineswepper.map_size_y = driver.map_y
                    self.maps.visible = not self.maps.visible
                    if self.maps.visible:
                        self.mineswepper.game_over()
                        self.mineswepper.isStart = False
                        self.mineswepper.inProgress = False
                        self.mineswepper.isFirstClick = False
                        self.mineswepper.isGameOver = False
                    else:
                        self.mineswepper.game_over()
                elif main_scene.menu_file.clicked_name == "close Window":
                    driver.done = True
            #---------menu bar  edit----------
            if self.menu_edit.clicked_index != -1:
                if self.menu_edit.clicked_name == "road":
                    try:
                        driver.map[driver.select_box_y][driver.select_box_x] = 0
                    except:
                        print("map box選択されていません")
                if self.menu_edit.clicked_name == "wall":
                    try:
                        driver.map[driver.select_box_y][driver.select_box_x] = 99
                    except:
                        print("map box選択されていないまたは、範囲外")
                if self.menu_edit.clicked_name == "start":
                    try:
                        driver.map[driver.select_box_y][driver.select_box_x] = 1
                        driver.x = driver.select_box_x
                        driver.y = driver.select_box_y
                    except:
                        print("map box選択されていないまたは、範囲外")
                if self.menu_edit.clicked_name == "goal":
                    try:
                        driver.map[driver.select_box_y][driver.select_box_x] = 90
                        driver.goal_x = driver.select_box_x
                        driver.goal_y = driver.select_box_y
                    except:
                        print("map box選択されていないまたは、範囲外")
                if self.menu_edit.clicked_name == "traffic add":
                    try:
                        driver.traffic.append(Traffic(pg.Rect(main_scene.maps.mapbox[driver.select_box_y][driver.select_box_x].rect.x,main_scene.maps.mapbox[driver.select_box_y][driver.select_box_x].rect.y,var.TRAFFIC_SIZE, var.TRAFFIC_SIZE),main_scene.maps.width,main_scene.maps.width,60,60,0,driver.select_box_x,driver.select_box_y))
                    except:
                        print("map box選択されていないまたは、範囲外")
            #-----------menu bar  view-----------
            if self.menu_view.clicked_index != -1:
                if self.menu_view.clicked_name == "theme":
                    main_scene.visible = False
                    setting_scene.visible = True
                    textbox_scene.visible = False
                    driver.screen = pg.display.set_mode((720, 480))
                elif self.menu_view.clicked_name == "variable view":
                    self.variable_view.visible = not self.variable_view.visible
                elif self.menu_view.clicked_name == "variable editer":
                    setting_scene.visible_displays = True
                    setting_scene.visible_datas = False
                    setting_scene.visible_other = False
            #------------------------------------
            for traffic in driver.traffic:
                traffic.update()
            self.variable_view.update()
            self.mineswepper.update()
    def draw(self, screen):
        if self.visible:
            self.mineswepper.draw(screen)
            self.maps.draw(screen)
            
            for object in self.objects:
                object.draw(screen)
            
            self.variable_view.draw(screen)
            self.driver_map.draw(screen)
            
class TextBoxScene:
    def __init__(self):
        self.visible = False
        self.x = driver.map_x
        self.y = driver.map_y
        self.text_tutorial = gui.Text(pg.Rect(20,20,128,32),"Please enter the width and height of the map")
        self.text_x = gui.Text(pg.Rect(50,68,128,32),"X")
        self.text_y = gui.Text(pg.Rect(330,68,128,32),"Y")
        self.inputbox_x = gui.InputBox(pg.Rect(50,100,128,32), "",var.FONT, True, False)
        self.inputbox_y = gui.InputBox(pg.Rect(330,100,128,32), "",var.FONT, True, False)
        self.box_determined = gui.Button(pg.Rect(50,320,130,32),"determined",var.FONT, True,var.COLOR_INACTIVE,var.COLOR_ACTIVE,var.COLOR_ACTIVE,False)
        self.box_cancel = gui.Button(pg.Rect(200,320,80,32),"cancel",var.FONT, True,var.COLOR_INACTIVE,var.COLOR_ACTIVE,var.COLOR_ACTIVE,False)
        self.objects = [self.inputbox_x, self.inputbox_y, self.box_determined, self.box_cancel, self.text_x, self.text_y,self.text_tutorial]
    def handle_event(self, event):
        if self.visible:
            for object in self.objects:
                object.handle_event(event)
    def update(self):
        if self.visible:
            for object in self.objects:
                object.update()
            if self.inputbox_x.clicked:
                try:
                    value = int(self.inputbox_x.clicked_text)
                    self.text_x.text = "X : " + self.inputbox_x.clicked_text
                    self.x = value
                except:
                    print("数値を入力してください")
            if self.inputbox_y.clicked:
                try:
                    value = int(self.inputbox_y.clicked_text)
                    self.text_y.text = "Y : " + self.inputbox_y.clicked_text
                    self.y = value
                except:
                    print("数値を入力してください")
            if self.box_determined.clicked:
                driver.map_x = self.x
                driver.map_y = self.y
                main_scene.visible = True
                self.visible = False
                driver.create_map()
                driver.screen = None
                main_scene.createflag = True
                driver.screen = pg.display.set_mode((var.WINDOWNSIZE_X, var.WINDOWNSIZE_Y))
            if self.box_cancel.clicked:
                main_scene.visible = True
                self.visible = False
                driver.screen = pg.display.set_mode((var.WINDOWNSIZE_X, var.WINDOWNSIZE_Y))
    def draw(self, screen):
        if self.visible:
            for object in self.objects:
                object.draw(screen)
class VariableView:
    def __init__(self, rect, visible):
        self.rect = rect
        self.visible = visible
        self.texts = gui.Texts(pg.Rect(self.rect.x, self.rect.y, 12,12), ["map size : ", "car x : ", "car y : ", "car direction : ", "selectbox x : ", "selectbox y : ", "rightclick x : ", "rightclick y : "], var.FONT_SMALL, var.COLOR_INACTIVE,True,8,24)
        self.text_direction = gui.Text(pg.Rect(self.rect.x, self.rect.y + 24 * 8, 32,32), "direction x", var.FONT_SMALL, True, var.COLOR_INACTIVE)
        self.inputbox_direction = gui.InputBox(pg.Rect(self.rect.x, self.rect.y + 24 * 9 - 2, 128,32), "", var.FONT, True, True, var.COLOR_INACTIVE,var.COLOR_ACTIVE, var.COLOR_INACTIVE)
        
    def handle_event(self, event):
        self.inputbox_direction.handle_event(event)
    def update(self):
        if self.visible:
            self.texts.texts[0].text = "map size : " + str(driver.map_x)
            self.texts.texts[1].text = "car x : " + str(driver.x)
            self.texts.texts[2].text = "car y : " + str(driver.y)
            self.texts.texts[3].text = "car direction : " + str(driver.direction)
            self.texts.texts[4].text = "selectbox x : " + str(driver.select_box_x)
            self.texts.texts[5].text = "selectbox y : " + str(driver.select_box_y)
            self.texts.texts[6].text = "rightclick x : " + str(driver.rightclick_x)
            self.texts.texts[7].text = "rightclick y : " + str(driver.rightclick_y)
            self.texts.update()
            if self.inputbox_direction.clicked_text != "":
                driver.direction = self.inputbox_direction.clicked_text
                self.inputbox_direction.clicked_text = ""
    def draw(self, screen):
        if self.visible:
            self.texts.draw(screen)
            self.inputbox_direction.draw(screen)
            self.text_direction.draw(screen)
            self.inputbox_direction.draw(screen)
            self.text_direction.draw(screen)

class SettingScene:
    def __init__(self):
        self.visible = False
        self.space = 15
        self.setting_tab = gui.ColumnText(pg.Rect(10,6,128,32),["display", "data", "other"],var.FONT,True,False,self.space,120,var.COLOR_INACTIVE,var.COLOR_INACTIVE,var.COLOR_INACTIVE,False,True)
        self.window_tab = gui.ColumnText(pg.Rect(492,6,128,32),["save", "close"],var.FONT,True,False,15,100,var.COLOR_INACTIVE,var.COLOR_ACTIVE,var.COLOR_ACTIVE,False,True)
        self.visible_always = True
        self.visible_displays = True
        self.visible_datas = False
        self.visible_other = False

        self.menu_line = gui.Line(pg.Rect(0, 38,0,0),pg.Rect(1280,38,0,0),True,3)
        self.display_line = gui.Line(pg.Rect(12, 38,0,0),pg.Rect(129,38,0,0),True,3,var.COLOR_BACK)
        self.data_line = gui.Line(pg.Rect(147, 38,0,0),pg.Rect(264,38,0,0),True,3,var.COLOR_BACK)
        self.other_line = gui.Line(pg.Rect(282, 38,0,0),pg.Rect(399,38,0,0),True,3,var.COLOR_BACK)

        #display
        self.boxsize_display = gui.InputBoxAndText(pg.Rect(10, 50, 100,32), "box size", var.FONT, var.COLOR_INACTIVE, var.COLOR_ACTIVE,True,False,pg.Rect(500,50,120,32),str(var.BOXSIZE))
        self.boxspace_display = gui.InputBoxAndText(pg.Rect(10, 85, 100,32), "box space", var.FONT, var.COLOR_INACTIVE, var.COLOR_ACTIVE,True,False,pg.Rect(500,85,120,32),str(var.BOXSPACE))
        self.switching_time_display = gui.InputBoxAndText(pg.Rect(10, 120, 100,32), "Signal switching time", var.FONT, var.COLOR_INACTIVE, var.COLOR_ACTIVE,True,False,pg.Rect(500,120,120,32),str(var.TRAFFIC_TIME))
        self.always = [self.menu_line]
        self.displays = [self.display_line, self.boxsize_display, self.boxspace_display, self.switching_time_display]
        self.datas = [self.data_line]
        self.other = [self.other_line]
    
    
    def handle_event(self, event):
        if self.visible:
            self.setting_tab.handle_event(event)
            self.window_tab.handle_event(event)

            if self.visible_always:
                for al in self.always:
                    al.handle_event(event)
            if self.visible_displays:
                for di in self.displays:
                    di.handle_event(event)
            if self.visible_datas:
                for da in self.datas:
                    da.handle_event(event)
            if self.visible_other:
                for ot in self.other:
                    ot.handle_event(event)
    def update(self):
        if self.visible:
            if self.setting_tab.clicked_index != -1:
                if self.setting_tab.clicked_name == "display":
                    self.visible_displays = True
                    self.visible_datas = False
                    self.visible_other = False
                if self.setting_tab.clicked_name == "data":
                    self.visible_displays = False
                    self.visible_datas = True
                    self.visible_other = False
                if self.setting_tab.clicked_name == "other":
                    self.visible_displays = False
                    self.visible_datas = False
                    self.visible_other = True
            if self.window_tab.clicked_index != -1:
                # セームボタンが押されたとき
                if self.window_tab.clicked_name == "save":
                    var.save_boxspace(self.boxspace_display.inputbox.text, main_scene, driver)
                    var.save_boxsize(self.boxsize_display.inputbox.text, main_scene, driver)
                    var.save_signal_switching_time(self.switching_time_display.inputbox.text)
                if self.window_tab.clicked_name == "close":
                    driver.screen = pg.display.set_mode((var.WINDOWNSIZE_X, var.WINDOWNSIZE_Y))
                    main_scene.visible = True
                    self.visible = False
            self.setting_tab.update()
            self.window_tab.update()
            #always 常に
            if self.visible_always:
                for al in self.always:
                    al.update()
            # display ディスプレイ
            if self.visible_displays:
                for di in self.displays:
                    di.update()
            
            # data データ
            if self.visible_datas:
                for da in self.datas:
                    da.update()
            # other ほかに
            if self.visible_other:
                for ot in self.other:
                    ot.update()
    def draw(self, screen ):
        if self.visible:
            self.setting_tab.draw(screen)
            self.window_tab.draw(screen)
            if self.visible_always:
                for al in self.always:
                    al.draw(screen)
            if self.visible_displays:
                for di in self.displays:
                    di.draw(screen)
            if self.visible_datas:
                for da in self.datas:
                    da.draw(screen)
            if self.visible_other:
                for ot in self.other:
                    ot.draw(screen)
main_scene = MainScene()   
textbox_scene = TextBoxScene()
setting_scene = SettingScene()
scene_list = [main_scene, textbox_scene, setting_scene]
# メイン処理関数   
def main():
    with PiCamera() as camera:
        camera.resolution = (528,480)
        camera.framerate = 24
        rawCapture = PiRGBArray(camera, size=camera.resolution)
        time.sleep(0.5)
        var.init_savedata(driver)
        clock = pg.time.Clock()
        for frame in camera.capture_continuous(rawCapture, format="bgr",use_video_port=True):
            if not driver.done:
                break
            driver.img = frame.array
            rawCapture.truncate(0)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    driver.done = False
                for sl in scene_list:
                    sl.handle_event(event)
            for sl in scene_list:
                sl.update()
            driver.screen.fill(var.COLOR_BACK)
            for sl in scene_list:
                sl.draw(driver.screen)
            pg.display.flip()
            clock.tick(30)
        cv2.destroyAllWindows()
        camera.close()  

if __name__ == '__main__':
    main()
    pg.quit()







# ラズベリーパイのみ必要
# kernel_5 = np.ones((5,5),np.uint8)
# px = Picarx()
# px.set_grayscale_reference(1400)
# color_dict = {'red':[0,4],'orange':[5,18],'yellow':[22,37],'green':[42,85],'blue':[92,110],'purple':[115,165],'red_2':[165,180]}

#class Car:
#    # ルール
#    # initialは開始するとき、Trueにして、処理を停止させるときはinitialでない同じ名前の変数をFalseにしてください
#    def __init__(self, angle, speed):
#        self.angle = angle
#        self.speed = speed
#        self.black_reflectance = 50
#        self.initial_Determined = False # Carの処理を開始するときはこの変数をTrueにする
#        self.Determined = False # Carの処理を停止するときはこの変数をFalseにする
#
#        self.linetrace = True # ライントレースをするか
#        self.backtime = 0
#        self.car_direction = 0 # ライントレーサーのTuning処理時に使用する
#        
#        self.Tuning_start_time = 2
#        self.Tuning_start_count = 0
#        
#        self.do_Tuning = True # コースアウト時チューニング処理を挟むか
#        self.Tuning = False 
#        self.TuningCount = 0
#        
#        self.curve = False 
#        self.initial_curve = False
#        self.curve_count = 0 # ハンドリング時の微調整
#
#        self.aftertreatment = False # コーナー後のちょっとした前進
#        self.aftercount = 0
#        
#        self.back = False
#        self.backcount = 0
#        
#        px.set_camera_servo2_angle(-50)
#        px.set_camera_servo1_angle(10)
#    def color_detect(self, img,color_name):
#        red_x = []
#        red_y = []
#        # 青色域は照明条件によって異なり、フレキシブルに調整できる。 H：彩度、S：彩度 v：明度
#        resize_img = cv2.resize(img, (160,120), interpolation=cv2.INTER_LINEAR)  # 計算量を減らすため、画像のサイズを(160,120)に縮小している。
#        hsv = cv2.cvtColor(resize_img, cv2.COLOR_BGR2HSV)              # BGRからHSVへの変換
#        color_type = color_name
#
#        mask = cv2.inRange(hsv,np.array([min(color_dict[color_type]), 60, 60]), np.array([max(color_dict[color_type]), 255, 255]) ) # inRange()：下/上の間を白、それ以外を黒にする
#        if color_type == 'red':
#                mask_2 = cv2.inRange(hsv, (color_dict['red_2'][0],0,0), (color_dict['red_2'][1],255,255)) 
#                mask = cv2.bitwise_or(mask, mask_2)
#
#        morphologyEx_img = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel_5,iterations=1) #画像に対してオープン操作を行う
#
#        # morphologyEx_imgで輪郭を検索し、面積の小さいものから大きいものまで輪郭を並べる。
#        _tuple = cv2.findContours(morphologyEx_img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)      
#        # opencv3.x および openc4.x と互換性がある。
#        if len(_tuple) == 3:
#            _, contours, hierarchy = _tuple
#        else:
#            contours, hierarchy = _tuple
#
#        color_area_num = len(contours) # 輪郭の数を数える
#
#        if color_area_num > 0: 
#            for i in contours:    # すべての輪郭を縦断する
#                x,y,w,h = cv2.boundingRect(i)      # 輪郭を左上隅の座標と認識オブジェクトの幅と高さに分解する。
#
#                # 画像に矩形を描く（画像、左上隅座標、右下隅座標、色、線幅）
#                if w >= 8 and h >= 8: # 画像は元のサイズの4分の1に縮小されるため、元の画像に長方形を描いてターゲットを囲もうとすると、x、y、w、hを4倍しなければならない。
#                    x = x * 4
#                    y = y * 4 
#                    w = w * 4
#                    h = h * 4
#                    cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)  # 長方形の枠を描く
#                    cv2.putText(img,color_type,(x,y), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),2)# キャラクターの説明を追加
#                    red_x.append(x + ( w / 2 ))
#                    red_y.append(y + ( h / 2 ))
#
#        #      画像  色の数      色のx  色のy
#        return img, len(red_x), red_x, red_y
#    
#
#    def update(self, direction, img):
#        # イニシャライズ処理
#        if self.initial_Determined:
#            self.initial_Determined = False
#            self.aftertreatment = False
#            self.Determined = True
#            self.backcount = 0
#            # 前進のみの場合 赤テープの部分でコースアウト判定になるので、ライントレースはチューニング処理を入れないことにする
#            if direction == 0:
#                self.do_Tuning = False
#                print("前進")
#            print("イニシャライズメイン処理")
#            
#        # main処理
#        if self.Determined:
#            
#            img,redflag,x,y =  self.color_detect(img,'red_2')
#            cv2.imshow("color detect camera", img)
#            self.LineTrace()
#            self.LineTuning()
#            # 前進でない場合
#            if direction != 0:
#                self.After()
#            # 前進の時は後処理の前進時間を伸ばす
#            else:
#                self.After(15)
#            self.Curve(direction)
#            self.Back()
#            for count in range(redflag):
#                if y[count] > 170 and not self.curve and not self.aftertreatment and direction != 0 and not self.back:
#                    self.back = True
#                    self.backtime = y[count]
#                if y[count] > 110 and not self.curve and not self.aftertreatment:
#                    #前進以外は曲がる処理を必要とする
#                    if direction != 0:
#                        self.initial_curve = True
#                    else:
#                        print("detect red")
#                        self.aftertreatment = True
#        else:
#            #処理命令が下されていない場合、数値を初期値にリセットする
#            self.linetrace = True # ライントレースをするか
#
#            self.car_direction = 0 # ライントレーサーのTuning処理時に使用する
#            self.do_Tuning = True # コースアウト時チューニング処理を挟むか
#            self.Tuning = False 
#            self.TuningCount = 0
#
#            self.curve = False 
#            self.initial_curve = False
#            self.curve_count = 0 # ハンドリング時の微調整
#
#            self.aftertreatment = False # コーナー後のちょっとした前進
#            self.aftercount = 0
#
#    def Back(self):
#        if self.back:
#            px.set_dir_servo_angle(0)
#            print("back")
#            self.backcount += 50
#            self.linetrace = False
#            px.backward(self.speed)
#            if self.backcount > self.backtime / 3:
#                self.backcount = 0
#                self.back = False
#                self.initial_curve = True
#                
#    def LineTrace(self):
#        # ライントレース
#        if self.linetrace:
#            reflectance = px.get_grayscale_data()
#            print(reflectance)
#            if reflectance[0] < self.black_reflectance and reflectance[1] < self.black_reflectance and reflectance[2] < self.black_reflectance and not self.Tuning:
#                px.forward(self.speed)
#                px.set_dir_servo_angle(0)
#                self.car_direction = self.Tuning_start_count = 0
#            elif reflectance[0] < self.black_reflectance and not self.Tuning:
#                px.forward(self.speed)
#                px.set_dir_servo_angle(-self.angle)
#                self.car_direction = -1
#                self.Tuning_start_count = 1
#            elif reflectance[2] < self.black_reflectance and not self.Tuning:
#                px.forward(self.speed)
#                px.set_dir_servo_angle(self.angle)
#                self.car_direction = self.Tuning_start_count = 1
#            elif reflectance[0] > self.black_reflectance and reflectance[1] < self.black_reflectance and reflectance[2] > self.black_reflectance and not self.Tuning:
#                px.forward(self.speed)
#                px.set_dir_servo_angle(0)
#                self.car_direction = 0
#            elif not self.Tuning:
#                print("tunig")
#                if self.do_Tuning:
#                    self.Tuning_start_count += 1
#                    if self.Tuning_start_count > self.Tuning_start_time:
#                        #ラインから外れた tuning処理
#                        self.Tuning = True
#                        self.linetrace = False
#                        self.Tuning_start_count = 0
#                        print("Tuning start")
#    def LineTuning(self):
#        if self.Tuning:
#            on_line = False
#            px.forward(self.speed)
#            if self.car_direction == -1:
#                px.set_dir_servo_angle(-self.angle - 20)
#            if self.car_direction == 1:
#                px.set_dir_servo_angle(self.angle + 20)
#            reflectance = px.get_grayscale_data()
#            if reflectance[0] < self.black_reflectance or reflectance[1] < self.black_reflectance or reflectance[2] < self.black_reflectance:
#                self.TuningCount += 1
#                on_line = True
#            # ラインに復帰する
#            if self.TuningCount > 2 or on_line:
#                if self.car_direction == -1:
#                    px.set_dir_servo_angle(self.angle - 5)
#                if self.car_direction == 1:
#                    px.set_dir_servo_angle(-self.angle + 5)
#                # 初期値に戻す
#                print("Tuning Stop")
#                self.Tuning = False
#                self.linetrace = True
#                self.TuningCount = 0
#        
#        
#    def Curve(self, direction):
#        #コーナーカーブ 初回
#        if self.initial_curve and not self.Tuning:
#            if  direction == -1:
#                px.forward(self.speed)
#                px.set_dir_servo_angle(-self.angle - 15)
#                self.car_direction = -1
#            if direction == 1:
#                px.forward(self.speed)
#                px.set_dir_servo_angle(self.angle + 15)
#                self.car_direction = 1
#            self.curve = True
#            self.initial_curve = not self.initial_curve
#            self.do_Tuning = False
#            self.linetrace = False
#            self.curve_count = 0
#            print("Curve start")
#        # コーナー処理
#        if self.curve:
#            reflectance = px.get_grayscale_data()
#            self.curve_count += 1
#            # ラインに乗ったかつ、初回時から50countした
#            if (reflectance[0] < self.black_reflectance or reflectance[1] < self.black_reflectance or reflectance[2] < self.black_reflectance) and self.curve_count > 5:
#                self.curve = False
#                self.aftertreatment = True
#                self.linetrace = True
#                self.do_Tuning = True
#                self.aftercount = 0
#                print("Curve stop")
#    def After(self, n = 5):
#        if self.aftertreatment:
#            self.aftercount += 1
#            if self.aftercount > n:
#                if not self.Tuning:
#                    self.Determined = False
#                    px.stop()
#                    print("After stop")
#                else:
#                    self.aftercount = 4
#
#
#class Traffic:
#    def __init__(self, rect, w,h, greentime, redtime, direction, map_x, map_y, count = 0):
#        self.rect = rect
#        self.dx = rect.x
#        self.dy = rect.y
#        self.dw = w
#        self.dh = h
#        self.greentime = greentime
#        self.redtime = redtime
#        self.color = pg.Color('green')
#        self.statue = 0
#        self.traffic_direction = direction
#        self.count = count
#        self.map_x = map_x
#        self.map_y = map_y
#        self.visible = True
#    def update(self):
#        if self.visible:
#            self.count = self.count + 1
#            if self.count == self.greentime + self.redtime:
#                self.statue = 0
#                self.count = 0
#                self.color = pg.Color('green')
#            elif self.count == self.greentime:
#                self.statue = 1
#                self.color = pg.Color('red')
#    def draw(self, screen):
#        if self.visible:
#            if self.traffic_direction == 0:
#                self.rect.y = self.dy - (self.rect.h / 2)
#                self.rect.x = self.dx + ((self.dw / 2) - self.rect.w / 2)
#            elif self.traffic_direction == 1:
#                self.rect.x = self.dx + self.dw - (self.rect.w / 2)
#                self.rect.y = self.dy + ((self.dh / 2) - self.rect.h / 2)
#            elif self.traffic_direction == 2:
#                self.rect.y = self.dy - (self.rect.h / 2) + self.dh
#                self.rect.x = self.dx + ((self.dw / 2) - self.rect.w / 2)
#            elif self.traffic_direction == 3:
#                self.rect.y = self.dy + ((self.dh / 2) - self.rect.h / 2)
#                self.rect.x = self.dx - (self.rect.w / 2)
#        pg.draw.rect(screen, self.color, self.rect, 0)
#    def send(sock, command, x, y, direction, stute):
#        x = str(x)
#        y = str(y)
#        direction = str(direction)
#        stute = str(stute)
#        sock.send(("send:" + command + ",x:" + str(x) + ",y:" + str(y) + ",direction:" + str(direction) + ",stute:" + str(stute)).encode("utf-8"))
#