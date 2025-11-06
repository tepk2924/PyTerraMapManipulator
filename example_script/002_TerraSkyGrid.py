import sys
import os
import random
import numpy as np
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from terrariaworld import TerrariaWorld
from enumeration import GameMode, Ch, Liquid
from chest import Chest, Item

def Place_Sprite(world:TerrariaWorld,
                 row:int,
                 col:int,
                 sprite_rownum:int,
                 sprite_colnum:int,
                 sprite_number:int):
    world.tiles.tileinfos[row:row + sprite_rownum, col:col + sprite_colnum, Ch.TILETYPE] = sprite_number
    for r in range(sprite_rownum):
        for c in range(sprite_colnum):
            world.tiles.tileinfos[row + r, col + c, Ch.U] = 18*c
            world.tiles.tileinfos[row + r, col + c, Ch.V] = 18*r

def Place_Chest(world:TerrariaWorld,
                row:int,
                col:int,
                itemnum:int,
                itemcnt:int=1):
    Place_Sprite(world, row, col, 2, 2, 21)
    chest = Chest(col, row, "")
    chest.items[0].netid = itemnum
    chest.items[0].stacksize = itemcnt
    world.chests.append(chest)

world = TerrariaWorld()
world.gamemode = GameMode.MASTER

blocklist = []

for idx in range(len(world.tileframeimportant)):
    if world.tileframeimportant[idx] == False:
        blocklist.append(idx)

ROW = world.tileshigh // 5 #480
COL = world.tileswide // 5 #1600
states = np.zeros((ROW, COL))

world.tiles.enter_editmode()
tile = -1 * np.ones((ROW*5, COL*5))
for r in range(ROW):
    for c in range(COL):
        tile[5*r + 3, 5*c + 2] = random.choice(blocklist)
world.tiles.tileinfos[:, :, Ch.TILETYPE] = tile

#Generate Dungeon
'''
Dungeon : 5884 West, 148 Height
'''
world.dungeonY = 458 #Row
world.dungeonX = 1260 #Column
world.tiles.tileinfos[400, 1220:1300, Ch.TILETYPE] = 41 #Placing Dungeon Brick
world.tiles.tileinfos[401:458, 1220:1300, Ch.TILETYPE] = -1 #Placing Air
world.tiles.tileinfos[458:460, 1220:1300, Ch.TILETYPE] = 41 #Placing Dungeon Brick
states[80:92, 244:260] = 1

#Generate Shimmer Pond
world.tiles.tileinfos[1200:1220, 6200:6400, Ch.TILETYPE] = 1 #Placing Stone
world.tiles.tileinfos[1200:1205, 6280:6320, Ch.TILETYPE] = -1 #Placing Air to fill shimmer
world.tiles.tileinfos[1200:1205, 6280:6320, Ch.LIQUIDTYPE] = Liquid.SHIMMER
world.tiles.tileinfos[1200:1205, 6280:6320, Ch.LIQUIDAMOUNT] = 255
states[240:244, 1240:1280] = 1

#Generate Temple
world.tiles.tileinfos[1100:1158, 5800:5900, Ch.TILETYPE] = -1 #Placing Air
world.tiles.tileinfos[1158:1160, 5800:5900, Ch.TILETYPE] = 226 #Placing Lihzarhd Brick
Place_Sprite(world, 1156, 5850, 2, 3, 237) #Placing Lih Altar
Place_Chest(world, 1156, 5830, 1293, 10) #Placing Chest with 10 Lih Cell
Place_Chest(world, 1156, 5870, 1293, 10) #Placing Chest with 10 Lih Cell
states[220:232, 1160:1180] = 1


states[79:89, 830:850] = 1

#Generate Water
for _ in range(2000):
    while True:
        r = random.randint(50, ROW - 51)
        c = random.randint(50, COL - 51)
        if states[r, c] != 1:
            break
    world.tiles.tileinfos[5*r + 3, 5*c + 2, Ch.TILETYPE] = -1 #Placing Air
    world.tiles.tileinfos[5*r + 3, 5*c + 2, Ch.LIQUIDTYPE] = Liquid.WATER
    world.tiles.tileinfos[5*r + 3, 5*c + 2, Ch.LIQUIDAMOUNT] = 255
    world.tiles.tileinfos[5*r + 4, 5*c + 2, Ch.TILETYPE] = 379 #Placing bubble to hold liquid
    world.tiles.tileinfos[5*r + 3, 5*c + 1, Ch.TILETYPE] = 379 #Placing bubble to hold liquid
    world.tiles.tileinfos[5*r + 3, 5*c + 3, Ch.TILETYPE] = 379 #Placing bubble to hold liquid
    states[r, c] = 1

#Generate Lava
for _ in range(1000):
    while True:
        r = random.randint(50, ROW - 51)
        c = random.randint(50, COL - 51)
        if states[r, c] != 1:
            break
    world.tiles.tileinfos[5*r + 3, 5*c + 2, Ch.TILETYPE] = -1 #Placing Air
    world.tiles.tileinfos[5*r + 3, 5*c + 2, Ch.LIQUIDTYPE] = Liquid.LAVA
    world.tiles.tileinfos[5*r + 3, 5*c + 2, Ch.LIQUIDAMOUNT] = 255
    world.tiles.tileinfos[5*r + 4, 5*c + 2, Ch.TILETYPE] = 379 #Placing bubble to hold liquid
    world.tiles.tileinfos[5*r + 3, 5*c + 1, Ch.TILETYPE] = 379 #Placing bubble to hold liquid
    world.tiles.tileinfos[5*r + 3, 5*c + 3, Ch.TILETYPE] = 379 #Placing bubble to hold liquid#Generate Water
    states[r, c] = 1

#Generate Honey
for _ in range(500):
    while True:
        r = random.randint(50, ROW - 51)
        c = random.randint(50, COL - 51)
        if states[r, c] != 1:
            break
    world.tiles.tileinfos[5*r + 3, 5*c + 2, Ch.TILETYPE] = -1 #Placing Air
    world.tiles.tileinfos[5*r + 3, 5*c + 2, Ch.LIQUIDTYPE] = Liquid.HONEY
    world.tiles.tileinfos[5*r + 3, 5*c + 2, Ch.LIQUIDAMOUNT] = 255
    world.tiles.tileinfos[5*r + 4, 5*c + 2, Ch.TILETYPE] = 379 #Placing bubble to hold liquid
    world.tiles.tileinfos[5*r + 3, 5*c + 1, Ch.TILETYPE] = 379 #Placing bubble to hold liquid
    world.tiles.tileinfos[5*r + 3, 5*c + 3, Ch.TILETYPE] = 379 #Placing bubble to hold liquid
    states[r, c] = 1

world.tiles.exit_editmode()
world.saveV2()