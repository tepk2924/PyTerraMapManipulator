import random
import numpy as np
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from enum import IntEnum
from terrariaworld import TerrariaWorld
from enumeration import TileID, WallID, Channel

class Direction(IntEnum):
    L = 0
    U = 1
    R = 2
    D = 3

class Cell:
    def __init__(self):
        self.is_on:bool = False
        self.can_L:bool = False
        self.can_U:bool = False
        self.can_R:bool = False
        self.can_D:bool = False
        self.root:Direction = -1

MAZE_ROW_CNT = 60
MAZE_COL_CNT = 180
CELL_SIZE = 30
GATE_SIZE = 28 #must be gt 0, lt CELL_SIZE
assert 0 < GATE_SIZE < CELL_SIZE
MARGIN = 50 #must be gt 42
assert MARGIN > 42

maze = [[Cell() for _ in range(MAZE_COL_CNT)] for _ in range(MAZE_ROW_CNT)]

row = 0
col = 0

while True:
    maze[row][col].is_on = True

    dir_choices = []
    #check L
    if col > 0 and maze[row][col].can_L == False and maze[row][col - 1].is_on == False:
        dir_choices.append(Direction.L)
    #check U
    if row > 0 and maze[row][col].can_U == False and maze[row - 1][col].is_on == False:
        dir_choices.append(Direction.U)
    #check R
    if col < MAZE_COL_CNT - 1 and maze[row][col].can_R == False and maze[row][col + 1].is_on == False:
        dir_choices.append(Direction.R)
    #check D
    if row < MAZE_ROW_CNT - 1 and maze[row][col].can_D == False and maze[row + 1][col].is_on == False:
        dir_choices.append(Direction.D)

    if len(dir_choices) == 0:
        match maze[row][col].root:
            case Direction.L:
                col -= 1
            case Direction.U:
                row -= 1
            case Direction.R:
                col += 1
            case Direction.D:
                row += 1
            case -1:
                break
    else:
        go_direction = random.choice(dir_choices)
        match go_direction:
            case Direction.L:
                maze[row][col].can_L = True
                col -= 1
                maze[row][col].can_R = True
                maze[row][col].root = Direction.R
            case Direction.U:
                maze[row][col].can_U = True
                row -= 1
                maze[row][col].can_D = True
                maze[row][col].root = Direction.D
            case Direction.R:
                maze[row][col].can_R = True
                col += 1
                maze[row][col].can_L = True
                maze[row][col].root = Direction.L
            case Direction.D:
                maze[row][col].can_D = True
                row += 1
                maze[row][col].can_U = True
                maze[row][col].root = Direction.U

maze[MAZE_ROW_CNT - 1][MAZE_COL_CNT - 1].can_R = True

world = TerrariaWorld((MARGIN + CELL_SIZE*MAZE_ROW_CNT + MARGIN, MARGIN + CELL_SIZE*MAZE_COL_CNT + MARGIN))

world.spawnX = MARGIN + CELL_SIZE//2
world.spawnY = MARGIN + CELL_SIZE//2

world.tiles.enter_editmode()

for row in range(MAZE_ROW_CNT):
    for col in range(MAZE_COL_CNT):
        rstart = MARGIN + CELL_SIZE*row
        rmid = rstart + CELL_SIZE//2
        rnext = rstart + CELL_SIZE
        cstart = MARGIN + CELL_SIZE*col
        cmid = cstart + CELL_SIZE//2
        cnext = cstart + CELL_SIZE
        world.tiles.tileinfos[rstart:rnext, cstart:cnext, Channel.TILETYPE] = TileID.GrayBrick
        world.tiles.tileinfos[rstart + 1:rnext - 1, cstart + 1:cnext - 1, Channel.TILETYPE] = TileID.Air
        if maze[row][col].can_L:
            world.tiles.tileinfos[rmid - GATE_SIZE//2:rmid + GATE_SIZE//2, cstart, Channel.TILETYPE] = TileID.Air
        if maze[row][col].can_U:
            world.tiles.tileinfos[rstart, cmid - GATE_SIZE//2:cmid + GATE_SIZE//2, Channel.TILETYPE] = TileID.Air
        if maze[row][col].can_R:
            world.tiles.tileinfos[rmid - GATE_SIZE//2:rmid + GATE_SIZE//2, cnext - 1, Channel.TILETYPE] = TileID.Air
        if maze[row][col].can_D:
            world.tiles.tileinfos[rnext - 1, cmid - GATE_SIZE//2:cmid + GATE_SIZE//2, Channel.TILETYPE] = TileID.Air

world.tiles.tileinfos[MARGIN + 1:MARGIN + CELL_SIZE*MAZE_ROW_CNT - 1, MARGIN + 1:MARGIN + CELL_SIZE*MAZE_COL_CNT - 1, Channel.WALL] = WallID.GrayBrick

world.tiles.exit_editmode()

world.save_world("maze")