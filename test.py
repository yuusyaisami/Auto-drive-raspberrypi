from pygui import gui
import pygame as pg
import variables
var = variables.Variables()
pg.init()
screen = pg.display.set_mode((1280, 880))

def main():
    clock = pg.time.Clock()
    done = False
    while not done:
        screen.fill((30, 30, 30))
        pg.display.flip()
        print(var.FONT.size("ksjdf;aoisjdfgnk")[1])
        clock.tick(24)

if __name__ == '__main__':
    main()
    pg.quit()