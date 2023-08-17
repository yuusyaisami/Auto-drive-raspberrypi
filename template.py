from pygui import gui
import pygame as pg

pg.init()
screen = pg.display.set_mode((1280, 880))

def main():
    clock = pg.time.Clock()
    done = False
    while not done:
        screen.fill((30, 30, 30))
        pg.draw.line(screen, pg.Color(10,240,10), 0,1280, 5)
        pg.display.flip()
        clock.tick(24)

if __name__ == '__main__':
    main()
    pg.quit()