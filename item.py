import pygame as pg
import random

pg.init()
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
FONT = pg.font.Font(None, 32)
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
class ButtonGravity:
    def __init__(self, x, y, w, h, image):
        self.rect = pg.Rect(x, y, w, h)
        self.default_x = x
        self.default_y = y
        self.image = image
        self.notclicked_image = image
        self.active = False
        self.Determined = False
        self.velocity = 0
        self.rotate = 0

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # ユーザーがButton rectをクリックした場合。
            if self.rect.collidepoint(event.pos):
                self.Determined = True
                self.velocity -= 20
                rotate = random.randint(0,20)
                self.rotate += rotate

    def update(self):
        if self.Determined:
            self.velocity += 9.8 * 0.2
            self.rect.y += self.velocity
            self.rotate += 1
            self.image = pg.transform.rotate(self.image,self.rotate)
        if self.velocity > 15:
            self.Determined = False
            self.rect.x = self.default_x
            self.rect.y = self.default_y
            self.image = pg.transform.rotate(self.image,0)
            
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))