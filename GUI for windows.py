import pygame as pg
import driver as dr
import time
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

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # ユーザーがButton rectをクリックした場合。
            if self.rect.collidepoint(event.pos):
                self.Determined = True
                self.remove_btn_count = 10
                self.color = COLOR_ACTIVE
    def update(self):
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

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # ユーザーがButton rectをクリックした場合。
            if self.rect.collidepoint(event.pos):
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

    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.active = False
        self.Determined = ""

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
        self.default = text
        self.txt_surface = pg.font.Font(None, size).render(text, True, self.color)
        self.active = False
    def update(self, text):
        if text == None:
            self.text = self.default
        else:
            self.text = text
    def draw(self, screen):
        # テキストを吹き飛ばす。
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
class DriverMapBox:
    def __init__(self, x, y, w, h ,text = ''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.colorS = pg.Color("white")
        self.colorG = pg.Color(128,128,0)
        self.box_status = 1
        self.text = text
    def update(self, Status):
        if Status == 99:
            self.box_status = 0
            self.color = COLOR_INACTIVE
        elif Status == 90:
            self.box_status = 1
            self.color = self.colorG
        elif Status == 80:
            self.box_status = 1
            # 薄い青
            self.color = COLOR_ACTIVE
        elif Status == 1:
            self.box_status = 1
            self.color = self.colorS
        else:
            self.box_status = 1
            self.color = COLOR_INACTIVE
    def draw(self, screen):
        # テキストを吹き飛ばす。
        screen.blit(FONT.render(self.text, True, self.color), (self.rect.x + 5, self.rect.y + 5))
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
                self.DrBoxs[y][x] = DriverMapBox(self.rect.x + x * 30, self.rect.y + y * 30, 20, 20)
        self.Traffics = [Traffic(self.rect.x + 1 * 30, self.rect.y + 1 * 30,120, 120 ,3, 1, 1, 120),Traffic(self.rect.x + 1 * 30, self.rect.y + 1 * 30,120, 120, 0, 1, 1),
                         Traffic(self.rect.x + 3 * 30, self.rect.y + 3 * 30, 60,  60, 1, 3, 3),     Traffic(self.rect.x + 3 * 30, self.rect.y + 3 * 30, 60,  60, 2, 3, 3, 60),
                         Traffic(self.rect.x + 3 * 30, self.rect.y + 3 * 30, 60,  60, 3, 3, 3),     Traffic(self.rect.x + 3 * 30, self.rect.y + 3 * 30, 60,  60, 0, 3, 3, 60)]
        self.map[driver.y][driver.x] = 1
    def update(self, run, gx, gy):
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
            if self.animationcount % 20 == 0:
                self.TrafficStop()
                self.map, driver.x, driver.y, direction, driver.direction = shorter.DriverDirection(self.map, driver)
                if direction == -2:
                    self.map[driver.y][driver.x] = 1
                    self.animation = False
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
                
    def search_traffic(self, x , y, direction):
        for index in range(len(self.Traffics)):
            if self.Traffics[index].map_x == x and self.Traffics[index].map_y == y and self.Traffics[index].traffic_direction == direction:
                return index
    def TrafficStop(self):
        if self.map[driver.y - 1][driver.x] == 90 and driver.direction == 0:
            nowtraffic = self.search_traffic(driver.x , driver.y - 1, driver.direction)
            if nowtraffic != None:
                if self.Traffics[nowtraffic].statue == 1:
                    while True:
                        for traffic in self.Traffics:
                                traffic.update()
                        time.sleep(0.036)
                        if self.Traffics[nowtraffic].statue == 0:
                            break
        if self.map[driver.y][driver.x + 1] == 90 and driver.direction == 1:
            nowtraffic = self.search_traffic(driver.x + 1 , driver.y, driver.direction)
            if nowtraffic != None:
                if self.Traffics[nowtraffic].statue == 1:
                    while True:
                        for traffic in self.Traffics:
                            traffic.update()
                        time.sleep(0.036)
                        if self.Traffics[nowtraffic].statue == 0:
                            break
        if self.map[driver.y + 1][driver.x] == 90 and driver.direction == 2:
            nowtraffic = self.search_traffic(driver.x , driver.y + 1, driver.direction)
            if nowtraffic != None:
                if self.Traffics[nowtraffic].statue == 1:
                    while True:
                        for traffic in self.Traffics:
                                traffic.update()
                        time.sleep(0.036)
                        if self.Traffics[nowtraffic].statue == 0:
                            break
        if self.map[driver.y][driver.x - 1] == 90 and driver.direction == 3:
            nowtraffic = self.search_traffic(driver.x - 1 , driver.y, driver.direction)
            if nowtraffic != None:
                if self.Traffics[nowtraffic].statue == 1:
                    while True:
                        for traffic in self.Traffics:
                                traffic.update()
                        time.sleep(0.036)
                        if self.Traffics[nowtraffic].statue == 0:
                            break

        


def main():


    clock = pg.time.Clock()

    carediter_image = pg.transform.scale(pg.image.load("ImageFile/carediter.png"), (60, 30))
    mapediter_image = pg.transform.scale(pg.image.load("ImageFile/mapediter.png"), (30, 30))
    optionediter_image = pg.transform.scale(pg.image.load("ImageFile/optionediter.png"), (40, 35))

    clicked_carediter_image = pg.transform.scale(pg.image.load("ImageFile/clicked_carediter.png"), (60, 30))
    clicked_mapediter_image = pg.transform.scale(pg.image.load("ImageFile/clicked_mapediter.png"), (30, 30))
    clicked_optionediter_image = pg.transform.scale(pg.image.load("ImageFile/clicked_optionediter.png"), (40, 35))

    carediter = ButtonImage(630, 100, 60,30,carediter_image,clicked_carediter_image)
    mapediter = ButtonImage(630, 150, 30,30,mapediter_image,clicked_mapediter_image)
    optionediter = ButtonImage(630, 200, 40,34,optionediter_image,clicked_optionediter_image)


    input_x = InputBox(20, 40, 100, 32)
    input_y = InputBox(250, 40, 100, 32)
    btn_run = Button(500, 40, 54, 32, "Run")
    option_run = ButtonSwitching(580, 40, 84, 32, "Option")
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
            if option_run.Determined:
                for om in optionmenu:
                    om.handle_event(event)




        driver_map.update(btn_run.Determined, input_x.text, input_y.text)
        if option_run.Determined:
            for om in optionmenu:
                om.update()
        for box in input_boxes:
            box.update()
        for text in text_lines:
            text.update(None)
        for btn in btns:
            btn.update()
        screen.fill((30, 30, 30))
        if option_run.Determined:
            for om in optionmenu:
                om.draw(screen)
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