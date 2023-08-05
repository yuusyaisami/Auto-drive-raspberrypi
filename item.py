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
        self.remove_btn_count = 0
        self.Determined = False
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
class RightBar:
    def __init__(self, x, y, Textbtn):
        self.x = x
        self.y = y
        self.Active = True
        self.selected = False
        self.selected_index = -1
        self.color = COLOR_INACTIVE
        self.texts = []
        self.texts = Textbtn
        self.Textbtns = []
        self.timer = 0
        self.timerflag = False
        max_len = 0
        diff = 0
        for i in range(len(self.texts)):
            if max_len * 18< len(self.texts[i]) * 24:
                max_len = len(self.texts[i])  * 24
        if 450 < len(self.texts) * 24 + self.y:
            diff = len(self.texts) * 24 + self.y - 450
        f_y = len(self.texts) * -24 
        self.rect = pg.Rect(x + 10, y - diff,max_len,len(self.texts) * 24 + 5) 
        if f_y < 0:
            f_y = 0
        for i in range(len(self.texts)):
            self.Textbtns.append(TextButton(self.x + 10,self.y + i * 24 + f_y - diff, len(Textbtn[i]) * 24 + 5,24,self.texts[i] ,18))
    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                pass
            else:
                self.Active = False
        for text in self.Textbtns:
            text.handle_event(event)
    def update(self):
        for i in range(len(self.Textbtns)):
            if self.Textbtns[i].Determined:
                self.selected = True
                self.selected_index = i
                self.timerflag = True
                self.timer = 0
        if self.timerflag:
            self.timer += 1

            if self.timer == 2:
                self.selected = False
            self.Active = False
        for text in self.Textbtns:
            text.update()

    def draw(self, screen):
        pg.draw.rect(screen, pg.Color(30, 30, 30), self.rect, 0)
        pg.draw.rect(screen, self.color, self.rect, 2)
        for text in self.Textbtns:
            text.draw(screen)














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
        self.time = 0.2
        self.jamp = 18.0

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.Determined = True
                self.velocity = 0
                self.velocity -= self.jamp

    def update(self):
        if self.Determined:
            self.velocity += 9.8 * self.time
            self.rect.y += self.velocity
            if self.default_y < self.rect.y:
                self.Determined = False
                self.rect.x = self.default_x
                self.rect.y = self.default_y
                self.velocity = 0
            
    def draw(self, screen):
        screen.blit(self.image, (int(self.rect.x), int(self.rect.y)))
    def collision(self, x, y, w, h):
        return (((self.rect.x < x and self.rect.w + self.rect.x > x) or (self.rect.x < x + w and self.rect.w + self.rect.x > x + w)) and 
                ((self.rect.y < y and self.rect.y + self.rect.h > y) or (self.rect.y < y + h and self.rect.y + self.rect.h > y + h)) or 
                ((x < self.rect.x and x + w > self.rect.x) or (x < self.rect.x + self.rect.w and w + x > self.rect.x + self.rect.w)) and
                ((y < self.rect.y and y + h > self.rect.y) or (y < self.rect.y + self.rect.h and h + y > self.rect.y + self.rect.h)))
                
class Obstacle_Small:
    def __init__(self, x, y, w, h, f_x, e_x):
        self.rect = pg.Rect(x, y, w, h)
        self.f_x = f_x
        self.e_x = e_x
        self.color = pg.Color(132,171,192,255)
        self.color.a = 128
        self.rect.x = self.f_x
    def update(self, speed):
        self.rect.x -= speed

    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect, 0)
class Obstacle_jamp:
    def __init__(self, x, y, w, h, f_x, e_x):
        self.rect = pg.Rect(x, y, w, h)
        self.f_x = f_x
        self.e_x = e_x
        self.default_x = x
        self.default_y = y
        self.velocity = 0

        self.color = COLOR_INACTIVE
        self.time = 0
        self.rect.x = self.f_x
        self.r = random.randint(1, 30)
        self.time = self.r
    def update(self, speed):
        self.rect.x -= speed
        self.time += 1
        self.velocity += 9.8 * 0.1
        self.rect.y += self.velocity
        if self.default_y < self.rect.y:
            self.Determined = False
            self.rect.y = self.default_y
            self.velocity = 0
        if self.time % 30 - speed == 0:
            self.velocity -= 6
    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect, 0)
class Obstacle_Medium:
    def __init__(self, x, y, w, h, f_x, e_x):
        self.rect = pg.Rect(x, y - 10, w, h + 10)
        self.f_x = f_x
        self.e_x = e_x
        self.color = COLOR_INACTIVE
        self.rect.x = self.f_x
    def update(self, speed):
        self.rect.x -= speed

    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect, 0)
class Obstacle_Large:
    def __init__(self, x, y, w, h, f_x, e_x):
        self.rect = pg.Rect(x, y - 20, w, h + 20)
        self.f_x = f_x
        self.e_x = e_x
        self.color = COLOR_INACTIVE
        self.rect.x = self.f_x
    def update(self, speed):
        self.rect.x -= speed

    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect, 0)
class Obstacle_Wide:
    def __init__(self, x, y, w, h, f_x, e_x):
        self.rect = pg.Rect(x, y, w + 10, h)
        self.f_x = f_x
        self.e_x = e_x
        self.color = COLOR_INACTIVE
        self.rect.x = self.f_x
    def update(self, speed):
        self.rect.x -= speed

    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect, 0)
class Obstacle_Super_Wide:
    def __init__(self, x, y, w, h, f_x, e_x):
        self.rect = pg.Rect(x, y, w + 30, h)
        self.f_x = f_x
        self.e_x = e_x
        self.color = COLOR_INACTIVE
        self.rect.x = self.f_x
    def update(self, speed):
        self.rect.x -= speed

    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect, 0)
class Obstacle_Super_High:
    def __init__(self, x, y, w, h, f_x, e_x):
        self.rect = pg.Rect(x, y - 40, w, h + 40)
        self.f_x = f_x
        self.e_x = e_x
        self.color = COLOR_INACTIVE
        self.rect.x = self.f_x
    def update(self, speed):
        self.rect.x -= speed

    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect, 0)
class Obstacle_Ghost:
    def __init__(self, x, y, w, h, f_x, e_x):
        self.rect = pg.Rect(x, y - 40, w, h + 39)
        self.f_x = f_x
        self.e_x = e_x
        self.color = pg.Color(132,171,192,255)
        self.rect.x = self.f_x
        self.timer = 254
        self.changeflag = True
    def update(self, speed):
        self.rect.x -= speed
        if self.changeflag:
            self.timer += 1
            self.color = pg.Color(self.timer,self.timer,self.timer,self.timer)
            if self.timer == 255:
                self.changeflag = not self.changeflag
        elif not self.changeflag:
            self.timer -= 1
            self.color = pg.Color(self.timer,self.timer,self.timer,self.timer)
            if self.timer == 30:
                self.changeflag = not self.changeflag
    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect, 0)
class Obstacle_Super_fly:
    def __init__(self, x, y, w, h, f_x, e_x):
        self.rect = pg.Rect(x, y, w + 100, h)
        self.f_x = f_x
        self.e_x = e_x
        self.color = COLOR_INACTIVE
        self.rect.x = self.f_x
    def update(self, speed):
        self.rect.x -= speed

    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect, 0)
class Obstacle_Super_cube:
    def __init__(self, x, y, w, h, f_x, e_x):
        self.rect = pg.Rect(x, y - 40, w + 40, h + 40)
        self.f_x = f_x
        self.e_x = e_x
        self.color = COLOR_INACTIVE
        self.rect.x = self.f_x
    def update(self, speed):
        self.rect.x -= speed

    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect, 0)
class Obstacle_Super_jamp:
    def __init__(self, x, y, w, h, f_x, e_x):
        self.rect = pg.Rect(x, y, w, h)
        self.f_x = f_x
        self.e_x = e_x
        self.default_x = x
        self.default_y = y
        self.velocity = 0

        self.color = COLOR_INACTIVE
        self.time = 0
        self.rect.x = self.f_x
        self.r = random.randint(1, 30)
        self.time = self.r
    def update(self, speed):
        self.rect.x -= speed
        self.time += 1
        self.velocity += 9.8 * 0.4
        self.rect.y += self.velocity
        if self.default_y < self.rect.y:
            self.Determined = False
            self.rect.y = self.default_y
            self.velocity = 0
        if self.time % 8== 0:
            self.velocity -= 24
    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect, 0)
