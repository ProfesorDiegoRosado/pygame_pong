import sys
import pygame as pg
from pygame.locals import *
from src.board import Board, Direction

dimension_y = 300
dimension_x = dimension_y * 2
display_dimension = (dimension_x, dimension_y)
BLACK = (0,0,0)
end = False
FPS = 30

pg.mixer.init()
pg.font.init()
pg.init()

clock: pg.time.Clock = pg.time.Clock()

#display = pg.display.set_mode(display_dimension)
#display.fill(BLACK)
board: Board = Board(display_dimension)

while not end:
    keys = pg.key.get_pressed()
    if keys[pg.K_UP]:
        board.player2.update_position(Direction.UP)
    if keys[pg.K_DOWN]:
        board.player2.update_position(Direction.DOWN)
    if keys[pg.K_q]:
        board.player1.update_position(Direction.UP)
    if keys[pg.K_a]:
        board.player1.update_position(Direction.DOWN)
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
    board.update()
    clock.tick(FPS)   # 30 FPS ???
