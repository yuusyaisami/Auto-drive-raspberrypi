import pygame as pg
import driver as dr
import time
import constant as cs
driver = dr.Driver(1,4,0)
shorter = dr.MazeShortest()
pg.init()
screen = pg.display.set_mode((740, 480))
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
FONT = pg.font.Font(None, 32)
pg.display.set_caption("drivers")
# ウィンドウのアイコンを設定
icon_image = pg.image.load("icon.png")  # アイコンとして使用する画像をロード
cs.TRAFFIC_TIMES = 60
pg.display.set_icon(icon_image)



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
    def __init__(self, x, y, time, redtime, direction, map_x, map_y, count = 0):
        self.rect = pg.Rect(x, y, 6, 6)
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
    def update(self):
        self.count = self.count + 1
        if self.count > self.time + self.redtime:
            self.statue = 0
            self.count = 0
            self.color = pg.Color('green')
        elif self.count > self.time:
            self.statue = 1
            self.color = pg.Color('red')
    def draw(self, screen):
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
        pg.draw.rect(screen, self.color, self.rect, 0)
        
class Button:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.active = False
        self.Determined = False
        self.remove_btn_count = 0
        self.forcing_run = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # ユーザーがButton rectをクリックした場合。
            if self.rect.collidepoint(event.pos):
                self.forcing_run = False
                self.Determined = True
                self.remove_btn_count = 10
                self.color = COLOR_ACTIVE
    def update(self):
        if self.forcing_run:
            self.forcing_run = False
            self.Determined = True
            self.remove_btn_count = 10
            self.color = COLOR_ACTIVE
        if self.remove_btn_count == 8:
            self.Determined = False
        if self.remove_btn_count >= 0:
            self.remove_btn_count = self.remove_btn_count - 1
        else:
            self.color = COLOR_INACTIVE
            self.Determined = False
    def draw(self, screen):
        screen.blit(FONT.render(self.text, True, self.color), (self.rect.x + 5, self.rect.y + 5))
        pg.draw.rect(screen, self.color, self.rect, 2)

class ButtonSwitching:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.active = False
        self.Determined = False
        self.remove_btn_count = 0
        self.forcing_run = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # ユーザーがButton rectをクリックした場合。
            if self.rect.collidepoint(event.pos):
                self.forcing_run = False
                if(self.Determined):
                    self.Determined = False
                elif(not self.Determined):
                    self.Determined = True
                self.remove_btn_count = 10
                self.color = COLOR_ACTIVE
    def update(self):
        if self.remove_btn_count >= 0:
            self.remove_btn_count = self.remove_btn_count - 1
        else:
            self.color = COLOR_INACTIVE
    def draw(self, screen):
        screen.blit(FONT.render(self.text, True, self.color), (self.rect.x + 5, self.rect.y + 5))
        pg.draw.rect(screen, self.color, self.rect, 2)
class ButtonImage:
    def __init__(self, x, y, w, h, image, clicked_image):
        self.rect = pg.Rect(x, y, w, h)
        self.image = image
        self.clicked_image = clicked_image
        self.notclicked_image = image
        self.active = False
        self.Determined = False
        self.remove_btn_count = 0

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # ユーザーがButton rectをクリックした場合。
            if self.rect.collidepoint(event.pos):
                self.Determined = True
                self.remove_btn_count = 10
                self.image = self.clicked_image
    def update(self):
        if self.remove_btn_count == 8:
            self.Determined = False
        if self.remove_btn_count >= 0:
            self.remove_btn_count = self.remove_btn_count - 1
        else:
            self.image = self.notclicked_image
            self.Determined = False
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
class InputBox:

    def __init__(self, x, y, w, h, text='', de = ""):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.active = False
        self.Determined = de

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # ユーザーがinput_box rectをクリックした場合。
            if self.rect.collidepoint(event.pos):
                # アクティブな変数を切り替える。
                self.active = not self.active
            else:
                self.active = False
            # 入力ボックスの現在の色を変更する。
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    self.Determined = self.text
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def update(self):
        # テキストが長すぎる場合は、ボックスのサイズを変更してください。
        width = max(200, FONT.render(self.text, True, self.color).get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # テキストを吹き飛ばす。
        screen.blit(FONT.render(self.text, True, self.color), (self.rect.x+5, self.rect.y+5))
        # レクトを吹き飛ばす。
        pg.draw.rect(screen, self.color, self.rect, 2)

class Text:
    def __init__(self, x, y, w, h, text='',size = 32):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.size = 32
        self.default = text
        self.active = False
        self.size = size
    def update(self, text = None):
        if text == None:
            self.text = self.default
        else:
            self.text = text
    def draw(self, screen):
        # テキストを吹き飛ばす。
        screen.blit(pg.font.Font(None, self.size).render(self.text, True, self.color), (self.rect.x+5, self.rect.y+5))
class TextButton:
    def __init__(self, x, y, w, h, text='',size = 32):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.default = text
        self.txt_surface = pg.font.Font(None, size).render(text, True, self.color)
        self.active = False
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

    def handle_event(self, event, Driver, gx, gy, run):
        if event.type == pg.MOUSEBUTTONDOWN:
            # ユーザーがButton rectをクリックした場合。
            if self.rect.collidepoint(event.pos):
                if event.button == 1:  # 左クリック
                    print("Left Click!" + " x : " +str(self.map_x) + "    y : " + str(self.map_y))
                    # クラスをアクティブにする
                    self.active = not self.active
                    self.color = self.selected_color

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
            
            

            
                

                

    def update(self, Status):
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
        for y in range(row):
            for x in range(column):
                self.DrBoxs[y][x] = DriverMapBox(self.rect.x + x * 30, self.rect.y + y * 30, 20, 20, x, y)
        self.Traffics = [Traffic(self.rect.x + 1 * 30, self.rect.y + 1 * 30,120, 120 ,3, 1, 1, 120),Traffic(self.rect.x + 1 * 30, self.rect.y + 1 * 30,120, 120, 0, 1, 1),
                         Traffic(self.rect.x + 3 * 30, self.rect.y + 3 * 30, 60,  60, 1, 3, 3),     Traffic(self.rect.x + 3 * 30, self.rect.y + 3 * 30, 60,  60, 2, 3, 3, 60),
                         Traffic(self.rect.x + 3 * 30, self.rect.y + 3 * 30, 60,  60, 3, 3, 3),     Traffic(self.rect.x + 3 * 30, self.rect.y + 3 * 30, 60,  60, 0, 3, 3, 60)]
        self.map[driver.y][driver.x] = 1
    def update(self, run, gx, gy):
        #run btnが押されたとき一度だけ実行される
        try:
            if run:
                self.map = shorter.ResetMaze(self.map)
                self.map = shorter.MazeWaterValue(self.map, driver)
                self.map[int(gy)][int(gx)] = 98
                self.map, error = shorter.MazeShortestRoute(self.map, driver)
                self.animation = True
                self.animationcount = 0
                if error == 1:
                    print("error : 目的地に到達できません")
            if self.animation:
                self.animationcount = 1 + self.animationcount
                #車の移動を実行する
                if self.animationcount % 20 == 0:
                    stop = self.TrafficStop()
                    # 信号にかからなかったら実行する
                    if not stop:
                        self.map, driver.x, driver.y, direction, driver.direction = shorter.DriverDirection(self.map, driver)
                        # 移動が終わったら実行する
                        if direction == -2:
                            self.map[driver.y][driver.x] = 1
                            self.animation = False
                    elif stop:
                        self.animationcount = 19
        except:
            print("error")
        for y in range(self.row):
            for x in range(self.column):
                self.DrBoxs[y][x].update(self.map[y][x])
        for traffic in self.Traffics:
            traffic.update()
    def draw(self, screen):
        for y in range(self.row):
            for x in range(self.column):
                self.DrBoxs[y][x].draw(screen)
        for traffics in self.Traffics:
            traffics.draw(screen)
                
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
        self.car_direction = Text(500, 86, 100, 20, "car direction : 0", 24)
        self.input_cardirection = InputBox(500, 110, 60,32 ,str(0),str(0))
        self.tutorial_run = ButtonSwitching(675, 40, 24, 32, "T")
        self.text1 = Text(350, 120, 100, 20, "Goal     : G", 24)
        self.text2 = Text(350, 140, 100, 20, "Start     : S", 24)
        self.text3 = Text(350, 160, 100, 20, "Wall      : W", 24)
        self.text4 = Text(350, 180, 100, 20, "Road    : R", 24)
        self.text5 = Text(350, 220, 100, 20, "Traffic set                                          : T + Arrow", 24)
        self.text6 = Text(350, 240, 100, 20, "Traffic delete                                    : ctrl + x + Arrow", 24)
        self.text7 = Text(350, 260, 100, 20, "Traffic set Up/down or left/right  : ctrl + c + Arrow", 24)
        self.text8 = Text(350, 280, 100, 20, "Traffic set Up/down/left/right       : ctrl + v + Arrow", 24)


        traffic_time = Text(500, 150, 100, 20, "traffic time : 60", 24)
        input_traffic_time = InputBox(500, 174, 50,32,str(60),str(60))
        self.inputlist = [self.input_cardirection,input_traffic_time,self.tutorial_run ]
        self.textlist = [self.car_direction,traffic_time]
        self.Ttextlist = [self.text1,self.text2,self.text3,self.text4,self.text5,self.text6,self.text7,self.text8]
        self.DeterminedChange = self.input_cardirection.Determined

    def update(self):
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

        
    def draw(self, screen):
        for list in self.inputlist:
            list.draw(screen)
        for text in self.textlist:
            text.draw(screen)
        if self.tutorial_run.Determined:
            for text in self.Ttextlist:
                text.draw(screen)


    


def main():


    clock = pg.time.Clock()

    edit_tool = EditTool()

    carediter_image = pg.transform.scale(pg.image.load("ImageFile/carediter.png"), (40, 20))
    mapediter_image = pg.transform.scale(pg.image.load("ImageFile/mapediter.png"), (35, 33))
    optionediter_image = pg.transform.scale(pg.image.load("ImageFile/optionediter.png"), (38, 33))

    clicked_carediter_image = pg.transform.scale(pg.image.load("ImageFile/clicked_carediter.png"), (40, 20))
    clicked_mapediter_image = pg.transform.scale(pg.image.load("ImageFile/clicked_mapediter.png"), (35, 33))
    clicked_optionediter_image = pg.transform.scale(pg.image.load("ImageFile/clicked_optionediter.png"), (38, 33))

    carediter = ButtonImage(630, 110, 40,20,carediter_image,clicked_carediter_image)
    mapediter = ButtonImage(630, 150, 35,33,mapediter_image,clicked_mapediter_image)
    optionediter = ButtonImage(630, 200, 38,33,optionediter_image,clicked_optionediter_image)


    input_x = InputBox(20, 40, 100, 32)
    input_y = InputBox(250, 40, 100, 32)






    btn_run = Button(500, 40, 54, 32, "Run")
    option_run = ButtonSwitching(573, 40, 84, 32, "Option")
    optionmenu = [carediter,mapediter,optionediter]
    btns = [btn_run, option_run]
    input_boxes = [input_x, input_y]
    text_lines = []
    for a in range(len(map[0])):
        text_lines.append(Text(40 + a * 30, 98, 10, 10, str(a), 24))
    for a in range(len(map)):
        text_lines.append(Text(20, 118 + a * 30, 10, 10, str(a), 24))

    text_ornament_x = Text(20, 10, 100, 20, "X")
    text_ornament_y = Text(250, 9, 100, 20, "Y")
    driver_map = DriverMap(40,120,len(map[0]),len(map),map)
    text_lines.append(text_ornament_x)
    text_lines.append(text_ornament_y)
    done = False

    goal_x = 0
    goal_y = 0
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
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
        driver_map.update(btn_run.Determined, input_x.text, input_y.text)
        for box in input_boxes:
            box.update()
        for text in text_lines:
            text.update(None)
        for btn in btns:
            btn.update()
        screen.fill((30, 30, 30))
        if option_run.Determined:
            edit_tool.draw(screen)
        driver_map.draw(screen)
        for box in input_boxes:
            box.draw(screen)
        for text in text_lines:
            text.draw(screen)
        for btn in btns:
            btn.draw(screen)

        pg.display.flip()
        clock.tick(24)


if __name__ == '__main__':
    main()
    pg.quit()