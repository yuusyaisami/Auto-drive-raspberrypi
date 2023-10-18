# クラスは updateとdraw関数 handle_eventがあります
# updateはオブジェクトのメイン処理
# drawは描写
# handle_eventはeventについての処理(主にユーザーの操作)です

# 処理は繰り返し処理の中に入れてください
# (例)
# import pygame as pg
# import gui #このguiモジュールをインポートしてくださいまたは, from pygui import guiを入力してください
# pg.init()
# screen = pg.display.set_mode((740, 480))
# done = False
# btn = Button(pg.Rect(10,10,100,100))
# while not done:
#     for event in pg.event.get():
#         if event.type == pg.QUIT:
#             done = True
#         btn.handle_event(event)
#     btn.update()
#     screen.fill((30, 30, 30))
#     btn.draw(screen)
#     pg.display.flip()
# pg.quit()
# 複数オブジェクトがあるときはlistにオブジェクトのインスタンスを宣言し、関数を呼び出してください

import pygame as pg
import random
import numpy as np
import variables
var = variables.variable
pg.init() # pygame initialize

# button
class Button: # ただのボタン
    def __init__(self, rect = pg.Rect(0,0,0,0), text = "", font = var.FONT,visible = True, color_inactive = var.COLOR_INACTIVE, color_active = var.COLOR_ACTIVE, color_on_mouse = var.COLOR_INACTIVE, NoFrame = False):
        self.rect = rect
        self.b_d_c = color_inactive #決定する前のいろ
        self.a_d_c = color_active # 決定した後の色
        self.o_c_c = color_on_mouse # マウスがオブジェクトの上にあるときのオブジェクトの色
        self.color = self.b_d_c
        self.text = text # オブジェクトの中のテキスト
        self.forcing_run = False # 強制的に決定する
        self.clicked = False # 決定されたとき1度trueになる (update関数が再び呼び出されるとFalseになる)
        self.btn_count = 0
        self.Font = font
        self.visible = visible
        self.NoFrame = NoFrame
        self.do_count = False
    def handle_event(self, event):
        if self.visible:
            if event.type == pg.MOUSEBUTTONDOWN:
                # ユーザーがButton rectをクリックした場合。
                if self.rect.collidepoint(event.pos):
                    self.forcing_run = False
                    self.clicked = True
                    self.do_count = True
                    self.btn_count = 10
                    self.color = self.a_d_c
            mouse_x, mouse_y = pg.mouse.get_pos()
            if self.rect.collidepoint(mouse_x, mouse_y):
                if not self.do_count:
                    self.color = self.o_c_c
            elif not self.do_count:
                self.color = self.b_d_c

    def update(self):
        if self.visible:
            if self.forcing_run: # handle_eventなしで決定
                self.forcing_run = False
                self.do_count = True
                self.btn_count = 10
                self.color = self.a_d_c
                self.clicked = True

            if self.btn_count == 9:
                self.clicked = False
            elif self.btn_count < 0:
                self.clicked = False
                self.do_count = False

            if self.do_count:
                self.btn_count -= 1
        self.b_d_c = var.COLOR_INACTIVE
        self.a_d_c = var.COLOR_ACTIVE
        self.o_c_c = var.COLOR_ACTIVE2
    def draw(self,screen):
        if self.visible:
            # pg.draw.rect(screen, self.color, self.rect, 3)
            if not self.NoFrame:
                tetragon(self.rect, self.color, 2, 5,screen)
            screen.blit(var.FONT.render(self.text, True, self.color), (self.rect.x+5, self.rect.y+5))
class ButtonSwitching: # スイッチ式のボタン
    def __init__(self, rect = pg.Rect(0,0,0,0), text = "",  font = var.FONT,text_rect = pg.Rect(0,0,0,0),visible = True, color_inactive = var.COLOR_INACTIVE, color_active = var.COLOR_ACTIVE, color_on_mouse = var.COLOR_INACTIVE):
        self.rect = rect
        self.b_d_c = color_inactive #決定する前のいろ
        self.a_d_c = color_active # 決定した後の色
        self.o_c_c = color_on_mouse # マウスがオブジェクトの上にあるときのオブジェクトの色
        self.color = self.b_d_c
        self.text = text # オブジェクトの中のテキスト
        self.forcing_run = False # 強制的に決定する
        self.clicked = False # 決定されたとき1度trueになる (update関数が再び呼び出されるとFalseになる)
        self.btn_count = 0
        self.text_rect = text_rect
        self.Font = font
        self.on_cursor = False
        self.visible = visible
        self.do_count = False
        self.frame = 3
    def handle_event(self, event):
        if self.visible:
            if event.type == pg.MOUSEBUTTONDOWN:
                # ユーザーがButton rectをクリックした場合。
                if self.rect.collidepoint(event.pos):
                    self.forcing_run = False
                    self.clicked = not self.clicked 
                    self.do_count = True
                    self.btn_count = 10
            mouse_x, mouse_y = pg.mouse.get_pos()
            if self.rect.collidepoint(mouse_x, mouse_y):
                self.color = self.o_c_c
                self.on_cursor = True
            else:
                self.on_cursor = False

    def update(self):
        if self.visible:
            if self.forcing_run: # handle_eventなしで決定
                self.forcing_run = False
                self.do_count = True
                self.btn_count = 10
                self.clicked = not self.clicked 

            elif self.btn_count < 0:
                self.do_count = False

            if self.do_count:
                self.btn_count -= 1
            if self.clicked:
                if not self.on_cursor :
                    self.color = self.a_d_c
            else :
                if not self.on_cursor :
                    self.color = self.b_d_c
        self.b_d_c = var.COLOR_INACTIVE
        self.a_d_c = var.COLOR_ACTIVE
        self.o_c_c = var.COLOR_ACTIVE2

    def draw(self,screen, width = 5):
        if self.visible:
            #pg.draw.rect(screen, self.color, self.rect, self.frame)
            tetragon(self.rect, self.color, self.frame, width,screen)
            screen.blit(self.Font.render(self.text, True, self.color), (self.text_rect.x, self.text_rect.y))
class Frame:
    def __init__(self, rect,visible = True, width = 5,color = pg.Color(30,30,30)):
        self.rect = rect
        self.color = color
        self.visible = visible
        self.width = width
    def handle_event(self, event):
        pass
    def update(self):
        pass
    def draw(self, screen):
        if self.visible:
            tetragon(self.rect, self.color, self.width, 5,screen)
class Line:
    def __init__(self, first_rect,end_rect,visible = True, width = 5,color = var.COLOR_INACTIVE):
        self.f_rect = first_rect
        self.e_rect = end_rect
        self.color = color
        self.visible = visible
        self.width = width
    def handle_event(self, event):
        pass
    def update(self):
        pass
    def draw(self, screen):
        if self.visible:
            self.color = var.COLOR_INACTIVE
            pg.draw.line(screen, self.color, (self.f_rect.x,self.f_rect.y),(self.e_rect.x, self.e_rect.y), self.width)
class ButtonImageSwitching: # 画像のボタン
    def __init__(self, rect , visible , before_clicked_image, after_clicked_image, on_cursor_image):
        self.rect = rect
        self.b_d_i = before_clicked_image #決定する前のいろ
        self.a_d_i = after_clicked_image # 決定した後の色
        self.o_c_i = on_cursor_image # マウスがオブジェクトの上にあるときのオブジェクトの色
        self.image = self.b_d_i
        self.forcing_run = False # 強制的に決定する
        self.clicked = False # 決定されたとき1度trueになる (update関数が再び呼び出されるとFalseになる)
        self.btn_count = 0
        self.visible = visible

        self.on_cursor = False
        self.do_count = False
    def handle_event(self, event):
        if self.visible:
            if event.type == pg.MOUSEBUTTONDOWN:
                # ユーザーがButton rectをクリックした場合。
                if self.rect.collidepoint(event.pos):
                    self.forcing_run = False
                    self.clicked = not self.clicked
                    self.do_count = True
                    self.btn_count = 10
                    self.image = self.a_d_i
            mouse_x, mouse_y = pg.mouse.get_pos()
            if self.rect.collidepoint(mouse_x, mouse_y):
                if not self.do_count:
                    self.on_cursor = True
                    self.image = self.o_c_i
            elif not self.do_count:
                self.on_cursor = False

    def update(self):
        if self.visible:
            if self.forcing_run: # handle_eventなしで決定
                self.forcing_run = False
                self.do_count = True
                self.btn_count = 10
                self.image = self.a_d_i
                self.clicked = not self.clicked
            elif self.btn_count < 0:
                self.do_count = False
            if self.do_count:
                self.btn_count -= 1
            if self.clicked:
                if not self.on_cursor:
                    self.image = self.a_d_i
            else :
                if not self.on_cursor:
                    self.image = self.b_d_i
        self.b_d_i = var.COLOR_INACTIVE
        self.a_d_i = var.COLOR_ACTIVE
        self.o_c_i = var.COLOR_ACTIVE2
    def draw(self,screen):
        if self.visible:
            screen.blit(self.image, (self.rect.x, self.rect.y))
class ButtonImage: # 画像のボタン
    def __init__(self, rect , visible , before_clicked_image, after_clicked_image, on_cursor_image):
        self.rect = rect
        self.b_d_i = before_clicked_image #決定する前のいろ
        self.a_d_i = after_clicked_image # 決定した後の色
        self.o_c_i = on_cursor_image # マウスがオブジェクトの上にあるときのオブジェクトの色
        self.image = self.b_d_i
        self.forcing_run = False # 強制的に決定する
        self.clicked = False # 決定されたとき1度trueになる (update関数が再び呼び出されるとFalseになる)
        self.btn_count = 0
        self.visible = visible

        self.do_count = False
    def handle_event(self, event):
        if self.visible:
            if event.type == pg.MOUSEBUTTONDOWN:
                # ユーザーがButton rectをクリックした場合。
                if self.rect.collidepoint(event.pos):
                    self.forcing_run = False
                    self.clicked = True
                    self.do_count = True
                    self.btn_count = 10
                    self.image = self.a_d_i
            mouse_x, mouse_y = pg.mouse.get_pos()
            if self.rect.collidepoint(mouse_x, mouse_y):
                if not self.do_count:
                    self.image = self.o_c_i
            elif not self.do_count:
                self.image = self.b_d_i

    def update(self):
        if self.visible:
            if self.forcing_run: # handle_eventなしで決定
                self.forcing_run = False
                self.do_count = True
                self.btn_count = 10
                self.image = self.a_d_i
                self.clicked = True
            if self.btn_count == 9:
                self.clicked = False
            elif self.btn_count < 0:
                self.do_count = False
                self.clicked = False
                self.image = self.b_d_i
            if self.do_count:
                self.btn_count -= 1
        self.b_d_i = var.COLOR_INACTIVE
        self.a_d_i = var.COLOR_ACTIVE
        self.o_c_i = var.COLOR_ACTIVE2
    def draw(self,screen):
        if self.visible:
            screen.blit(self.image, (self.rect.x, self.rect.y))
class InputBox:
    def __init__(self, rect, text='', font = var.FONT,  visible = True, clear_text = True, color_inactive = var.COLOR_INACTIVE, color_active = var.COLOR_ACTIVE, color_on_mouse = var.COLOR_INACTIVE ):
        self.rect = rect
        self.color = color_inactive
        self.color_inactive = color_inactive
        self.color_active = color_active
        self.color_on_mouse = color_on_mouse
        self.text = text
        self.active = False
        self.clicked = False
        self.clicked_text = text
        self.clear = clear_text
        self.Font = font
        self.visible = visible

    def handle_event(self, event):
        if self.visible:
            if event.type == pg.MOUSEBUTTONDOWN:
                # ユーザーがinput_box rectをクリックした場合。
                if self.rect.collidepoint(event.pos):
                    # アクティブな変数を切り替える。
                    self.active = not self.active
                    self.color = self.color_active
                else:
                    self.active = False
            mouse_x, mouse_y = pg.mouse.get_pos()
            if self.rect.collidepoint(mouse_x, mouse_y):
                if not self.active:
                    self.color = self.color_on_mouse
            else:
                if not self.active:
                    self.color = self.color_inactive

            if event.type == pg.KEYDOWN:
                if self.active:
                    if event.key == pg.K_RETURN:
                        self.clicked = True
                        self.clicked_text = self.text
                        if self.clear:
                            self.text = ""
                    elif event.key == pg.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        self.text += event.unicode

    def update(self):
        if self.visible:
            # テキストが長すぎる場合は、ボックスのサイズを変更してください。
            width = max(200, var.FONT.render(self.text, True, self.color).get_width()+10)
            self.rect.w = width
            self.color_inactive = var.COLOR_INACTIVE
            self.color_active = var.COLOR_ACTIVE
            self.color_on_mouse = var.COLOR_ACTIVE2
    def draw(self, screen):
        if self.visible:
            # テキストを吹き飛ばす。
            screen.blit(var.FONT.render(self.text, True, self.color), (self.rect.x+5, self.rect.y+5))
            self.clicked = False
            # レクトを吹き飛ばす。
            pg.draw.rect(screen, self.color, self.rect, 2)
class Text:
    def __init__(self, rect, text = "", font = var.FONT, visible = True, textcolor = var.COLOR_INACTIVE):
        self.rect = rect
        self.text = text
        self.font = font
        self.visible = visible
        self.color = textcolor
    def handle_event(self, event):
        pass
    def update(self):
        self.color_inactive = var.COLOR_INACTIVE
        self.color_active = var.COLOR_ACTIVE
        self.color_on_mouse = var.COLOR_ACTIVE2
        self.color = var.COLOR_INACTIVE
    def draw(self, screen):
        if self.visible:
            screen.blit(self.font.render(self.text, True, self.color), (self.rect.x+5, self.rect.y+5))

class CheckBox:
    def __init__(self, rect , text, font = var.FONT, visible = True, clicked = True, color = var.COLOR_INACTIVE, boxsize = 10):
        self.rect = rect
        self.text = text
        self.font = font
        self.color = color
        self.visible = visible
        self.clicked = clicked
        self.checkobject = ButtonSwitching(pg.Rect(self.rect.x + (self.rect.h / 3) - boxsize / 2,self.rect.y + (self.rect.h / 3) - boxsize / 2,boxsize,boxsize))
        if self.clicked:
            self.checkobject.forcing_run = True
    def handle_event(self, event):
        if self.visible:
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.checkobject.clicked = not self.checkobject.clicked
                    if self.checkobject.clicked:
                        self.checkobject.frame = 0
                    else:
                        self.checkobject.frame = 3
                    print(self.checkobject.clicked)
    def update(self):
        if self.visible:
            self.clicked = self.checkobject.clicked
    def draw(self, screen):
        if self.visible:
            screen.blit(self.font.render(self.text, True, self.color), (self.rect.x+26, self.rect.y))
            self.checkobject.draw(screen)
def circle(rect, radius ,first_rad , end_rad, color ,screen, points = 30, width = 5):
    # 半円を描画
    center_x = rect.x
    center_y = rect.y

    # 半円の点を生成
    angle_range = np.linspace(first_rad, end_rad, points)
    points = [(int(center_x + radius * np.cos(angle)), int(center_y + radius * np.sin(angle))) for angle in angle_range]
    if width == 0:
        pg.draw.polygon(screen, color, points)
    else :
        # 点同士を線でつなぐ
        pg.draw.lines(screen, color, False, points, width)
def tetragon(rect, color, width, radius, screen):
    if width == 0:
        pg.draw.rect(screen, color, pg.Rect(rect.x, rect.y + radius, rect.w, rect.h - radius * 2), width) # 横
        pg.draw.rect(screen, color, pg.Rect(rect.x + radius, rect.y, rect.w - radius - radius, rect.h), width) # 横

        circle(pg.Rect(rect.x + radius,rect.y + radius,rect.w,rect.h), radius, np.pi /32,np.pi * 2,color, screen,100, 0)
        circle(pg.Rect(rect.x - radius + rect.w ,rect.y + radius ,rect.w,rect.h), radius, np.pi /32,np.pi * 2 - np.pi /32 ,color, screen,100, 0)
        circle(pg.Rect(rect.x - radius + rect.w,rect.y + rect.h - radius ,rect.w - 2,rect.h), radius, np.pi /32, np.pi * 2 - np.pi /32,color, screen,100, 0)
        circle(pg.Rect(rect.x + radius,rect.y + rect.h - radius ,rect.w,rect.h), radius, np.pi /32, np.pi * 2,color, screen,100, 0)
    else:
        pg.draw.line(screen, color, (rect.x + radius, rect.y), (rect.x + rect.w - radius, rect.y), width)
        pg.draw.line(screen, color, (rect.x + rect.w, rect.y + radius), (rect.x + rect.w, rect.y + rect.h - radius), width)
        pg.draw.line(screen, color, (rect.x + radius - 2, rect.y + rect.h), (rect.x + rect.w - radius , rect.y + rect.h), width)
        pg.draw.line(screen, color, (rect.x, rect.y + radius), (rect.x, rect.y + rect.h - radius), width)
        circle(pg.Rect(rect.x + radius,rect.y + radius,rect.w,rect.h), radius, np.pi, np.pi + np.pi / 2,color, screen,100, width)
        circle(pg.Rect(rect.x - radius + rect.w + 1,rect.y + radius ,rect.w,rect.h), radius, np.pi + np.pi / 2,np.pi + np.pi - np.pi /32,color, screen,100, width)
        circle(pg.Rect(rect.x - radius + rect.w + 1,rect.y + rect.h - radius + 1 ,rect.w,rect.h), radius, np.pi /32, np.pi / 2,color, screen,100, width)
        circle(pg.Rect(rect.x + radius,rect.y + rect.h - radius + 1 ,rect.w,rect.h), radius, np.pi / 2 - np.pi /32, np.pi,color, screen,100, width)
# elements は 要素の名前を入れてください
# clicked_indexは選択されたインデックスが入ります、処理をもう一度通すと、-1(選択されていない)になります
class CombineBox:
    def __init__(self, rect, main_name, element_names, font = var.FONT, visible = True, clicked = False, size = 20,elementwidth = 100, color_inactive = var.COLOR_INACTIVE, color_active = var.COLOR_ACTIVE, color_on_mouse = var.COLOR_ACTIVE) -> None:
        self.rect = rect 
        self.main_name = main_name
        self.elements = element_names
        self.font = font
        self.visible = visible
        self.clicked = clicked
        self.clicked_index = -1
        self.color = var.COLOR_INACTIVE
        self.color_inactive = var.COLOR_INACTIVE
        self.color_active = var.COLOR_ACTIVE
        self.color_on_mouse = var.COLOR_ACTIVE2
        self.count_on_mouse = 0
        self.Boxvisible = False
        self.objects = []
        for i in range(len(self.elements)):
            self.objects.append(Button(pg.Rect(rect.x + rect.w + 6, rect.y + size * (i + 1) - size, elementwidth , rect.h),self.elements[i], self.font, True,color_inactive,color_active,color_on_mouse))
    def handle_event(self, event):
        if self.visible:
            if self.Boxvisible:
                for object in self.objects:
                        object.handle_event(event)
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.Boxvisible = not self.Boxvisible
                    self.count_on_mouse = 0
                    if self.Boxvisible:
                        self.color = self.color_active
                    else:
                        self.color = self.color_inactive
                else :
                    self.count_on_mouse = 0
                    self.Boxvisible = False
                    self.color = self.color_inactive
            mouse_x, mouse_y = pg.mouse.get_pos()
            if self.rect.collidepoint(mouse_x, mouse_y):
                self.color = self.color_on_mouse
                self.count_on_mouse += 3
            else :
                if not self.Boxvisible:
                    self.color = self.color_inactive
                    self.count_on_mouse = 0
    def update(self):
        if self.visible:
            if self.Boxvisible:
                for object in self.objects:
                    object.update()
            self.clicked_index = -1
            if self.count_on_mouse > 30:
                self.Boxvisible = True
            for i in range(len(self.objects)):
                if self.objects[i].clicked == True:
                    self.clicked_index = i
        self.color_inactive = var.COLOR_INACTIVE
        self.color_active = var.COLOR_ACTIVE
        self.color_on_mouse = var.COLOR_ACTIVE2
                    

    def draw(self, screen):
        if self.visible:
            if self.Boxvisible:
                for object in self.objects:
                    object.draw(screen)
            tetragon(self.rect, self.color, 2, 5,screen)
            screen.blit(self.font.render(self.main_name, True, self.color), (self.rect.x+5, self.rect.y+5))
class Menubar:
    def __init__(self, rect, main_name, element_names, font = var.FONT, visible = True, clicked = False, size = 20,elementwidth = 100, color_inactive = var.COLOR_INACTIVE, color_active = var.COLOR_ACTIVE, color_on_mouse = var.COLOR_ACTIVE, NoFrame = False, NoOutLine = True) -> None:
        self.rect = rect
        self.main_name = main_name
        self.elements = element_names
        self.font = font
        self.visible = visible
        self.clicked = clicked
        self.clicked_index = -1 # クリックされたインデックスを入れる、処理が再び入ると-1に戻る
        self.clicked_name = "" # クリックされた要素の名前を入れる、処理が再び入ると""に戻る
        self.color = var.COLOR_INACTIVE
        self.color_inactive = var.COLOR_INACTIVE
        self.color_active = var.COLOR_ACTIVE
        self.color_on_mouse = var.COLOR_ACTIVE2
        self.count_on_mouse = 0
        self.Boxvisible = False
        self.NoFrame = NoFrame
        self.NoOutLine = NoOutLine
        self.frame = Frame(pg.Rect(rect.x - 5,rect.y - 5 + size ,elementwidth + 10, size * len(self.elements)),True,0)
        self.outframe = Frame(pg.Rect(rect.x - 5,rect.y - 5 + size ,elementwidth + 10, size * len(self.elements)),True,3, self.color_inactive)
        self.objects = []
        self.cancelrightclicked = False
        self.countflag = False
        self.count = 0
        for i in range(len(self.elements)):
            self.objects.append(Button(pg.Rect(rect.x, rect.y + size * (i + 1), elementwidth , rect.h),self.elements[i], self.font, True,color_inactive,color_active,color_on_mouse,NoFrame))
    def handle_event(self, event):
        if self.visible:
            if self.countflag:
                self.count += 1
                if self.count > 3:
                    self.count = 0
                    self.cancelrightclicked = False
                    self.countflag = False
            if self.Boxvisible:
                for object in self.objects:
                        object.handle_event(event)
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.Boxvisible = not self.Boxvisible
                    self.count_on_mouse = 0
                    if self.Boxvisible:
                        self.cancelrightclicked = True
                        self.color = self.color_active
                    else:
                        self.countflag = True
                        self.color = self.color_inactive
                else :
                    self.countflag = True
                    self.count_on_mouse = 0
                    self.Boxvisible = False
                    self.color = self.color_inactive
            mouse_x, mouse_y = pg.mouse.get_pos()
            if self.rect.collidepoint(mouse_x, mouse_y):
                self.color = self.color_on_mouse
            else :
                if not self.Boxvisible:
                    self.color = self.color_inactive
                    self.count_on_mouse = 0
    def update(self):
        if self.visible:
            for object in self.objects:
                object.update()
            self.clicked_index = -1
            self.clicked_name = ""
            for i in range(len(self.objects)):
                if self.objects[i].clicked == True:
                    self.clicked_index = i
                    self.clicked_name = self.elements[i]
        self.color_inactive = var.COLOR_INACTIVE
        self.color_active = var.COLOR_ACTIVE
        self.color_on_mouse = var.COLOR_ACTIVE2
                    

    def draw(self, screen):

        if self.visible:
            if self.Boxvisible:
                self.frame.draw(screen)
                if self.NoOutLine:
                    self.outframe.draw(screen)
                for object in self.objects:
                    object.draw(screen)
            if not self.NoFrame:
                tetragon(self.rect, self.color, 2, 5,screen)
            screen.blit(self.font.render(self.main_name, True, self.color), (self.rect.x+5, self.rect.y+5))
class RowText:
    def __init__(self, rect, element_names, font = var.FONT, visible = True, clicked = False, size = 20,elementwidth = 100, color_inactive = var.COLOR_INACTIVE, color_active = var.COLOR_ACTIVE, color_on_mouse = var.COLOR_ACTIVE, NoFrame = False, NoOutLine = True) -> None:
        self.rect = rect
        self.elements = element_names
        self.font = font
        self.visible = visible
        self.clicked = clicked
        self.clicked_index = -1 # クリックされたインデックスを入れる、処理が再び入ると-1に戻る
        self.clicked_name = "" # クリックされた要素の名前を入れる、処理が再び入ると""に戻る
        self.color = var.COLOR_INACTIVE
        self.color_inactive = var.COLOR_INACTIVE
        self.color_active = var.COLOR_ACTIVE
        self.color_on_mouse = var.COLOR_ACTIVE2
        self.NoFrame = NoFrame
        self.NoOutLine = NoOutLine
        self.size = size
        self.objects = []
        for i in range(len(self.elements)):
            self.objects.append(Button(pg.Rect(rect.x, rect.y + size * i, elementwidth , rect.h),self.elements[i], self.font, True,color_inactive,color_active,color_on_mouse,NoFrame))
        self.rect.h = len(self.elements) * size
    def handle_event(self, event):
        if self.visible:
            for object in self.objects:
                    object.handle_event(event)
    def update(self):
        if self.visible:
            for object in self.objects:
                object.update()
            self.clicked_index = -1
            self.clicked_name = ""
            for i in range(len(self.objects)):
                if self.objects[i].clicked == True:
                    self.clicked_index = i
                    self.clicked_name = self.elements[i]
        self.color_inactive = var.COLOR_INACTIVE
        self.color_active = var.COLOR_ACTIVE
        self.color_on_mouse = var.COLOR_ACTIVE2
    def draw(self, screen):
        if self.visible:
            pg.draw.rect(screen, pg.Color(30,30,30), pg.Rect(self.rect.x, self.rect.y , self.rect.w, self.rect.h ), 0) # 横
            for object in self.objects:
                object.draw(screen)
            if not self.NoOutLine:
                tetragon(self.rect, self.color, 2, 5,screen)
class ColumnText:
    def __init__(self, rect, element_names, font = var.FONT, visible = True, clicked = False, space = 20,elementwidth = 100, color_inactive = var.COLOR_INACTIVE, color_active = var.COLOR_ACTIVE, color_on_mouse = var.COLOR_ACTIVE, NoFrame = False, NoOutLine = True) -> None:
        self.rect = rect
        self.elements = element_names
        self.font = font
        self.visible = visible
        self.clicked = clicked
        self.clicked_index = -1 # クリックされたインデックスを入れる、処理が再び入ると-1に戻る
        self.clicked_name = "" # クリックされた要素の名前を入れる、処理が再び入ると""に戻る
        self.color = var.COLOR_INACTIVE
        self.color_inactive = var.COLOR_INACTIVE
        self.color_active = var.COLOR_ACTIVE
        self.color_on_mouse = var.COLOR_ACTIVE2
        self.NoFrame = NoFrame
        self.NoOutLine = NoOutLine
        self.objects = []
        for i in range(len(self.elements)):
            self.objects.append(Button(pg.Rect(rect.x + elementwidth * i + space * i, rect.y, elementwidth , rect.h),self.elements[i], self.font, True,color_inactive,color_active,color_on_mouse,NoFrame))
    def handle_event(self, event):
        if self.visible:
            for object in self.objects:
                    object.handle_event(event)
    def update(self):
        if self.visible:
            for object in self.objects:
                object.update()
            self.clicked_index = -1
            self.clicked_name = ""
            for i in range(len(self.objects)):
                if self.objects[i].clicked == True:
                    self.clicked_index = i
                    self.clicked_name = self.elements[i]
        self.color_inactive = var.COLOR_INACTIVE
        self.color_active = var.COLOR_ACTIVE
        self.color_on_mouse = var.COLOR_ACTIVE2
    def draw(self, screen):
        if self.visible:
            for object in self.objects:
                object.draw(screen)
            if not self.NoOutLine:
                tetragon(self.rect, self.color, 2, 5,screen)
class Texts:
    def __init__(self, rect, elements, font, color, visible, space, width):
        self.rect = rect
        self.elements = elements
        self.texts = []
        self.font = font
        self.color = color
        self.visible = visible
        self.width = width
        for i in range(len(elements)):
            self.texts.append(Text(pg.Rect(self.rect.x, self.rect.y + self.font.size("1fekv:")[1] * i + space * i, width, self.font.size("1fekv:")[1]),elements[i],self.font, True, self.color))
    def update(self):
        for te in self.texts:
            te.update()
        self.color_inactive = var.COLOR_INACTIVE
        self.color_active = var.COLOR_ACTIVE
        self.color_on_mouse = var.COLOR_ACTIVE2
    def draw(self, screen):
        for te in self.texts:
            te.draw(screen)
class InputBoxAndText:
    def __init__(self, rect, text, font, color_inactive, color_active, visible, auto_rect = True,inputbox_rect = pg.Rect(0,0,0,0), inputbox_text = ""):
        self.rect = rect
        self.font = font
        self.color = color_inactive
        self.color_inactive = color_inactive
        self.color_active = color_active

        self.visible = visible
        self.auto_rect = auto_rect
        if auto_rect:
            self.inputbox_rect = pg.Rect(font.size(text)[0] + self.rect.x, self.rect.y, self.rect.w, self.rect.h)
        else:
            self.inputbox_rect = inputbox_rect
        self.inputbox = InputBox(self.inputbox_rect, inputbox_text, self.font, visible, False, self.color, self.color_active, self.color_inactive)
        self.text = Text(rect, text, font, True, self.color)
    def handle_event(self, event):
        self.inputbox.handle_event(event)

    def update(self):
        self.inputbox.update()
        self.text.update()
    def draw(self, screen):
        self.inputbox.draw(screen)
        self.text.draw(screen)

if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode((1280, 880))
    done = False
    image = pg.transform.scale(pg.image.load("ikemen.png"), (60, 60))
    image_d = pg.transform.scale(pg.image.load("drag.png"), (60, 60))
    btn_image = ButtonImage(pg.Rect(200,200,60,60),True,image,image_d,image)
    input = InputBox(pg.Rect(10,30,32,32),"",var.FONT,True,True,pg.Color('lightskyblue3'),pg.Color('dodgerblue2'),pg.Color('dodgerblue1'))
    text = Text(pg.Rect(10,400,32,32),"helloworld",var.FONT,True)
    checkbox = CheckBox(pg.Rect(10, 300,126,32), "checked",var.FONT, True, True, var.COLOR_INACTIVE,20)
    box = CombineBox(pg.Rect(10,600,64,32),"box :",["hello","world", "and", "see you", "world"],var.FONT,True,False,38)
    box1 = Menubar(pg.Rect(20,10,64,32),"file",["new create","save", "name save", "setting", "close Windows"],var.FONT,True,False,38,170,var.COLOR_INACTIVE,var.COLOR_ACTIVE,var.COLOR_ACTIVE,True, True)
    objects = [btn_image, input, text, checkbox,box,box1]
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            for handle in objects:
                handle.handle_event(event)
        for object_update in objects:
            object_update.update()
        screen.fill((30, 30, 30))
        for object_draw in objects:
            object_draw.draw(screen)
        pg.display.flip()
        pg.time.Clock().tick(60)
    pg.quit()