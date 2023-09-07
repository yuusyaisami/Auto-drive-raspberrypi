import pygame as pg
from pygui import save as sa
save = sa.SaveText()
class Variables:
    def __init__(self):
        self.FONT = pg.font.Font(None, 32)
        self.FONT_SMALL = pg.font.Font(None, 24)
        self.FONT_SMALLEST = pg.font.Font(None, 12)
        self.COLOR_INACTIVE = pg.Color('lightskyblue3')
        self.COLOR_ACTIVE = pg.Color('dodgerblue2')
        self.COLOR_GOAL = pg.Color('gold')
        self.COLOR_START = pg.Color("white")
        self.COLOR_SELECT = pg.Color('blue')
        self.COLOR_BACK = pg.Color(30,30,30)
        self.COLOR_TRACK = pg.Color('dodgerblue')
        self.COLOR_NEXT = pg.Color('teal')
        self.WINDOWNSIZE_X = 1280
        self.WINDOWNSIZE_Y = 550
        
        self.TRAFFIC_SIZE = 6
        self.BOXSPACE = 32
        self.BOXSIZE = 20
    def init_savedata(self):
        self.BOXSIZE = save.search("BOXSIZE","save.txt", "int")
        self.BOXSPACE = save.search("BOXSPACE","save.txt", "int")
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
    def save_reset(self, mc, driver):
        self.save_boxspace(32, mc, driver)
        self.save_boxsize(20, mc, driver)
        pass