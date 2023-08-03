class Driver:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
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
    # 最短距離
    def MazeShortestRoute(self, array, driver):
        gx, gy = self.Search(array, 98)
        error = 0
        nowvalue = array[gy][gx]
        array[gy][gx] = 90
        flag = False
        while True:
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