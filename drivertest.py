import driver as dr

map = [ [99,99,99,99,99,99, 99,99, 99],
        [99, 0, 0, 0, 0, 0,  0, 0, 99],
        [99, 0,99, 0,99, 0, 99, 0, 99],
        [99, 0, 0, 0, 0, 0,  0, 0, 99],
        [99, 0,99, 0,99, 0, 99, 0, 99],
        [99, 0, 0, 0, 0, 0, 0 , 0, 99],
        [99, 0,99, 0,99, 0, 99, 0, 99],
        [99, 0, 0, 0, 0, 0, 0 , 0, 99],
        [99,99,99,99,99,99, 99,99, 99]]

driver = dr.Driver(1,4,0)
shorter = dr.MazeShortest()
map = shorter.ResetMaze(map)
map = shorter.MazeWaterValue(map, driver)
shorter.PrintArray(map,1)
map[int(input("y : "))][int(input("x : "))] = 98
map, error = shorter.MazeShortestRoute(map, driver)
shorter.PrintArray(map,1)
if error == 1:
    print("error : 目的地に到達できません")
while True:
    map, driver.x, driver.y, direction, driver.direction = shorter.DriverDirection(map, driver)
    if direction == -2:
        break
shorter.PrintArray(map,1)
