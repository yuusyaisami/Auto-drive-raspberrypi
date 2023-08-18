from pygui import gui
import pygame as pg
import driver as dr
import variables as vr
import numpy as np
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
pg.init()
pg.display.set_caption("drivers")
# ウィンドウのアイコンを設定
icon_image = pg.image.load("icon.png")  # アイコンとして使用する画像をロード
pg.display.set_icon(icon_image)
# 箱
class DriverMapBox:
    def __init__(self):
        pass
    def handle_event(self, event):
        pass
    def update(self, mainscene):
        pass
    def draw(self, screen):
        pass
# 自動走行のクラス
class DriverMap:
    def __init__(self):
        self.run = False
    def handle_event(self, event):
        pass
    def update(self, mainscene):
        if mainscene.menu_file.clicked_index != -1:
            pass
        if mainscene.menu_edit.clicked_index != -1:
            pass
        #--------------------------------------------------自動走行処理--------------------------------------------------
        if mainscene.run_button.clicked:
            self.run = True
        if self.run:
            pass
    
    def draw(self, screen):
        pass
class Maps:
    def __init__(self, rect, size, width):
        self.rect = rect
        self.size = size
        self.width = width
        self.mapbox = []
        self.row = []
        for y in range(driver.map_y):
            for x in range(driver.map_x):
                self.row.append(DriverMapBox(pg.Rect(self.rect.x + x * size,self.rect.y + y * size, self.width, self.width),x,y))
            self.mapbox.append(self.row)
            self.row = []
        pass
    def handle_event(self, event):
        pass
    def update(self, mc):
        if mc.createflag:
            self.mapbox = []
            self.row = []
            for y in range(driver.map_y):
                for x in range(driver.map_x):
                    self.row.append(DriverMapBox(pg.Rect(self.rect.x + x * self.size,self.rect.y + y * self.size, self.width, self.width),x,y))
                self.mapbox.append(self.row)
                self.row = []
        for y in range(len(self.mapbox)):
            for x in range(len(self.mapbox[0])):
                self.mapbox[y][x].update(mc)
    def draw(self, screen):
        for y in range(len(self.mapbox)):
            for x in range(len(self.mapbox[0])):
                self.mapbox[y][x].draw(screen)
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

        self.visible = True
    def handle_event(self, event):
        if self.visible:
            if event.type == pg.MOUSEBUTTONDOWN:
                # ユーザーがinput_box rectをクリックした場合。
                if self.rect.collidepoint(event.pos):
                    pass
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
                self.color = self.color_goal
                self.width = 2

    def draw(self, screen):
        #テトラゴンは処理が重くなるからだめ
        # gui.tetragon(self.rect, self.color, self.width, 5, screen)
        pg.draw.rect(screen, self.color,self.rect, self.width)

# 大まかな処理のクラス
class MainScene:
    def __init__(self):
        self.createflag = False
        self.visible = True
        self.visible_handle_event_and_update = True
        self.createmap_flag = False
        self.createmap_range = [9,9]
        self.menu_file = gui.Menubar(pg.Rect(20,10,42,32),"file",["new create","save", "name save", "setting", "close Window"],var.FONT,True,False,32,170,var.COLOR_INACTIVE,var.COLOR_ACTIVE,var.COLOR_ACTIVE,True, True)
        self.menu_edit = gui.Menubar(pg.Rect(80,10,48,32),"edit",["road","wall", "start", "goal", "traffic add", "up/down traffic add", "all traffic add", "traffic delete"],var.FONT,True,False,32,210,var.COLOR_INACTIVE,var.COLOR_ACTIVE,var.COLOR_ACTIVE,True, True)
        self.menu_view = gui.Menubar(pg.Rect(140,10,55,32),"view",["theme","variable view", "variable editer"],var.FONT,True,False,32,170,var.COLOR_INACTIVE,var.COLOR_ACTIVE,var.COLOR_ACTIVE,True, True)
        self.run_button = gui.Button(pg.Rect(1200,10,48,32),"Run",var.FONT,True,var.COLOR_INACTIVE,var.COLOR_ACTIVE,var.COLOR_INACTIVE,True)
        self.menu_line = gui.Line(pg.Rect(0, 50,0,0),pg.Rect(1280,50,0,0),True,3)
        self.driver_map = DriverMap()
        self.maps = Maps(pg.Rect(20,100,32,32),32,20)
        self.objects = [self.menu_line,self.menu_file,self.menu_edit,self.menu_view, self.run_button] 
    def handle_event(self, event):
        if self.visible and self.visible_handle_event_and_update:
            for object in self.objects:
                object.handle_event(event)
            self.driver_map.handle_event(event)
    def update(self):
        if self.visible and self.visible_handle_event_and_update:
            for object in self.objects:
                object.update()
            self.driver_map.update(self)
            self.maps.update(self)
            self.createflag = False
    def draw(self, screen):
        if self.visible:
            self.driver_map.draw(screen)
            self.maps.draw(screen)
            for object in self.objects:
                object.draw(screen)
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
                screen = pg.display.set_mode((1280, 880))
            if self.box_cancel.clicked:
                main.visible = True
                self.visible = False
                screen = pg.display.set_mode((1280, 880))
    def draw(self, screen):
        if self.visible:
            for object in self.objects:
                object.draw(screen)
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
        self.always = [self.menu_line]
        self.displays = [self.display_line]
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
                if self.window_tab.clicked_name == "save":
                    pass
                if self.window_tab.clicked_name == "close":
                    screen = pg.display.set_mode((1280, 880))
                    mc.visible = True
                    self.visible = False
            self.setting_tab.update()
            self.window_tab.update()
            if self.visible_always:
                for al in self.always:
                    al.update()
            if self.visible_displays:
                for di in self.displays:
                    di.update()
            if self.visible_datas:
                for da in self.datas:
                    da.update()
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
    screen = pg.display.set_mode((1280, 880))  
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