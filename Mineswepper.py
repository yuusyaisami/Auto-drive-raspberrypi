from pygui import gui
import pygame as pg
import numpy as np
import random
pg.init()

color_inactive = pg.Color("blue1")
color_index1 = pg.Color(135, 206, 235)
color_open = pg.Color("white")
color_bom = pg.Color("red")
FONT_SMALL = pg.font.Font(None, 30)
screen = pg.display.set_mode((1280, 880))
class Text:
    def __init__(self, rect, x, y):
        self.rect = rect
        self.color = color_index1
        self.x = x
        self.y = y
        self.visible = False
        self.text = ""
        if(gamescene.map_index[y][x] != 0 and gamescene.map_index[y][x] != -1):
            self.text = str(gamescene.map_index[y][x])
    def handle_event(self, event):
        pass
    def update(self):
        pass
    def draw(self, screen):
        if self.visible:
            screen.blit(FONT_SMALL.render(self.text, True, self.color), (self.rect.x + 5, self.rect.y + 1))
class Box():
    def __init__(self, rect, x, y):
        self.rect = rect
        self.x = x
        self.y = y
        self.color = color_inactive
        self.visible = True
        self.visible_handle_event = True
        self.isBom = False
        self.isForceRun = False
        self.isGameover = False
        if gamescene.map[y][x] == 1:
            self.isBom = True
        self.isOpen = False
    def handle_event(self, event):
        if self.visible and self.visible_handle_event:
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    if self.isBom:
                        self.isOpen = True
                        gamescene.gameover_c()
                    else:
                        self.isOpen = True
                        if not gamescene.isFirstClick and not gamescene.inProgress:
                            gamescene.isFirstClick = True
                            gamescene.first_click_y = self.y
                            gamescene.first_click_x = self.x
                            self.isForceRun = True
                        else:
                            self.check_open()
                            gamescene.visible_text(self.x, self.y, True)
                            self.check_gameclear()
    def update(self):
        if self.visible:
            if self.isOpen:
                if self.isBom:
                    self.color = color_bom
                else:
                    self.color = color_open
            else:
                self.color = color_inactive
            self.check_gameclear()

            if self.isForceRun and not self.isOpen:
                self.isForceRun = False
                if self.isBom:
                    self.isGameover = True
                    gamescene.gameover_c()
                else:
                    self.isOpen = True
                    if not gamescene.isFirstClick and not gamescene.inProgress:
                        gamescene.isFirstClick = True
                        gamescene.first_click_y = self.y
                        gamescene.first_click_x = self.x
                    else:
                        self.check_open()
                        gamescene.visible_text(self.x, self.y, True)
                        self.check_gameclear()
    def draw(self, screen):
        if self.visible:
            pg.draw.rect(screen, self.color, self.rect, 0)
    def check_open(self):
        raw = len(gamescene.map)
        column = len(gamescene.map[0])
        index = gamescene.search_box(self.x, self.y)
        if gamescene.map_index[self.y][self.x] == 0:
            if self.y - 1 != -1:
                index = gamescene.search_box(self.x, self.y - 1)
                if not gamescene.box_list[index].isOpen:
                    gamescene.box_list[index].isForceRun = True
            if self.y + 1 < raw:
                index = gamescene.search_box(self.x, self.y + 1)
                if not gamescene.box_list[index].isOpen:
                    gamescene.box_list[index].isForceRun = True
            if self.x - 1 != -1:
                index = gamescene.search_box(self.x - 1, self.y)
                if not gamescene.box_list[index].isOpen:
                    gamescene.box_list[index].isForceRun = True
            if self.x + 1 < column:
                index = gamescene.search_box(self.x + 1, self.y)
                if not gamescene.box_list[index].isOpen:
                    gamescene.box_list[index].isForceRun = True
            if self.y - 1 != -1 and self.x - 1 != -1:
                index = gamescene.search_box(self.x - 1, self.y - 1)
                if not gamescene.box_list[index].isOpen:
                    gamescene.box_list[index].isForceRun = True
            if self.y - 1 != -1 and self.x + 1 < column:
                index = gamescene.search_box(self.x + 1, self.y - 1)
                if not gamescene.box_list[index].isOpen:
                    gamescene.box_list[index].isForceRun = True
            if self.y + 1 < raw and self.x - 1 != -1:
                index = gamescene.search_box(self.x - 1, self.y + 1)
                if not gamescene.box_list[index].isOpen:
                    gamescene.box_list[index].isForceRun = True
            if self.y + 1 < raw and self.x + 1 < column:
                index = gamescene.search_box(self.x + 1, self.y + 1)
                if not gamescene.box_list[index].isOpen:
                    gamescene.box_list[index].isForceRun = True
    def check_gameclear(self):
        if gamescene.gameclear_count == 0:
            raw = len(gamescene.map)
            column = len(gamescene.map[0])
            for y in range(raw):
                for x in range(column):
                    index = gamescene.search_box(x, y)
                    if gamescene.map_index[y][x] != -1:
                        if gamescene.box_list[index].isOpen:
                            pass
                        else:
                            return False
            gamescene.gameclear_c()
            

class GameScene:
    def __init__(self, default_x, default_y):
        self.isStart = False
        self.inProgress = False
        self.isFirstClick = False
        self.isGameOver = False

        self.map_size_x = 15
        self.map_size_y = 15
        self.map_box_size_x = 32
        self.map_box_size_y = 32
        self.map_box_space_x = 40
        self.map_box_space_y = 40


        self.gameclear_count = 0
        self.gameover_count = 0
        self.first_click_x = 0
        self.first_click_y = 0
        self.turns = 0
        self.d_x = default_x
        self.d_y = default_y
        self.number_of_bom = 10
        self.box_list = []
        self.text_list = []
        self.map_index = [[]]
        #bom : 1, open : 0
        self.map = [[]]
        self.map = np.array(self.map)
        self.map = np.zeros_like(self.map)
        self.map_index = np.array(self.map_index)
        self.map_index = np.zeros_like(self.map_index)
        #for y in range(len(map)):
            #for x in range(len(map[0])):
    def handle_event(self, event):
        for boxs in self.box_list:
            boxs.handle_event(event)
    def update(self):
        if self.isStart:
            self.isStart = False
            self.create_map(self.map_size_x, self.map_size_y)
            self.create_box()
        if self.isFirstClick and not self.inProgress:
            self.inProgress = True
            self.isFirstClick = False
            self.design_map(self.first_click_x, self.first_click_y)
            self.design_map_index()
            self.create_box()
            self.create_text()
            self.box_list[self.search_box(self.first_click_x, self.first_click_y)].isForceRun = True
        if self.inProgress:
            pass
        for boxs in self.box_list:
            boxs.update()
            if self.isGameOver:
                break
        for texts in self.text_list:
            texts.update()
        if self.gameclear_count > 0:
            self.gameclear_count += 1
            if self.gameclear_count > 20:
                self.game_clear()
                self.gameclear_count = 0
        if self.gameover_count > 0:
            self.gameover_count += 1
            if self.gameover_count > 20:
                self.game_over()
                self.gameover_count = 0
    def draw(self, screen):
        for boxs in self.box_list:
            boxs.draw(screen)
        for texts in self.text_list:
            texts.draw(screen)
    def gameover_c(self):
        gamescene.gameover_count = 1
        for boxs in self.box_list:
            boxs.visible_handle_event = False
    def gameclear_c(self):
        gamescene.gameclear_count = 1
        for boxs in self.box_list:
            boxs.visible_handle_event = False
    def design_map(self, x, y):
        i = 0
        self.map = np.zeros_like(self.map)
        while i < self.number_of_bom:
            raw = random.randint(0, len(self.map) - 1)
            column = random.randint(0, len(self.map[0]) - 1)
            if (raw - 1 == y and column - 1 == x) or (raw - 1 == y and column == x) or (raw - 1 == y and column + 1 == x) or (raw == y and column - 1 == x) or (raw == y and column == x) or (raw == y and column + 1 == x) or (raw + 1 == y and column - 1 == x) or (raw + 1 == y and column == x) or (raw + 1 == y and column + 1 == x) or self.map[raw][column] == 1:
                i -= 1  
            else:
                self.map[raw][column] = 1
            i += 1
        self.design_map_index()
    def game_over(self):
        self.isGameOver = True
        self.box_list = []
        self.text_list = []
        self.map = np.zeros_like(self.map)
        self.first_click_x = 0
        self.first_click_y = 0
        self.turns = 0
        self.box_list = []
        self.text_list = []
        self.map_index = [[]]
        #bom : 1, open : 0
        self.map = [[]]

        self.isStart = True
        self.inProgress = False
        self.isFirstClick = False
        self.isGameOver = False
        print("game over")
    def game_clear(self):
        self.isGameOver = True
        self.box_list = []
        self.text_list = []
        self.map = np.zeros_like(self.map)
        self.first_click_x = 0
        self.first_click_y = 0
        self.turns = 0
        self.box_list = []
        self.text_list = []
        self.map_index = [[]]
        #bom : 1, open : 0
        self.map = [[]]

        self.isStart = True
        self.inProgress = False
        self.isFirstClick = False
        self.isGameOver = False
        print("game clear")
    def design_map_index(self):
        self.map_index = self.map
        self.map_index = np.zeros_like(self.map_index)
        raw = len(self.map)
        column = len(self.map[0])
        for y in range(raw):
            for x in range(column):
                index = 0
                if y - 1 != -1 and x - 1 != -1:
                    if self.map[y - 1][x - 1] == 1:
                        index += 1
                if y - 1 != -1:
                    if self.map[y - 1][x] == 1:
                        index += 1
                if y - 1 != -1 and x + 1 < column:
                    if self.map[y - 1][x + 1] == 1:
                        index += 1
                if x + 1 < column:
                    if self.map[y][x + 1] == 1:
                        index += 1
                if x - 1 != -1:
                    if self.map[y][x - 1] == 1:
                        index += 1
                if y + 1 < raw and x - 1 != -1:
                    if self.map[y + 1][x - 1] == 1:
                        index += 1
                if y + 1 < raw:
                    if self.map[y + 1][x] == 1:
                        index += 1
                if y + 1 < raw and x + 1 < column:
                    if self.map[y + 1][x + 1] == 1:
                        index += 1
                if self.map[y][x] == 1:
                    index = -1
                self.map_index[y][x] = index
    def create_box(self):
        self.box_list = []
        raw = len(self.map)
        column = len(self.map[0])
        for y in range(raw):
            for x in range(column):
                self.box_list.append(Box(pg.Rect(y * self.map_box_space_y + self.d_y, x * self.map_box_space_x + self.d_x, self.map_box_size_x, self.map_box_size_y),x, y))
    def create_text(self):
        self.text_list = []
        raw = len(self.map)
        column = len(self.map[0])
        for y in range(raw):
            for x in range(column):
                self.text_list.append(Text(pg.Rect(y * self.map_box_space_y + self.d_y, x * self.map_box_space_x + self.d_x, self.map_box_size_x, self.map_box_size_y),x, y))
    def visible_text(self, x, y, bool):
        for texts in self.text_list:
            if texts.x == x and texts.y == y:
                texts.visible = bool
                break
    def search_box(self, x, y):
        for i in range(len(self.box_list)):
            if self.box_list[i].x == x and self.box_list[i].y == y:
                return i
    def create_map(self, map_size_x, map_size_y):
        self.map = np.empty((0, map_size_x), dtype=int)
        self.map_index = np.empty((0, map_size_x), dtype=int)
        line = np.zeros(map_size_x, dtype=int)
        for i in range(map_size_y):
            self.map = np.vstack((self.map, line))
            self.map_index = np.vstack((self.map_index, line))



gamescene = GameScene(50, 50)
def main():
    clock = pg.time.Clock()
    done = False
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            gamescene.handle_event(event)
        gamescene.update()
        screen.fill((30, 30, 30))
        gamescene.draw(screen)
        pg.display.flip()
        clock.tick(24)

if __name__ == '__main__':
    main()
    pg.quit()