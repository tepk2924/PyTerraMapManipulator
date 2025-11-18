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

MAZE_ROW = 60
MAZE_COL = 100
CELL_SIZE = 8
G = 1 #must be gt 0, lt CELL_SIZE//2
assert 0 < G < CELL_SIZE//2
S = 50 #must be gt 42
assert S > 42

maze = [[Cell() for _ in range(MAZE_COL)] for _ in range(MAZE_ROW)]

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
    if col < MAZE_COL - 1 and maze[row][col].can_R == False and maze[row][col + 1].is_on == False:
        dir_choices.append(Direction.R)
    #check D
    if row < MAZE_ROW - 1 and maze[row][col].can_D == False and maze[row + 1][col].is_on == False:
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
        try:
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
        except Exception as e:
            print(row, col, e)
            exit(1)

maze[MAZE_ROW - 1][MAZE_COL - 1].can_R = True

world = TerrariaWorld((S + CELL_SIZE*MAZE_ROW + S, S + CELL_SIZE*MAZE_COL + S))

world.spawnX = S + CELL_SIZE//2
world.spawnY = S + CELL_SIZE//2

world.tiles.enter_editmode()

for row in range(MAZE_ROW):
    for col in range(MAZE_COL):
        world.tiles.tileinfos[S + CELL_SIZE*row:S + CELL_SIZE*-~row, S + CELL_SIZE*col:S + CELL_SIZE*-~col, Channel.TILETYPE] = TileID.GrayBrick
        world.tiles.tileinfos[S + 1 + CELL_SIZE*row:S - 1 + CELL_SIZE*-~row, S + 1 + CELL_SIZE*col:S - 1 + CELL_SIZE*-~col, Channel.TILETYPE] = TileID.Air
        world.tiles.tileinfos[S + CELL_SIZE*row:S + CELL_SIZE*-~row, S + CELL_SIZE*col:S + CELL_SIZE*-~col, Channel.WALL] = WallID.GrayBrick
        if maze[row][col].can_L:
            world.tiles.tileinfos[S + CELL_SIZE*row + G:S + CELL_SIZE*-~row - G, S + CELL_SIZE*col, Channel.TILETYPE] = TileID.Air
        if maze[row][col].can_U:
            world.tiles.tileinfos[S + CELL_SIZE*row, S + CELL_SIZE*col + G:S + CELL_SIZE*-~col - G, Channel.TILETYPE] = TileID.Air
        if maze[row][col].can_R:
            world.tiles.tileinfos[S + CELL_SIZE*row + G:S + CELL_SIZE*-~row - G, S - 1 + CELL_SIZE*-~col, Channel.TILETYPE] = TileID.Air
        if maze[row][col].can_D:
            world.tiles.tileinfos[S - 1 + CELL_SIZE*-~row, S + CELL_SIZE*col + G:S + CELL_SIZE*-~col - G, Channel.TILETYPE] = TileID.Air

world.tiles.tileinfos[S:S + CELL_SIZE*MAZE_ROW, S, Channel.WALL] = WallID.Air
world.tiles.tileinfos[S:S + CELL_SIZE*MAZE_ROW, S + CELL_SIZE*MAZE_COL - 1, Channel.WALL] = WallID.Air
world.tiles.tileinfos[S, S:S + CELL_SIZE*MAZE_COL, Channel.WALL] = WallID.Air
world.tiles.tileinfos[S + CELL_SIZE*MAZE_ROW - 1, S:S + CELL_SIZE*MAZE_COL, Channel.WALL] = WallID.Air

world.tiles.exit_editmode()

world.save_world("maze")