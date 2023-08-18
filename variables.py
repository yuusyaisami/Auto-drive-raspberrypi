import pygame as pg
class Variables:
    def __init__(self):
        self.FONT = pg.font.Font(None, 32)
        self.COLOR_INACTIVE = pg.Color('lightskyblue3')
        self.COLOR_ACTIVE = pg.Color('dodgerblue2')
        self.COLOR_GOAL = pg.Color('gold')
        self.COLOR_START = pg.Color("white")
        self.COLOR_SELECT = pg.Color('blue')
        self.COLOR_BACK = pg.Color(30,30,30)