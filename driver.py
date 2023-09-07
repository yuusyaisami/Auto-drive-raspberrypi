import numpy as np
import pygame as pg
import variables as vari
var = vari.Variables()
class Driver:
    def __init__(self, x, y, direction, map = [[]]):
        self.screen = pg.display.set_mode((var.WINDOWNSIZE_X, var.WINDOWNSIZE_Y))  

        self.img = None
        self.done = True
        self.x = x
        self.y = y
        self.direction = direction
        self.map_x = 9
        self.map_y = 9

        self.goal_x = 2
        self.goal_y = 1

        self.rightclick_x = -1
        self.rightclick_y = -1
        self.map = map

        self.select_box_x = -1
        self.select_box_y = -1

        self.traffic = []
    def search_map_value(self, value):
        for y in range(self.map_y):
            for x in range(self.map_x):
                if self.map[y][x] == value:
                    return x, y
        return -1, -1
    def search_traffic(self, x, y, direction):
        if direction != -1:
            for index in range(len(self.traffic)):
                if self.traffic[index].map_x == x and self.traffic[index].map_y == y and self.traffic[index].traffic_direction == direction:
                    return index
        elif direction == -1:
            for index in range(len(self.traffic)):
                if self.traffic[index].map_x == x and self.traffic[index].map_y == y:
                    return index
        return None
    def trafic_delete(self, x, y):
        for index in range(len(self.traffic)):
            if self.traffic[index].map_x == x and self.traffic[index].map_y == y:
                del self.traffic[index]
                return
    def traffic_stop(self):
        if self.map[self.y - 1][self.x] == 90 and self.direction == 0:
            nowtraffic = self.search_traffic(self.x , self.y - 1, self.direction)
            if nowtraffic != None:
                if self.traffic[nowtraffic].statue == 1:
                    return True
        if self.map[self.y][self.x + 1] == 90 and self.direction == 1:
            nowtraffic = self.search_traffic(self.x + 1 , self.y, self.direction)
            if nowtraffic != None:
                if self.traffic[nowtraffic].statue == 1:
                    return True
        if self.map[self.y + 1][self.x] == 90 and self.direction == 2:
            nowtraffic = self.search_traffic(self.x , self.y + 1, self.direction)
            if nowtraffic != None:
                if self.traffic[nowtraffic].statue == 1:
                    return True
        if self.map[self.y][self.x - 1] == 90 and self.direction == 3:
            nowtraffic = self.search_traffic(self.x - 1 , self.y, self.direction)
            if nowtraffic != None:
                if self.traffic[nowtraffic].statue == 1:
                    return True
        return False
    def create_map(self):
        self.map = np.empty((0, self.map_x))
        rowsline = np.zeros(self.map_x)
        for i in range(self.map_x):
            rowsline[i] = np.array(99)
        self.map = np.vstack((self.map, rowsline))
        rowsline = np.zeros(self.map_x)
        for i in range(1,self.map_y - 1,1):
            for j in range(self.map_x):
                if j == 0:
                    rowsline[j] = np.array(99)
                elif j % 2 == 0 and i % 2 == 0:
                    rowsline[j] = np.array(99)
                elif j == self.map_x - 1:
                    rowsline[j] = np.array(99)
                else:
                    rowsline[j] = np.array(0)
            self.map = np.vstack((self.map, rowsline))
            rowsline = np.zeros(self.map_x)
            
                
        for i in range(self.map_x):
            rowsline[i] = np.array(99)
        self.map = np.vstack((self.map, rowsline))
        






class MazeShortest:
    def ResetMaze(self, array):
        for y in range(len(array)):
                for x in range(len(array[0])):
                    if array[y][x] == 99:
                        array[y][x] = 99
                    elif array[y][x] == 0:
                        array[y][x] = 0
                    else:
                        array[y][x] = 0
        return array
    # デバッグ用
    def DebugDriver1(self, array, driver, conditions_value, other_value):
        if driver.direction == 0:
            if array[driver.y - 1][driver.x] == conditions_value:
                return -1
        elif driver.direction == 1:
            if array[driver.y][driver.x + 1] == conditions_value:
                return -1
        elif driver.direction == 2:
            if array[driver.y + 1][driver.x] == conditions_value:
                return -1
        elif driver.direction == 3:
            if array[driver.y][driver.x - 1] == conditions_value:
                return -1
        else:
            return other_value
    #数値検索
    def Search(self, array, value):
        for i in range(len(array)):
            for j in range(len(array[0])):
                if array[i][j] == value:
                    return j, i
        return -1, -1
    #数値流し
    def MazeWaterValue(self, array, driver):
        if self.DebugDriver1(array, driver, 99, 0) == -1:
            return array
        nx, ny = self.SearchDirection(array, driver)
        array[ny][nx] = count = 2
        array[driver.y][driver.x] = 99
        try:
            while True:
                for y in range(len(array)):
                    for x in range(len(array[0])):
                        if array[y][x] == count:
                            if array[y - 1][x] == 0:
                                array[y - 1][x] = count + 1
                                flag = True
                            if array[y][x + 1] == 0:
                                array[y][x + 1] = count + 1
                                flag = True
                            if array[y + 1][x] == 0:
                                array[y + 1][x] = count + 1
                                flag = True
                            if array[y][x - 1] == 0:
                                array[y][x - 1] = count + 1
                                flag = True
                count = count + 1
                if flag == False:
                    break
                else:
                    flag = False
            array[driver.y][driver.x] = 1
            return array
        except:
            print("error")
            return array
    # 最短距離
    def MazeShortestRoute(self, array, driver):
        gx, gy = self.Search(array, 98)
        error = 0
        nowvalue = array[gy][gx]
        array[gy][gx] = 90
        flag = False
        while True:
            go = -1
            if array[gy - 1][gx] < nowvalue and array[gy - 1][gx] != 0 and array[gy - 1][gx] != 1:
                nowvalue = array[gy - 1][gx]
                go = 0
                flag = True
            if array[gy][gx + 1] < nowvalue and array[gy][gx + 1] != 0 and array[gy][gx + 1] != 1 :
                nowvalue = array[gy][gx + 1]
                go = 1
                flag = True
            if array[gy + 1][gx] < nowvalue and array[gy + 1][gx] != 0 and array[gy + 1][gx] != 1:
                nowvalue = array[gy + 1][gx]
                go = 2
                flag = True
            if array[gy][gx - 1] < nowvalue and array[gy][gx - 1] != 0 and array[gy][gx - 1] != 1:
                nowvalue = array[gy][gx - 1]
                go = 3
                flag = True
        
            if go == 0:
                nowvalue = array[gy - 1][gx]
                array[gy - 1][gx] = 90
                gy = gy - 1
            if go == 1:
                nowvalue = array[gy][gx + 1]
                array[gy][gx + 1] = 90
                gx = gx + 1
            if go == 2:
                nowvalue = array[gy + 1][gx]
                array[gy + 1][gx] = 90
                gy = gy + 1
            if go == 3:
                nowvalue = array[gy][gx - 1]
                array[gy][gx - 1] = 90
                gx = gx - 1
            if flag == False and nowvalue != 2:
                error = 1
                break
            if nowvalue == 0:
                error = 1
                break
            if nowvalue == 2:
                break
            flag = False
        return array, error
    # driverの向いてる先の座標
    def SearchDirection(self, array, driver ):
        if driver.direction == 0:
            return driver.x ,driver.y - 1
        elif driver.direction == 1:
            return driver.x + 1 ,driver.y
        elif driver.direction == 2:
            return driver.x ,driver.y + 1
        elif driver.direction == 3:
            return driver.x - 1 ,driver.y
        else:
            return -1, -1
    # 配列のprint
    def PrintArray(self, array, frame = 0):
        if frame == 1:
            print("-----------------------------------------------")
        string = ""
        for y in range(len(array)):
            for x in range(len(array[0])):
                if array[y][x] < 10:
                    string += " " + str(array[y][x]) + ","
                elif array[y][x] < 100:
                    string += str(array[y][x]) + ","
            print(string)
            string = ""
        if frame == 1:
            print("-----------------------------------------------")
    def DriverDirection(self, array, driver):
        next_direction = -2
        if driver.direction == 0:
            if array[driver.y - 1][driver.x - 1] == 90:
                next_direction = -1
                array[driver.y][driver.x] = 80
                driver.y = driver.y - 1
                driver.x = driver.x - 1
                driver.direction = 3
            elif array[driver.y - 1][driver.x + 1] == 90:
                next_direction = 1
                array[driver.y][driver.x] = 80
                driver.y = driver.y - 1
                driver.x = driver.x + 1
                driver.direction = 1
            elif array[driver.y - 2][driver.x] == 90:
                next_direction = 0
                array[driver.y][driver.x] = 80
                array[driver.y - 1][driver.x] = 80
                driver.y = driver.y - 2
                driver.x = driver.x
                driver.direction = 0
        elif driver.direction == 1:
            if array[driver.y - 1][driver.x + 1] == 90:
                next_direction = -1
                array[driver.y][driver.x] = 80
                driver.y = driver.y - 1
                driver.x = driver.x + 1
                driver.direction = 0
            elif array[driver.y + 1][driver.x + 1] == 90:
                next_direction = 1
                array[driver.y][driver.x] = 80
                driver.y = driver.y + 1
                driver.x = driver.x + 1
                driver.direction = 2
            elif array[driver.y    ][driver.x + 2] == 90:
                next_direction = 0
                array[driver.y][driver.x] = 80
                array[driver.y][driver.x + 1] = 80
                driver.y = driver.y
                driver.x = driver.x + 2
                driver.direction = 1
        elif driver.direction == 2:
            if array[driver.y + 1][driver.x + 1] == 90:
                next_direction = -1
                array[driver.y][driver.x] = 80
                driver.y = driver.y + 1
                driver.x = driver.x + 1
                driver.direction = 1
            elif array[driver.y + 1][driver.x - 1] == 90:
                next_direction = 1
                array[driver.y][driver.x] = 80
                driver.y = driver.y + 1
                driver.x = driver.x - 1
                driver.direction = 3
            elif array[driver.y + 2][driver.x] == 90:
                next_direction = 0
                array[driver.y][driver.x] = 80
                array[driver.y + 1][driver.x] = 80
                driver.y = driver.y + 2
                driver.x = driver.x
                driver.direction = 2
        elif driver.direction == 3:
            if array[driver.y + 1][driver.x - 1] == 90:
                next_direction = -1
                array[driver.y][driver.x] = 80
                driver.y = driver.y + 1
                driver.x = driver.x - 1
                driver.direction = 2
            elif array[driver.y - 1][driver.x - 1] == 90:
                next_direction = 1
                array[driver.y][driver.x] = 80
                driver.y = driver.y - 1
                driver.x = driver.x - 1
                driver.direction = 0
            elif array[driver.y    ][driver.x - 2] == 90:
                next_direction = 0
                array[driver.y][driver.x] = 80
                array[driver.y][driver.x - 1] = 80
                driver.y = driver.y
                driver.x = driver.x - 2
                driver.direction = 3
        array[driver.y][driver.x] = 80
        return array, driver.x, driver.y, next_direction, driver.direction
    def Go(self, array, driver, direction):
        if direction == -1: #左
            return
        if direction == 0: #前
            return
        if direction == 1: #右
            return