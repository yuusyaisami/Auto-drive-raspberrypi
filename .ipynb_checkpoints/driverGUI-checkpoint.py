from pygui import gui
import pygame as pg
import driver as dr
import variables as vr
import numpy as np
import pygame.mouse as ms
np.map = [ [99,99,99,99,99,99, 99,99, 99],
        [99, 0, 0, 0, 0, 0,  0, 0, 99],
        [99, 0,99, 0,99, 0, 99, 0, 99],
        [99, 0, 0, 0, 0, 0,  0, 0, 99],
        [99, 0,99, 0,99, 0, 99, 0, 99],
        [99, 0, 0, 0, 0, 0, 0 , 0, 99],
        [99, 0,99, 0,99, 0, 99, 0, 99],
        [99, 0, 0, 0, 0, 0, 0 , 0, 99],
        [99,99,99,99,99,99, 99,99, 99]]
var = vr.Variables()
driver = dr.Driver(1,4,0,np.map)
shorter = dr.MazeShortest()
pg.init()
pg.display.set_caption("drivers")
# ウィンドウのアイコンを設定
icon_image = pg.image.load("icon.png")  # アイコンとして使用する画像をロード
pg.display.set_icon(icon_image)
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
            if self.count > self.greentime + self.redtime:
                self.statue = 0
                self.count = 0
                self.color = pg.Color('green')
            elif self.count > self.greentime:
                self.statue = 1
                self.color = pg.Color('red')
    def draw(self, screen):
        if self.visible:
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
# 自動走行のクラス
class DriverMap:
    def __init__(self):
        self.init_run = False
        self.run = False
        self.simulation_count = 0
    def handle_event(self, event):
        pass
    def update(self, mainscene):
        if mainscene.menu_file.clicked_index != -1:
            pass
        if mainscene.menu_edit.clicked_index != -1:
            pass
        #--------------------------------------------------自動走行処理--------------------------------------------------
        if mainscene.run_button.clicked:
            self.init_run = True
        if self.init_run:
            driver.map = shorter.ResetMaze(driver.map)
            driver.map = shorter.MazeWaterValue(driver.map, driver)
            driver.map[driver.goal_y][driver.goal_x] = 98
            driver.map, error = shorter.MazeShortestRoute(driver.map, driver)
            if error == 1:
                print("error : 目的地に到達できません")
                self.init_run = False
                return
            self.run = True
            self.init_run = False
            self.simulation_count = 0
            
        if self.run:
            self.simulation_count += 1
            if self.simulation_count % 20 == 0:
                if not driver.traffic_stop():
                    driver.map, driver.x, driver.y, direction, driver.direction = shorter.DriverDirection(driver.map, driver)
                    # 移動が終わったら実行する
                    if direction == -2:
                        driver.map = shorter.ResetMaze(driver.map)
                        driver.map[driver.y][driver.x] = 1
                        self.run = False
                else :
                    self.simulation_count = 15
    
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

        for y in range(driver.map_y):
            for x in range(driver.map_x):
                self.row.append(DriverMapBox(pg.Rect(self.rect.x + x * size,self.rect.y + y * size, self.width, self.width),x,y))
            self.mapbox.append(self.row)
            self.row = []
        pass
    def handle_event(self, event, mc):
        for y in range(len(self.mapbox)):
            for x in range(len(self.mapbox[0])):
                self.mapbox[y][x].handle_event(event, mc)


    def update(self, mc):
        if mc.createflag: # マッピング
            self.mapbox = []
            self.row = []
            try:
                driver.map[driver.goal_y][driver.goal_x] = 90
            except:
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
            for y in range(driver.map_y):
                for x in range(driver.map_x):
                    self.row.append(DriverMapBox(pg.Rect(self.rect.x + x * self.size,self.rect.y + y * self.size, self.width, self.width),x,y))
                self.mapbox.append(self.row)
                self.row = []
        #選択されたボックスの更新がなければ、-1(選択なし)
        driver.select_box_x = driver.select_box_y = -1
        for y in range(len(self.mapbox)):
            for x in range(len(self.mapbox[0])):
                self.mapbox[y][x].update(mc)
    def exist_rightclick(self):
        for y in range(len(self.mapbox)):
            for x in range(len(self.mapbox[0])):
                if self.mapbox[y][x].rightclicked and self.mapbox[y][x].selectme:
                    return True
        return False
    def draw(self, screen):
        self.rightbar_back = False
        for y in range(len(self.mapbox)):
            for x in range(len(self.mapbox[0])):
                self.mapbox[y][x].draw(screen)
                if self.mapbox[y][x].rightclicked and self.mapbox[y][x].selectme:
                    self.mouse_position_x_y[0] = self.mapbox[y][x].rightbar.rect.x
                    self.mouse_position_x_y[1] = self.mapbox[y][x].rightbar.rect.y
                    self.rightbar_back = True
                    self.mouse_position_x_y[2] = x
                    self.mouse_position_x_y[3] = y
        for traffic in driver.traffic:
                traffic.draw(screen)
        if self.rightbar_back:
            gui.tetragon(pg.Rect(self.mouse_position_x_y[0],self.mouse_position_x_y[1],140,len(self.mapbox[self.mouse_position_x_y[3]][self.mouse_position_x_y[2]].rightbar.elements) * self.mapbox[self.mouse_position_x_y[3]][self.mouse_position_x_y[2]].rightbar.size),var.COLOR_BACK,0,10,screen)
            self.mapbox[self.mouse_position_x_y[3]][self.mouse_position_x_y[2]].rightbar.draw(screen)
            
            
class DriverMapBox:
    def __init__(self,rect, x, y, width = 1):
        self.rect = rect
        self.x = x
        self.y = y
        self.width = width
        self.color = var.COLOR_INACTIVE
        self.color_wall = var.COLOR_INACTIVE
        self.color_road = var.COLOR_INACTIVE
        self.color_goal = var.COLOR_GOAL
        self.color_start = var.COLOR_START
        self.color_select = var.COLOR_SELECT
        self.color_track = var.COLOR_TRACK
        self.color_next = var.COLOR_NEXT
        self.selectme = False
        self.rightclicked = False
        self.release_count = 0
        self.release_flag = False
        self.rightbar = gui.RowText(pg.Rect(0,0,0,0),["1"],var.FONT,False)

        self.visible = True
    def handle_event(self, event, mc):
        if self.visible:
            x, y = ms.get_pos()
            if self.selectme and self.rightclicked:
                self.rightbar.handle_event(event)
                self.rightbar.update()
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
            if event.type == pg.MOUSEBUTTONDOWN and not mc.menu_edit.cancelrightclicked:
                # ユーザーがDriverMapBoxをクリックしたとき
                if self.rect.collidepoint(event.pos):
                    if event.button == 1 and not mc.maps.exist_rightclick():
                        self.selectme = not self.selectme
                        if not self.selectme:
                            self.rightclicked = False
                        else:
                            self.color = self.color_select
                            driver.rightclick_x = self.x
                            driver.rightclick_y = self.y
                    elif event.button == 3:
                        self.selectme = True
                        self.rightclicked = True
                        self.color = self.color_select
                        
                        self.rightbar = gui.RowText(pg.Rect(x + 5,y - 5,140,32), ["road", "wall", "goal", "start", "cross traffic", "over traffic", "delete traffic"], var.FONT_SMALL,True,False,30,140,var.COLOR_INACTIVE,var.COLOR_ACTIVE,var.COLOR_ACTIVE,True,False )
                else:
                    if y > 50:
                        self.release_flag = True

    def update(self, mc):
        if self.visible:
            if driver.map[self.y][self.x] == 99:
                self.color = self.color_wall
                self.width = 0
            elif driver.map[self.y][self.x] == 0:
                self.color = self.color_road
                self.width = 2
            elif driver.map[self.y][self.x] == 1:
                self.color = self.color_start
                self.width = 2
            elif driver.map[self.y][self.x] == 90:
                self.color = self.color_next
                self.width = 2
            elif driver.map[self.y][self.x] == 98:
                self.color = self.color_goal
                self.width = 2
            elif driver.map[self.y][self.x] == 80:
                self.color = self.color_track
                self.width = 2

            if self.selectme:
                driver.select_box_x = self.x
                driver.select_box_y = self.y
                self.color = self.color_select
            
            if self.release_flag:
                self.release_count += 1
                if self.release_count > 2:
                    self.release_count = 0
                    self.release_flag = False
                    self.selectme = False
                    self.rightclicked = False

            

    def draw(self, screen):
        #テトラゴンは処理が重くなるからだめ
        # gui.tetragon(self.rect, self.color, self.width, 5, screen)
        pg.draw.rect(screen, self.color,self.rect, self.width)
        
        if self.selectme and self.rightclicked:
            self.rightbar.draw(screen)

# 大まかな処理のクラス
class MainScene:
    def __init__(self):
        self.createflag = False
        self.visible = True
        self.visible_handle_event_and_update = True
        self.createmap_flag = False
        self.createmap_range = [9,9]
        self.variable_view = VariableView(pg.Rect(1100,60,0,0),False)
        self.menu_file = gui.Menubar(pg.Rect(20,10,75,32),"file(F)",["new create","save", "name save", "setting", "close Window"],var.FONT,True,False,32,170,var.COLOR_INACTIVE,var.COLOR_ACTIVE,var.COLOR_ACTIVE,True, True)
        self.menu_edit = gui.Menubar(pg.Rect(100,10,75,32),"edit(E)",["road","wall", "start", "goal", "traffic add", "up/down traffic add", "right/left traffic add", "all traffic add", "traffic delete"],var.FONT,True,False,32,210,var.COLOR_INACTIVE,var.COLOR_ACTIVE,var.COLOR_ACTIVE,True, True)
        self.menu_view = gui.Menubar(pg.Rect(190,10,75,32),"view(V)",["theme","variable view", "variable editer"],var.FONT,True,False,32,170,var.COLOR_INACTIVE,var.COLOR_ACTIVE,var.COLOR_ACTIVE,True, True)
        self.run_button = gui.Button(pg.Rect(var.WINDOWNSIZE_X - 100,10,75,32),"Run(F5)",var.FONT,True,var.COLOR_INACTIVE,var.COLOR_ACTIVE,var.COLOR_INACTIVE,True)
        self.menu_line = gui.Line(pg.Rect(0, 50,0,0),pg.Rect(1280,50,0,0),True,3)
        self.driver_map = DriverMap()
        self.maps = Maps(pg.Rect(20,100,var.BOXSIZE,var.BOXSIZE),var.BOXSPACE,var.BOXSIZE)
        self.objects = [self.menu_line,self.menu_file,self.menu_edit,self.menu_view, self.run_button] 
    def handle_event(self, event):
        if self.visible and self.visible_handle_event_and_update:
            for object in self.objects:
                object.handle_event(event)
            self.driver_map.handle_event(event)
            self.maps.handle_event(event, self)
    def update(self):
        if self.visible and self.visible_handle_event_and_update:
            for object in self.objects:
                object.update()
            self.driver_map.update(self)
            self.maps.update(self)
            self.createflag = False

            if self.menu_edit.clicked_index != -1:
                if self.menu_edit.clicked_name == "road":
                    try:
                        driver.map[driver.rightclick_y][driver.rightclick_x] = 0
                    except:
                        print("map box選択されていません")
                if self.menu_edit.clicked_name == "wall":
                    try:
                        driver.map[driver.rightclick_y][driver.rightclick_x] = 99
                    except:
                        print("map box選択されていないまたは、範囲外")
                if self.menu_edit.clicked_name == "start":
                    try:
                        driver.map[driver.rightclick_y][driver.rightclick_x] = 1
                        driver.x = driver.rightclick_x
                        driver.y = driver.rightclick_y
                    except:
                        print("map box選択されていないまたは、範囲外")
                if self.menu_edit.clicked_name == "goal":
                    try:
                        driver.map[driver.rightclick_y][driver.rightclick_x] = 90
                        driver.goal_x = driver.rightclick_x
                        driver.goal_y = driver.rightclick_y
                    except:
                        print("map box選択されていないまたは、範囲外")
            if self.menu_view.clicked_index != -1:
                if self.menu_view.clicked_name == "variable view":
                    self.variable_view.visible = not self.variable_view.visible
            for traffic in driver.traffic:
                traffic.update()
            self.variable_view.update()
    def draw(self, screen):
        if self.visible:
            self.driver_map.draw(screen)
            self.maps.draw(screen)
            
            for object in self.objects:
                object.draw(screen)
            
            self.variable_view.draw(screen)
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
    def update(self, main,screen):
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
                main.visible = True
                self.visible = False
                driver.create_map()
                screen = None
                main.createflag = True
                screen = pg.display.set_mode((var.WINDWONSIZE_X, var.WINDWONSIZE_Y))
            if self.box_cancel.clicked:
                main.visible = True
                self.visible = False
                screen = pg.display.set_mode((var.WINDWONSIZE_X, var.WINDWONSIZE_Y))
    def draw(self, screen):
        if self.visible:
            for object in self.objects:
                object.draw(screen)
class VariableView:
    def __init__(self, rect, visible):
        self.rect = rect
        self.visible = visible
        self.texts = gui.Texts(pg.Rect(self.rect.x, self.rect.y, 12,12), ["map size : ", "car x : ", "car y : ", "car direction : ", "selectbox x : ", "selectbox y : "], var.FONT_SMALL, var.COLOR_INACTIVE,True,8,24)
    def update(self):
        self.texts.texts[0].text = "map size : " + str(driver.map_x)
        self.texts.texts[1].text = "car x : " + str(driver.x)
        self.texts.texts[2].text = "car y : " + str(driver.y)
        self.texts.texts[3].text = "car direction : " + str(driver.direction)
        self.texts.texts[4].text = "selectbox x : " + str(driver.select_box_x)
        self.texts.texts[5].text = "selectbox y : " + str(driver.select_box_y)

        self.texts.update()
    def draw(self, screen):
        if self.visible:
            self.texts.draw(screen)

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
        self.always = [self.menu_line]
        self.displays = [self.display_line, self.boxsize_display, self.boxspace_display]
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
    def update(self,mc):
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
                    var.save_boxspace(self.boxspace_display.inputbox.text, mc, driver)
                    var.save_boxsize(self.boxsize_display.inputbox.text, mc, driver)
                if self.window_tab.clicked_name == "close":
                    screen = pg.display.set_mode((var.WINDOWNSIZE_X, var.WINDOWNSIZE_Y))
                    mc.visible = True
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

# メイン処理関数   
def main():
    var.init_savedata()
    screen = pg.display.set_mode((var.WINDOWNSIZE_X, var.WINDOWNSIZE_Y))  
    clock = pg.time.Clock()
    main_scene = MainScene()   
    textbox_scene = TextBoxScene()
    setting_scene = SettingScene()
    done = False
    textboxsceneflag = False
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            main_scene.handle_event(event)
            textbox_scene.handle_event(event)
            setting_scene.handle_event(event)
        if main_scene.menu_file.clicked_index == 0:
            main_scene.visible = False
            setting_scene.visible = False
            textbox_scene.visible = True
            screen = pg.display.set_mode((580, 380))
            main_scene.menu_file.clicked_index = -1
        elif main_scene.menu_file.clicked_index == 3 or main_scene.menu_view.clicked_index == 0:
            main_scene.visible = False
            setting_scene.visible = True
            textbox_scene.visible = False
            screen = pg.display.set_mode((720, 480))
            if main_scene.menu_view.clicked_index == 0:
                setting_scene.visible_displays = True
                setting_scene.visible_datas = False
                setting_scene.visible_other = False
            main_scene.menu_file.clicked_index = -1
            main_scene.menu_view.clicked_index = -1
        elif main_scene.menu_file.clicked_index == 4:
            done = True
        main_scene.update()
        setting_scene.update(main_scene)
        textbox_scene.update(main_scene, screen)
        screen.fill((30, 30, 30))
        main_scene.draw(screen)
        textbox_scene.draw(screen)
        setting_scene.draw(screen)
        pg.display.flip()
        clock.tick(24)

if __name__ == '__main__':
    main()
    pg.quit()