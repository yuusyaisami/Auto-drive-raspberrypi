import pygame as pg
import pygame.mouse as ms
import driver as dr
import time
import constant as cs
import random
import item 
from picarx import Picarx
from time import sleep
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import time
import keyboard
kernel_5 = np.ones((5,5),np.uint8)
driver = dr.Driver(1,4,0)
shorter = dr.MazeShortest()
px = Picarx()
px.set_grayscale_reference(1400)
color_dict = {'red':[0,4],'orange':[5,18],'yellow':[22,37],'green':[42,85],'blue':[92,110],'purple':[115,165],'red_2':[165,180]}
pg.init()
screen = pg.display.set_mode((740, 480))
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
FONT = pg.font.Font(None, 32)
pg.display.set_caption("drivers")
# ウィンドウのアイコンを設定
cs.TRAFFIC_TIMES = 60



map = [ [99,99,99,99,99,99, 99,99, 99],
        [99, 0, 0, 0, 0, 0,  0, 0, 99],
        [99, 0,99, 0,99, 0, 99, 0, 99],
        [99, 0, 0, 0, 0, 0,  0, 0, 99],
        [99, 0,99, 0,99, 0, 99, 0, 99],
        [99, 0, 0, 0, 0, 0, 0 , 0, 99],
        [99, 0,99, 0,99, 0, 99, 0, 99],
        [99, 0, 0, 0, 0, 0, 0 , 0, 99],
        [99,99,99,99,99,99, 99,99, 99]]
class Traffic:
    def __init__(self, x, y, time, redtime, direction, map_x, map_y, count = 0,Train = False):
        self.width = 6
        self.height = 6
        self.rect = pg.Rect(x, y, self.width, self.height)
        self.dx = x
        self.dy = y
        self.time = time
        self.redtime = redtime
        self.color = pg.Color('green')
        self.statue = 0
        self.traffic_direction = direction
        self.count = count
        self.map_x = map_x
        self.map_y = map_y
        self.Train = Train
    def update(self):
        if not self.Train:
            self.count = self.count + 1
            if self.count > self.time + self.redtime:
                self.statue = 0
                self.count = 0
                self.color = pg.Color('green')
            elif self.count > self.time:
                self.statue = 1
                self.color = pg.Color('red')
        elif self.Train:
            self.count = self.count + 1
            if self.count > self.time + self.redtime:
                self.statue = 0
                self.count = 0
                self.color = pg.Color(30,30,30)
            elif self.count > self.time:
                self.statue = 1
                self.color = pg.Color('yellow')
    def draw(self, screen):
        if not self.Train:
            if self.traffic_direction == 0:
                self.rect.y = self.dy - 2
                self.rect.x = self.dx + 7
            elif self.traffic_direction == 1:
                self.rect.x = self.dx + 16
                self.rect.y = self.dy + 7 
            elif self.traffic_direction == 2:
                self.rect.y = self.dy + 16
                self.rect.x = self.dx + 7
            elif self.traffic_direction == 3:
                self.rect.y = self.dy + 7
                self.rect.x = self.dx - 2
        if self.Train:
            if self.traffic_direction == 0:
                self.rect.y = self.dy + 1
                self.rect.x = self.dx + 7
                self.rect.h = 18
            elif self.traffic_direction == 1:
                self.rect.x = self.dx + 1
                self.rect.y = self.dy + 7
                self.rect.w = 18
            elif self.traffic_direction == 2:
                self.rect.y = self.dy + 12
                self.rect.x = self.dx + 7
                self.rect.h = 22
            elif self.traffic_direction == 3:
                self.rect.y = self.dy + 7
                self.rect.x = self.dx
                self.rect.w = 22
        pg.draw.rect(screen, self.color, self.rect, 0)
        
class DriverMapBox:
    def __init__(self, x, y, w, h ,map_x, map_y):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.selected_color = pg.Color("cyan")
        self.colorS = pg.Color("white")
        self.colorG = pg.Color(128,128,0)
        self.box_status = 1
        self.map_x = map_x
        self.map_y = map_y
        self.active = False
        self.menubar_active = False
        self.rightbar = None

    def handle_event(self, event, Driver, gx, gy, run):
        if self.rightbar != None:
            self.rightbar.handle_event(event)
        if event.type == pg.MOUSEBUTTONDOWN:
            # ユーザーがButton rectをクリックした場合。
            
            if self.rect.collidepoint(event.pos):
                if event.button == 1:  # 左クリック
                    print("Left Click!" + " x : " +str(self.map_x) + "    y : " + str(self.map_y))
                    # クラスをアクティブにする
                    self.active = not self.active
                    self.color = self.selected_color
                if event.button == 3:
                    self.active = not self.active
                    self.color = self.selected_color
                    x, y = ms.get_pos()
                    texts = ["set wall", "set road", "start pos", "goal pos", "delete traffic","traffic up/down", "traffic left/right", "traffic all"]
                    self.rightbar = item.RightBar(x, y,texts,)
            else:
                self.active = False
                self.color = COLOR_INACTIVE
        if event.type == pg.KEYDOWN and self.active:
            if event.key == pg.K_w:
                Driver.map[self.map_y][self.map_x] = 99
                self.active = False
            if event.key == pg.K_r:
                Driver.map[self.map_y][self.map_x] = 0
                self.active = False
            if event.key == pg.K_s:
                for y in range(len(map)):
                    for x in range(len(map[0])):
                        if Driver.map[y][x] == 1:
                            Driver.map[y][x] = 0
                driver.x = self.map_x
                driver.y = self.map_y
                Driver.map[self.map_y][self.map_x] = 1
                self.active = False
            if event.key == pg.K_g:
                if Driver.map[self.map_y][self.map_x] == 99:
                    return

                gx.text = str(self.map_x)
                gy.text = str(self.map_y)
                for y in range(len(map)):
                    for x in range(len(map[0])):
                        if Driver.map[y][x] == 666:
                            Driver.map[y][x] = 0
                Driver.map[self.map_y][self.map_x] = 666
                self.active = False
            if event.key == pg.K_SPACE:
                run.forcing_run = True
                self.active = False
            keys = pg.key.get_pressed()

            if keys[pg.K_UP] and keys[pg.K_LCTRL] and keys[pg.K_x]:
                index = Driver.search_traffic(self.map_x, self.map_y, 0, True)
                if index == -1:
                    pass
                else:
                    del Driver.Traffics[index] 
            elif keys[pg.K_RIGHT] and keys[pg.K_LCTRL] and keys[pg.K_x]:
                index = Driver.search_traffic(self.map_x, self.map_y, 1, True)
                if index == -1:
                    pass
                else:
                    del Driver.Traffics[index] 
            elif keys[pg.K_DOWN] and keys[pg.K_LCTRL] and keys[pg.K_x]:
                index = Driver.search_traffic(self.map_x, self.map_y, 2, True)
                if index == -1:
                    pass
                else:
                    del Driver.Traffics[index]
            elif keys[pg.K_LEFT] and keys[pg.K_LCTRL] and keys[pg.K_x]:
                index = Driver.search_traffic(self.map_x, self.map_y, 3, True)
                if index == -1:
                    pass
                else:
                    del Driver.Traffics[index] 
            
            elif keys[pg.K_UP] and keys[pg.K_t] and keys[pg.K_c]:
                Driver.Traffics.append(Traffic(Driver.rect.x + self.map_x * 30,Driver.rect.y + self.map_y * 30,cs.TRAFFIC_TIMES,cs.TRAFFIC_TIMES,1,self.map_x,self.map_y))

            elif (keys[pg.K_UP] or keys[pg.K_DOWN]) and keys[pg.K_LCTRL] and keys[pg.K_c]:
                Driver.Traffics.append(Traffic(Driver.rect.x + self.map_x * 30,Driver.rect.y + self.map_y * 30,cs.TRAFFIC_TIMES,cs.TRAFFIC_TIMES,0,self.map_x,self.map_y))
                Driver.Traffics.append(Traffic(Driver.rect.x + self.map_x * 30,Driver.rect.y + self.map_y * 30,cs.TRAFFIC_TIMES,cs.TRAFFIC_TIMES,2,self.map_x,self.map_y))
            elif (keys[pg.K_RIGHT] or keys[pg.K_LEFT])  and keys[pg.K_LCTRL] and keys[pg.K_c]:
                Driver.Traffics.append(Traffic(Driver.rect.x + self.map_x * 30,Driver.rect.y + self.map_y * 30,cs.TRAFFIC_TIMES,cs.TRAFFIC_TIMES,1,self.map_x,self.map_y))
                Driver.Traffics.append(Traffic(Driver.rect.x + self.map_x * 30,Driver.rect.y + self.map_y * 30,cs.TRAFFIC_TIMES,cs.TRAFFIC_TIMES,3,self.map_x,self.map_y))
            
            elif (keys[pg.K_UP] or keys[pg.K_DOWN]) and keys[pg.K_LCTRL] and keys[pg.K_v]:
                Driver.Traffics.append(Traffic(Driver.rect.x + self.map_x * 30,Driver.rect.y + self.map_y * 30,cs.TRAFFIC_TIMES,cs.TRAFFIC_TIMES,0,self.map_x,self.map_y))
                Driver.Traffics.append(Traffic(Driver.rect.x + self.map_x * 30,Driver.rect.y + self.map_y * 30,cs.TRAFFIC_TIMES,cs.TRAFFIC_TIMES,2,self.map_x,self.map_y))
                Driver.Traffics.append(Traffic(Driver.rect.x + self.map_x * 30,Driver.rect.y + self.map_y * 30,cs.TRAFFIC_TIMES,cs.TRAFFIC_TIMES,1,self.map_x,self.map_y, cs.TRAFFIC_TIMES))
                Driver.Traffics.append(Traffic(Driver.rect.x + self.map_x * 30,Driver.rect.y + self.map_y * 30,cs.TRAFFIC_TIMES,cs.TRAFFIC_TIMES,3,self.map_x,self.map_y, cs.TRAFFIC_TIMES))

            elif (keys[pg.K_RIGHT] or keys[pg.K_LEFT]) and keys[pg.K_LCTRL] and keys[pg.K_v]:
                Driver.Traffics.append(Traffic(Driver.rect.x + self.map_x * 30,Driver.rect.y + self.map_y * 30,cs.TRAFFIC_TIMES,cs.TRAFFIC_TIMES,0,self.map_x,self.map_y, cs.TRAFFIC_TIMES))
                Driver.Traffics.append(Traffic(Driver.rect.x + self.map_x * 30,Driver.rect.y + self.map_y * 30,cs.TRAFFIC_TIMES,cs.TRAFFIC_TIMES,2,self.map_x,self.map_y, cs.TRAFFIC_TIMES))
                Driver.Traffics.append(Traffic(Driver.rect.x + self.map_x * 30,Driver.rect.y + self.map_y * 30,cs.TRAFFIC_TIMES,cs.TRAFFIC_TIMES,1,self.map_x,self.map_y))
                Driver.Traffics.append(Traffic(Driver.rect.x + self.map_x * 30,Driver.rect.y + self.map_y * 30,cs.TRAFFIC_TIMES,cs.TRAFFIC_TIMES,3,self.map_x,self.map_y))

            if keys[pg.K_UP] and keys[pg.K_t] and keys[pg.K_LCTRL]:
                Driver.Traffics.append(Traffic(Driver.rect.x + self.map_x * 30,Driver.rect.y + self.map_y * 30,cs.TRAFFIC_TIMES,cs.TRAFFIC_TIMES,0,self.map_x,self.map_y, cs.TRAFFIC_TIMES))
            elif keys[pg.K_RIGHT] and keys[pg.K_t] and keys[pg.K_LCTRL]:
                Driver.Traffics.append(Traffic(Driver.rect.x + self.map_x * 30,Driver.rect.y + self.map_y * 30,cs.TRAFFIC_TIMES,cs.TRAFFIC_TIMES,1,self.map_x,self.map_y, cs.TRAFFIC_TIMES))
            elif keys[pg.K_DOWN] and keys[pg.K_t] and keys[pg.K_LCTRL]:
                Driver.Traffics.append(Traffic(Driver.rect.x + self.map_x * 30,Driver.rect.y + self.map_y * 30,cs.TRAFFIC_TIMES,cs.TRAFFIC_TIMES,2,self.map_x,self.map_y, cs.TRAFFIC_TIMES))
            elif keys[pg.K_LEFT] and keys[pg.K_t] and keys[pg.K_LCTRL]:
                Driver.Traffics.append(Traffic(Driver.rect.x + self.map_x * 30,Driver.rect.y + self.map_y * 30,cs.TRAFFIC_TIMES,cs.TRAFFIC_TIMES,3,self.map_x,self.map_y, cs.TRAFFIC_TIMES))
            elif keys[pg.K_UP] and keys[pg.K_t]:
                Driver.Traffics.append(Traffic(Driver.rect.x + self.map_x * 30,Driver.rect.y + self.map_y * 30,cs.TRAFFIC_TIMES,cs.TRAFFIC_TIMES,0,self.map_x,self.map_y))
            elif keys[pg.K_RIGHT] and keys[pg.K_t]:
                Driver.Traffics.append(Traffic(Driver.rect.x + self.map_x * 30,Driver.rect.y + self.map_y * 30,cs.TRAFFIC_TIMES,cs.TRAFFIC_TIMES,1,self.map_x,self.map_y))
            elif keys[pg.K_DOWN] and keys[pg.K_t]:
                Driver.Traffics.append(Traffic(Driver.rect.x + self.map_x * 30,Driver.rect.y + self.map_y * 30,cs.TRAFFIC_TIMES,cs.TRAFFIC_TIMES,2,self.map_x,self.map_y))
            elif keys[pg.K_LEFT] and keys[pg.K_t]:
                Driver.Traffics.append(Traffic(Driver.rect.x + self.map_x * 30,Driver.rect.y + self.map_y * 30,cs.TRAFFIC_TIMES,cs.TRAFFIC_TIMES,3,self.map_x,self.map_y))
    def update(self, Status, Driver,gx, gy):
        if not self.active:
            if Status == 99:
                self.box_status = 0
                self.color = COLOR_INACTIVE
            elif Status == 90:
                self.box_status = 1
                self.color = self.colorG
            elif Status == 80:
                self.box_status = 1
                self.color = COLOR_ACTIVE
            elif Status == 1:
                self.box_status = 1
                self.color = self.colorS
            elif Status == 666:
                self.box_status = 1
                self.color = pg.Color('gold')
            else:
                self.box_status = 1
                self.color = COLOR_INACTIVE
        if self.rightbar != None:
            self.rightbar.update()
            if self.rightbar.selected:
                # マップ処理
                if self.rightbar.selected_index == 0:
                    Driver.map[self.map_y][self.map_x] = 99
                    self.active = False
                elif self.rightbar.selected_index == 1:
                    Driver.map[self.map_y][self.map_x] = 0
                    self.active = False
                elif self.rightbar.selected_index == 2:
                    for y in range(len(map)):
                        for x in range(len(map[0])):
                            if Driver.map[y][x] == 1:
                                Driver.map[y][x] = 0
                    driver.x = self.map_x
                    driver.y = self.map_y
                    Driver.map[self.map_y][self.map_x] = 1
                    self.active = False
                if self.rightbar.selected_index == 3:
                    if Driver.map[self.map_y][self.map_x] == 99:
                        return
                    gx.text = str(self.map_x)
                    gy.text = str(self.map_y)
                    for y in range(len(map)):
                        for x in range(len(map[0])):
                            if Driver.map[y][x] == 666:
                                Driver.map[y][x] = 0
                                
                    Driver.map[self.map_y][self.map_x] = 666
                    self.active = False
                if self.rightbar.selected_index == 4:
                    index = Driver.search_traffic(self.map_x, self.map_y, -1, True)
                    if index == -1:
                        pass
                    else:
                        del Driver.Traffics[index] 
                if self.rightbar.selected_index == 5:
                    Driver.Traffics.append(Traffic(Driver.rect.x + self.map_x * 30,Driver.rect.y + self.map_y * 30,cs.TRAFFIC_TIMES,cs.TRAFFIC_TIMES,0,self.map_x,self.map_y))
                    Driver.Traffics.append(Traffic(Driver.rect.x + self.map_x * 30,Driver.rect.y + self.map_y * 30,cs.TRAFFIC_TIMES,cs.TRAFFIC_TIMES,2,self.map_x,self.map_y))
                if self.rightbar.selected_index == 6:
                    Driver.Traffics.append(Traffic(Driver.rect.x + self.map_x * 30,Driver.rect.y + self.map_y * 30,cs.TRAFFIC_TIMES,cs.TRAFFIC_TIMES,1,self.map_x,self.map_y))
                    Driver.Traffics.append(Traffic(Driver.rect.x + self.map_x * 30,Driver.rect.y + self.map_y * 30,cs.TRAFFIC_TIMES,cs.TRAFFIC_TIMES,3,self.map_x,self.map_y))
                if self.rightbar.selected_index == 7:
                    Driver.Traffics.append(Traffic(Driver.rect.x + self.map_x * 30,Driver.rect.y + self.map_y * 30,cs.TRAFFIC_TIMES,cs.TRAFFIC_TIMES,0,self.map_x,self.map_y))
                    Driver.Traffics.append(Traffic(Driver.rect.x + self.map_x * 30,Driver.rect.y + self.map_y * 30,cs.TRAFFIC_TIMES,cs.TRAFFIC_TIMES,2,self.map_x,self.map_y))
                    Driver.Traffics.append(Traffic(Driver.rect.x + self.map_x * 30,Driver.rect.y + self.map_y * 30,cs.TRAFFIC_TIMES,cs.TRAFFIC_TIMES,1,self.map_x,self.map_y, cs.TRAFFIC_TIMES))
                    Driver.Traffics.append(Traffic(Driver.rect.x + self.map_x * 30,Driver.rect.y + self.map_y * 30,cs.TRAFFIC_TIMES,cs.TRAFFIC_TIMES,3,self.map_x,self.map_y, cs.TRAFFIC_TIMES))

            if not self.rightbar.Active:
                self.rightbar = None
    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect, self.box_status)
        
class DriverMap:
    def __init__(self, x, y, row, column, map, w = 0, h = 0):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.row = row
        self.column = column
        self.dr = dr
        self.map = map
        self.animation = False
        self.animationcount = 0
        self.DrBoxs = [[None for _ in range(column)] for _ in range(row)]
        self.car = Car(10,10)
        self.direction = 0
        self.stop = False
        for y in range(row):
            for x in range(column):
                self.DrBoxs[y][x] = DriverMapBox(self.rect.x + x * 30, self.rect.y + y * 30, 20, 20, x, y)
        self.Traffics = [Traffic(self.rect.x + 1 * 30, self.rect.y + 1 * 30,120, 120 ,3, 1, 1, 120),Traffic(self.rect.x + 1 * 30, self.rect.y + 1 * 30,120, 120, 0, 1, 1),
                         Traffic(self.rect.x + 3 * 30, self.rect.y + 3 * 30, 60,  60, 1, 3, 3),     Traffic(self.rect.x + 3 * 30, self.rect.y + 3 * 30, 60,  60, 2, 3, 3, 60),
                         Traffic(self.rect.x + 3 * 30, self.rect.y + 3 * 30, 60,  60, 3, 3, 3),     Traffic(self.rect.x + 3 * 30, self.rect.y + 3 * 30, 60,  60, 0, 3, 3, 60),
                         Traffic(self.rect.x + 6 * 30, self.rect.y + 7 * 30, 60,  60, 1, 6, 7, 60,True)]
        self.map[driver.y][driver.x] = 1
    def update(self, run, gx, gy,img):
        for y in range(self.row):
            for x in range(self.column):
                self.DrBoxs[y][x].update(self.map[y][x], self,gx,gy)
        for traffic in self.Traffics:
            traffic.update()
        #run btnが押されたとき一度だけ実行される
        if run:
            self.map = shorter.ResetMaze(self.map)
            self.map = shorter.MazeWaterValue(self.map, driver)
            self.map[int(gy.text)][int(gx.text)] = 98
            self.map, error = shorter.MazeShortestRoute(self.map, driver)
            self.animation = True
            self.animationcount = 0
            if error == 1:
                print("error : 目的地に到達できません")
        if self.animation:
            #車の移動を実行する
            # 車の処理が始まっていない
            if not self.car.Determined:
                self.stop = self.TrafficStop()
                
            # 信号にかかっていないかつ車の処理が行われていないとき
            if not self.stop and not self.car.Determined:
                    
                
                self.map, driver.x, driver.y, self.direction, driver.direction = shorter.DriverDirection(self.map, driver)
                # 移動が終わったら実行する
                if self.direction == -2:
                    self.map = shorter.ResetMaze(self.map)
                    self.map[driver.y][driver.x] = 1
                    self.animation = False
                    print("owari")
                    return
                self.car.initial_Determined = True
        self.car.update(self.direction,img)
    def draw(self, screen):
        for y in range(self.row):
            for x in range(self.column):
                self.DrBoxs[y][x].draw(screen)
        for traffics in self.Traffics:
            traffics.draw(screen)
        for y in range(self.row):
            for x in range(self.column):
                if self.DrBoxs[y][x].rightbar != None:
                    self.DrBoxs[y][x].rightbar.draw(screen)
                
    def search_traffic(self, x , y, direction, errorMessage = False):
        if direction != -1:
            for index in range(len(self.Traffics)):
                if self.Traffics[index].map_x == x and self.Traffics[index].map_y == y and self.Traffics[index].traffic_direction == direction:
                    return index
        elif direction == -1:
            for index in range(len(self.Traffics)):
                if self.Traffics[index].map_x == x and self.Traffics[index].map_y == y:
                    return index
        if errorMessage: 
            return -1
    def TrafficStop(self):
        if self.map[driver.y - 1][driver.x] == 90 and driver.direction == 0:
            nowtraffic = self.search_traffic(driver.x , driver.y - 1, driver.direction)
            if nowtraffic != None:
                if self.Traffics[nowtraffic].statue == 1:
                    return True
        if self.map[driver.y][driver.x + 1] == 90 and driver.direction == 1:
            nowtraffic = self.search_traffic(driver.x + 1 , driver.y, driver.direction)
            if nowtraffic != None:
                if self.Traffics[nowtraffic].statue == 1:
                    return True
        if self.map[driver.y + 1][driver.x] == 90 and driver.direction == 2:
            nowtraffic = self.search_traffic(driver.x , driver.y + 1, driver.direction)
            if nowtraffic != None:
                if self.Traffics[nowtraffic].statue == 1:
                    return True
        if self.map[driver.y][driver.x - 1] == 90 and driver.direction == 3:
            nowtraffic = self.search_traffic(driver.x - 1 , driver.y, driver.direction)
            if nowtraffic != None:
                if self.Traffics[nowtraffic].statue == 1:
                    return True
        return False
class EditTool:
    def __init__(self):
        self.car_direction = item.Text(500, 86, 100, 20, "car direction : 0", 24)
        self.input_cardirection = item.InputBox(500, 110, 60,32 ,str(0),str(0))
        self.tutorial_run = item.ButtonSwitching(675, 40, 24, 32, "T")
        self.text1 = item.Text(350, 120, 100, 20, "Goal     : G", 24)
        self.text2 = item.Text(350, 140, 100, 20, "Start     : S", 24)
        self.text3 = item.Text(350, 160, 100, 20, "Wall      : W", 24)
        self.text4 = item.Text(350, 180, 100, 20, "Road    : R", 24)
        self.text5 = item.Text(350, 220, 100, 20, "Traffic set                                          : T + Arrow", 24)
        self.text6 = item.Text(350, 240, 100, 20, "Traffic delete                                    : ctrl + x + Arrow", 24)
        self.text7 = item.Text(350, 260, 100, 20, "Traffic set Up/down or left/right  : ctrl + c + Arrow", 24)
        self.text8 = item.Text(350, 280, 100, 20, "Traffic set Up/down/left/right       : ctrl + v + Arrow", 24)


        traffic_time = item.Text(500, 150, 100, 20, "traffic time : 60", 24)
        input_traffic_time = item.InputBox(500, 174, 50,32,str(60),str(60))
        self.inputlist = [self.input_cardirection,input_traffic_time,self.tutorial_run ]
        self.textlist = [self.car_direction,traffic_time]
        self.Ttextlist = [self.text1,self.text2,self.text3,self.text4,self.text5,self.text6,self.text7,self.text8]
        self.DeterminedChange = self.input_cardirection.Determined

    def update(self):
        try:
            for list in self.inputlist:
                list.update()
            if self.tutorial_run.Determined:
                for text in self.Ttextlist:
                    text.update(None)
            self.textlist[0].update("car direction : " + str(cs.TRAFFIC_TIMES))
            self.textlist[1].update("traffic time : " + str(cs.TRAFFIC_TIMES))
            self.tutorial_run.update()
            cs.TRAFFIC_TIMES = int(self.inputlist[1].Determined)
            if self.input_cardirection.Determined != self.DeterminedChange:
                self.DeterminedChange = self.input_cardirection.Determined
                driver.direction = int(self.DeterminedChange)
                self.textlist[0].update("car direction : " + str(driver.direction))
            else:
                self.textlist[0].update("car direction : " + str(driver.direction))
        except:
            print("edit error")

        
    def draw(self, screen):
        for list in self.inputlist:
            list.draw(screen)
        for text in self.textlist:
            text.draw(screen)
        if self.tutorial_run.Determined:
            for text in self.Ttextlist:
                text.draw(screen)
class CarJamp:
    def __init__(self, x, y, w, h, player_image):
        self.rect = pg.Rect(x, y, w, h)
        self.player_image = player_image
        self.timer = 0
        self.player = item.ButtonGravity(30,460, 37,18,player_image)
        self.score = item.Text(x, y, w / 2, h / 2)
        self.obstacles = []
        self.deathtime = 0
        self.speed = 5
        self.scorevalue = 0
        self.start = False
        self.randomrange = 5
        self.randomrange_min = 0
    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if not self.start:
                    self.scorevalue = 0
                self.start = True
                self.velocity = 0
                self.velocity -= 20.0
        self.player.handle_event(event)
    def update(self):
        self.player.update()
        for obstacle in self.obstacles:
            if self.player.collision(obstacle.rect.x,obstacle.rect.y,obstacle.rect.w,obstacle.rect.h):
                self.start = False
                self.timer = -11
                self.speed = 5
                self.player.time = 0.2
                self.randomrange = 5
                self.player.jamp = 18
                self.randomrange_min = 0
            if self.timer > -10:
                obstacle.update(self.speed)

        if self.start:
            self.timer = self.timer + 1
            if self.timer > 30 and self.timer % 25 == 0 and random.randint(1,2) == 2 :
                Random = random.randint(1,self.randomrange)
                if Random == 1 or Random == 5 or Random == 11: 
                    self.obstacles.append(item.Obstacle_jamp(self.rect.x + 200,470,10,10,self.rect.w + self.rect.x,0))
                elif Random == 2 or Random == 3:
                    self.obstacles.append(item.Obstacle_Wide(self.rect.x + 200,470,10,10,self.rect.w + self.rect.x,0))
                elif Random == 6 or Random == 8 or Random == 12:
                    self.obstacles.append(item.Obstacle_Medium(self.rect.x + 200,470,10,10,self.rect.w + self.rect.x,0))
                elif Random == 9 or Random == 10 or Random == 13:
                    self.obstacles.append(item.Obstacle_Large(self.rect.x + 200,470,10,10,self.rect.w + self.rect.x,0))
                elif Random == 14 or Random == 15:
                    self.obstacles.append(item.Obstacle_Super_Wide(self.rect.x + 200,470,10,10,self.rect.w + self.rect.x,0))
                    self.timer = -10
                elif Random == 16 or Random == 17:
                    self.obstacles.append(item.Obstacle_Super_High(self.rect.x + 200,470,10,10,self.rect.w + self.rect.x,0))
                    self.timer = -10
                elif Random == 18 or Random == 20:
                    self.obstacles.append(item.Obstacle_Super_fly(self.rect.x + 200,470,10,10,self.rect.w + self.rect.x,0))
                    self.timer = -10
                elif Random == 21 or Random == 22:
                    self.obstacles.append(item.Obstacle_Super_cube(self.rect.x + 200,470,10,10,self.rect.w + self.rect.x,0))
                    self.timer = -10
                elif Random == 23 or Random == 24:
                    self.obstacles.append(item.Obstacle_Ghost(self.rect.x + 200,470,10,10,self.rect.w + self.rect.x,0))
                elif Random == 25 or Random == 26:
                    self.obstacles.append(item.Obstacle_Super_jamp(self.rect.x + 200,470,10,10,self.rect.w + self.rect.x,0))
                else:
                    self.obstacles.append(item.Obstacle_Small(self.rect.x,470,10,10,self.rect.w + self.rect.x,0))
            for i in range(len(self.obstacles) - 1):
                if self.obstacles[i].rect.x < self.obstacles[i].e_x:
                    del self.obstacles[i]
                    self.scorevalue += 1
            if self.scorevalue == 7:
                self.scorevalue += 1
                self.timer = -30
                self.score.text = "speed up"
                self.speed = 8
                self.player.time += 0.1
                self.player.jamp += 5
                self.randomrange += 5
            if self.scorevalue == 15:
                self.scorevalue += 1
                self.timer = -30
                self.score.text = "Increased difficulty"
                self.randomrange += 6
            if self.scorevalue == 30:
                self.scorevalue += 1
                self.timer = -60
                self.score.text = "highest level of difficulty"
                self.randomrange += 10
                self.randomrange_min += 10
            
        else:
            self.obstacles.clear()
            self.score.update("score : " + str(self.scorevalue))
    def draw(self, screen):
        self.player.draw(screen)
        for obstacle in self.obstacles:
            obstacle.draw(screen)
        if self.timer < -10:
            self.score.draw(screen)
class Car:
    # ルール
    # initialは開始するとき、Trueにして、処理を停止させるときはinitialでない同じ名前の変数をFalseにしてください
    def __init__(self, angle, speed):
        self.angle = angle
        self.speed = speed
        self.black_reflectance = 50
        self.initial_Determined = False # Carの処理を開始するときはこの変数をTrueにする
        self.Determined = False # Carの処理を停止するときはこの変数をFalseにする

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
            self.Determined = True
            # 前進のみの場合 赤テープの部分でコースアウト判定になるので、ライントレースはチューニング処理を入れないことにする
            if direction == 0:
                self.do_Tuning = False
                print("前進")
            print("イニシャライズメイン処理")
            
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
                self.After(15)
            self.Curve(direction)
            for count in range(redflag):
                if y[count] > 90 and not self.curve and not self.aftertreatment:
                    # 前進以外は曲がる処理を必要とする
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


    def LineTrace(self):
        # ライントレース
        if self.linetrace:
            reflectance = px.get_grayscale_data()
            print(reflectance)
            if reflectance[0] < self.black_reflectance and reflectance[1] < self.black_reflectance and reflectance[2] < self.black_reflectance and not self.Tuning:
                px.forward(self.speed)
                px.set_dir_servo_angle(0)
                self.car_direction = 0
            elif reflectance[0] < self.black_reflectance and not self.Tuning:
                px.forward(self.speed)
                px.set_dir_servo_angle(-self.angle)
                self.car_direction = -1
            elif reflectance[2] < self.black_reflectance and not self.Tuning:
                px.forward(self.speed)
                px.set_dir_servo_angle(self.angle)
                self.car_direction = 1
            elif reflectance[0] > self.black_reflectance and reflectance[1] < self.black_reflectance and reflectance[2] > self.black_reflectance and not self.Tuning:
                px.forward(self.speed)
                px.set_dir_servo_angle(0)
                self.car_direction = 0
            elif not self.Tuning:
                print("tunig")
                if self.do_Tuning:
                    #ラインから外れた tuning処理
                    self.Tuning = True
                    self.linetrace = False
                    print("Tuning start")
    def LineTuning(self):
        if self.Tuning:
            on_line = False
            px.forward(self.speed)
            if self.car_direction == -1:
                px.set_dir_servo_angle(-self.angle - 20)
            if self.car_direction == 1:
                px.set_dir_servo_angle(self.angle + 20)
            reflectance = px.get_grayscale_data()
            if reflectance[0] < self.black_reflectance or reflectance[1] < self.black_reflectance or reflectance[2] < self.black_reflectance:
                self.TuningCount += 1
                on_line = True
            # ラインに復帰する
            if self.TuningCount > 2 or on_line:
                if self.car_direction == -1:
                    px.set_dir_servo_angle(self.angle - 5)
                if self.car_direction == 1:
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
                px.set_dir_servo_angle(-self.angle - 15)
                self.car_direction = -1
            if direction == 1:
                px.forward(self.speed)
                px.set_dir_servo_angle(self.angle + 15)
                self.car_direction = 1
            self.curve = True
            self.initial_curve = not self.initial_curve
            self.do_Tuning = False
            self.linetrace = False
            self.curve_count = 0
            print("Curve start")
        # コーナー処理
        if self.curve:
            reflectance = px.get_grayscale_data()
            self.curve_count += 1
            # ラインに乗ったかつ、初回時から50countした
            if (reflectance[0] < self.black_reflectance or reflectance[1] < self.black_reflectance or reflectance[2] < self.black_reflectance) and self.curve_count > 5:
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
                    print("After stop")
                else:
                    self.aftercount = 4


def main():
    with PiCamera() as camera:
        camera.resolution = (528,480)
        camera.framerate = 24
        rawCapture = PiRGBArray(camera, size=camera.resolution)
        time.sleep(2)
        clock = pg.time.Clock()

        edit_tool = EditTool()

        carediter_image = pg.transform.scale(pg.image.load("ImageFile/carediter.png"), (40, 20))
        
        car_jamp = CarJamp(10,400,600,300,carediter_image)


        input_x = item.InputBox(20, 40, 100, 32)
        input_y = item.InputBox(250, 40, 100, 32)

        btn_run = item.Button(500, 40, 54, 32, "Run")
        option_run = item.ButtonSwitching(573, 40, 84, 32, "Option")
        btns = [btn_run, option_run,car_jamp]
        input_boxes = [input_x, input_y]
        text_lines = []
        for a in range(len(map[0])):
            text_lines.append(item.Text(40 + a * 30, 98, 10, 10, str(a), 24))
        for a in range(len(map)):
            text_lines.append(item.Text(20, 118 + a * 30, 10, 10, str(a), 24))

        text_ornament_x = item.Text(20, 10, 100, 20, "X")
        text_ornament_y = item.Text(250, 9, 100, 20, "Y")
        driver_map = DriverMap(40,120,len(map[0]),len(map),map)
        text_lines.append(text_ornament_x)
        text_lines.append(text_ornament_y)
        for frame in camera.capture_continuous(rawCapture, format="bgr",use_video_port=True):
            img = frame.array
            rawCapture.truncate(0)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return
                for box in input_boxes:
                    box.handle_event(event)
                for btn in btns:
                    btn.handle_event(event)
                for y in range(len(map)):
                    for x in range(len(map[0])):
                        driver_map.DrBoxs[y][x].handle_event(event, driver_map,input_boxes[0],input_boxes[1],btns[0])
                for edit_input in edit_tool.inputlist:
                    edit_input.handle_event(event)


            if option_run.Determined:
                edit_tool.update()
            driver_map.update(btn_run.Determined, input_x, input_y,img)
            for box in input_boxes:
                box.update()
            for text in text_lines:
                text.update(None)
            for btn in btns:
                btn.update()
            screen.fill((30, 30, 30))
            if option_run.Determined:
                edit_tool.draw(screen)
            for box in input_boxes:
                box.draw(screen)
            for text in text_lines:
                text.draw(screen)
            for btn in btns:
                btn.draw(screen)
            driver_map.draw(screen)
            pg.display.flip()
            clock.tick(24)
        cv2.destroyAllWindows()
        camera.close()  


if __name__ == '__main__':
    main()
    pg.quit()