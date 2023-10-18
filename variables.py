import pygame as pg
import save as sa
save = sa.SaveText()
pg.init()
class Variables:
    def __init__(self):
        self.FONT = pg.font.Font(None, 32)
        self.FONT_SMALL = pg.font.Font(None, 24)
        self.FONT_SMALLEST = pg.font.Font(None, 12)
        self.COLOR_INACTIVE = pg.Color('lightskyblue3')
        self.COLOR_ACTIVE = pg.Color('dodgerblue2')
        self.COLOR_ACTIVE2 = pg.Color('dodgerblue')
        self.COLOR_GOAL = pg.Color('gold')
        self.COLOR_START = pg.Color("white")
        self.COLOR_SELECT = pg.Color('blue')
        self.COLOR_BACK = pg.Color(30,30,30)
        self.COLOR_TRACK = pg.Color('dodgerblue')
        self.COLOR_NEXT = pg.Color(0, 128, 128)
        self.WINDOWNSIZE_X = 780
        self.WINDOWNSIZE_Y = 550
        
        self.TRAFFIC_TIME = 60
        self.TRAFFIC_SIZE = 6
        self.BOXSPACE = 32
        self.BOXSIZE = 20
        self.BOX_X = 9
        self.BOX_Y = 9
    def init_savedata(self):
        self.BOXSIZE = save.search("BOXSIZE","save.txt", "int")
        self.BOXSPACE = save.search("BOXSPACE","save.txt", "int")
        self.TRAFFIC_TIME = save.search("TRAFFIC_TIME", "save.txt", "int")
        self.map_y = save.search("BOX_Y","save.txt", "int")
        self.map_x = save.search("BOX_X","save.txt", "int")
    def save_boxsize(self, value, mc, driver):
        try:
            if int(value) > 0:
                save.add("BOXSIZE", value, "save.txt")
                mc.maps.size= int(value)
                for y in range(driver.map_x):
                    for x in range(driver.map_y):
                        mc.maps.mapbox[y][x].rect.w = int(value)
                        mc.maps.mapbox[y][x].rect.h = int(value)
        except:
            print("fail")
            pass
    def save_box(self, x, y):
            if int(x) > 0 and int(y) > 0:
                save.add("BOX_X", int(x), "save.txt")
                save.add("BOX_Y", int(y), "save.txt")
                self.BOX_X = int(x)
                self.BOX_Y = int(y)
    def save_boxspace(self, value, mc, driver):
        try:
            if int(value) > 0:
                save.add("BOXSPACE", value, "save.txt")
                
                mc.maps.width = int(value)
                for y in range(driver.map_x):
                    for x in range(driver.map_y):
                        mc.maps.mapbox[y][x].rect.y = mc.maps.rect.y + y * int(value)
                        mc.maps.mapbox[y][x].rect.x = mc.maps.rect.x + x * int(value)
        except:
            pass
    def save_signal_switching_time(self, value):
        try:
            if int(value) > 0:
                save.add("TRAFFIC_TIME", value, "save.txt")
                self.TRAFFIC_TIME = int(value)
        except:
            pass
    def save_reset(self, mc, driver):
        self.save_boxspace(32, mc, driver)
        self.save_boxsize(20, mc, driver)
        pass
variable = Variables()