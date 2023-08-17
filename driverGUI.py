from pygui import gui
import pygame as pg
import driver as dr
import variables as vr
var = vr.Variables()
driver = dr.Driver(1,4,0)
pg.init()
screen = pg.display.set_mode((1280, 880))
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
        pass
    def handle_event(self, event):
        pass
    def update(self, mainscene):
        if mainscene.menu_file.clicked_index != -1:
            pass
        #--------------------------------------------------自動走行処理--------------------------------------------------

    
    def draw(self, screen):
        pass
# 大まかな処理のクラス
class MainScene:
    def __init__(self):
        self.visible = True
        self.visible_handle_event_and_update = True
        self.createmap_flag = False
        self.createmap_range = [9,9]
        self.menu_file = gui.Menubar(pg.Rect(20,10,42,32),"file",["new create","save", "name save", "setting", "close Windows"],var.FONT,True,False,32,170,var.COLOR_INACTIVE,var.COLOR_ACTIVE,var.COLOR_ACTIVE,True, True)
        self.menu_edit = gui.Menubar(pg.Rect(80,10,48,32),"edit",["road","wall", "start", "goal", "traffic add", "up/down traffic add", "all traffic add", "traffic delete"],var.FONT,True,False,32,210,var.COLOR_INACTIVE,var.COLOR_ACTIVE,var.COLOR_ACTIVE,True, True)
        self.menu_view = gui.Menubar(pg.Rect(140,10,55,32),"view",["theme","variable view", "variable editer"],var.FONT,True,False,32,170,var.COLOR_INACTIVE,var.COLOR_ACTIVE,var.COLOR_ACTIVE,True, True)
        self.run_button = gui.Button(pg.Rect(1200,10,48,32),"Run",var.FONT,True,var.COLOR_INACTIVE,var.COLOR_ACTIVE,var.COLOR_INACTIVE,True)
        self.menu_line = gui.Line(pg.Rect(0, 50,0,0),pg.Rect(1280,50,0,0),True,3)
        self.driver_map = DriverMap()
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
    def draw(self, screen):
        if self.visible:
            for object in self.objects:
                object.draw(screen)
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
                screen = None
                screen = pg.display.set_mode((1280, 880))
    def draw(self, screen):
        if self.visible:
            for object in self.objects:
                object.draw(screen)
# メイン処理関数
def main():
    clock = pg.time.Clock()
    main_scene = MainScene()
    textbox_scene = TextBoxScene()
    done = False
    screen1 = None
    textboxsceneflag = False
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            main_scene.handle_event(event)
            textbox_scene.handle_event(event)
        if main_scene.menu_file.clicked_index == 0:
            main_scene.visible = False
            textbox_scene.visible = True
            screen1 = pg.display.set_mode((580, 380))
            main_scene.menu_file.clicked_index = -1
        main_scene.update()
        textbox_scene.update(main_scene, screen1)
        screen.fill((30, 30, 30))
        main_scene.draw(screen)
        textbox_scene.draw(screen1)
        pg.display.flip()
        clock.tick(24)

if __name__ == '__main__':
    main()
    pg.quit()