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
                 sprite_number:int,
                 sprite_rownum:int,
                 sprite_colnum:int,
                 U_shift:int=0,
                 V_shift:int=0):
    world.tiles.tileinfos[row:row + sprite_rownum, col:col + sprite_colnum, Ch.TILETYPE] = sprite_number
    for r in range(sprite_rownum):
        for c in range(sprite_colnum):
            world.tiles.tileinfos[row + r, col + c, Ch.U] = 18*c + U_shift
            world.tiles.tileinfos[row + r, col + c, Ch.V] = 18*r + V_shift

def Place_Chest(world:TerrariaWorld,
                row:int,
                col:int,
                itemnum:int,
                itemcnt:int=1,
                U_shift:int=0,
                V_shift:int=0):
    Place_Sprite(world, row, col, 21, 2, 2, U_shift, V_shift)
    chest = Chest(col, row, "")
    chest.items[0].netid = itemnum
    chest.items[0].stacksize = itemcnt
    world.chests.append(chest)

def Place_Chest_Group2(world:TerrariaWorld,
                       row:int,
                       col:int,
                       itemnum:int,
                       itemcnt:int=1,
                       U_shift:int=0,
                       V_shift:int=0):
    Place_Sprite(world, row, col, 467, 2, 2, U_shift, V_shift)
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
world.tiles.tileinfos[1100:1160, 5800:5900, Ch.WALL] = 87 #Lih Wall (Mob spawnable)
world.tiles.tileinfos[1158:1160, 5800:5900, Ch.TILETYPE] = 226 #Placing Lihzarhd Brick
Place_Sprite(world, 1156, 5850, 237, 2, 3) #Placing Lih Altar
Place_Chest(world, 1156, 5830, 1293, 10, 576, 0) #Placing Chest with 10 Lih Cell
Place_Chest(world, 1156, 5870, 1293, 10, 576, 0) #Placing Chest with 10 Lih Cell
states[220:232, 1160:1180] = 1

#To spawn-proof
states[79:89, 830:850] = 1

#Generate Water
for _ in range(2000):
    while True:
        r = random.randint(0, ROW - 1)
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
        r = random.randint(0, ROW - 1)
        c = random.randint(50, COL - 51)
        if states[r, c] != 1:
            break
    world.tiles.tileinfos[5*r + 3, 5*c + 2, Ch.TILETYPE] = -1 #Placing Air
    world.tiles.tileinfos[5*r + 3, 5*c + 2, Ch.LIQUIDTYPE] = Liquid.LAVA
    world.tiles.tileinfos[5*r + 3, 5*c + 2, Ch.LIQUIDAMOUNT] = 255
    world.tiles.tileinfos[5*r + 4, 5*c + 2, Ch.TILETYPE] = 379 #Placing bubble to hold liquid
    world.tiles.tileinfos[5*r + 3, 5*c + 1, Ch.TILETYPE] = 379 #Placing bubble to hold liquid
    world.tiles.tileinfos[5*r + 3, 5*c + 3, Ch.TILETYPE] = 379 #Placing bubble to hold liquid
    states[r, c] = 1

#Generate Honey
for _ in range(500):
    while True:
        r = random.randint(0, ROW - 1)
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

#Generating Altars
for _ in range(50):
    while True:
        r = random.randint(0, ROW - 1)
        c = random.randint(50, COL - 51)
        if states[r, c] != 1:
            break
    Place_Sprite(world, 5*r + 1, 5*c + 1, 26, 2, 3) #Corruption Altar
    world.tiles.tileinfos[5*r + 3, 5*c + 1:5*c + 4, Ch.TILETYPE] = 25 #Ebonstone Block
    states[r, c] = 1
for _ in range(50):
    while True:
        r = random.randint(0, ROW - 1)
        c = random.randint(50, COL - 51)
        if states[r, c] != 1:
            break
    Place_Sprite(world, 5*r + 1, 5*c + 1, 26, 2, 3, 54, 0) #Corruption Altar
    world.tiles.tileinfos[5*r + 3, 5*c + 1:5*c + 4, Ch.TILETYPE] = 203 #Crimstone Block
    states[r, c] = 1

#Generating Hellforges
for _ in range(25):
    while True:
        r = random.randint(440, ROW - 1)
        c = random.randint(50, COL - 51)
        if states[r, c] != 1:
            break
    Place_Sprite(world, 5*r + 1, 5*c + 1, 77, 2, 3) #Hellforge
    world.tiles.tileinfos[5*r + 3, 5*c + 1:5*c + 4, Ch.TILETYPE] = 75 #Obsidian Brick
    states[r, c] = 1

#Generating Orbs / Hearts
for _ in range(15):
    while True:
        r = random.randint(0, ROW - 1)
        c = random.randint(50, COL - 51)
        if states[r, c] != 1:
            break
    Place_Sprite(world, 5*r + 1, 5*c + 1, 31, 2, 2) #Orb
    states[r, c] = 1
for _ in range(15):
    while True:
        r = random.randint(0, ROW - 1)
        c = random.randint(50, COL - 51)
        if states[r, c] != 1:
            break
    Place_Sprite(world, 5*r + 1, 5*c + 1, 31, 2, 2, 36, 0) #Heart
    states[r, c] = 1

#Generating Biome Chests
while True:
    r = random.randint(0, ROW - 1)
    c = random.randint(50, COL - 51)
    if states[r, c] != 1:
        break
Place_Chest(world, 5*r + 1, 5*c + 1, 1569, 1, 900, 0) #Locked Crimson Chest with Vampire Knives
world.tiles.tileinfos[5*r + 3, 5*c + 1:5*c + 3, Ch.TILETYPE] = 41 #Dungeon Brick
states[r, c] = 1
while True:
    r = random.randint(0, ROW - 1)
    c = random.randint(50, COL - 51)
    if states[r, c] != 1:
        break
Place_Chest(world, 5*r + 1, 5*c + 1, 1572, 1, 972, 0) #Locked Ice Chest with Frost Hydra Staff
world.tiles.tileinfos[5*r + 3, 5*c + 1:5*c + 3, Ch.TILETYPE] = 41 #Dungeon Brick
states[r, c] = 1
while True:
    r = random.randint(0, ROW - 1)
    c = random.randint(50, COL - 51)
    if states[r, c] != 1:
        break
Place_Chest(world, 5*r + 1, 5*c + 1, 1260, 1, 936, 0) #Locked Hallow Chest with Rainbow Gun
world.tiles.tileinfos[5*r + 3, 5*c + 1:5*c + 3, Ch.TILETYPE] = 41 #Dungeon Brick
states[r, c] = 1
while True:
    r = random.randint(0, ROW - 1)
    c = random.randint(50, COL - 51)
    if states[r, c] != 1:
        break
Place_Chest(world, 5*r + 1, 5*c + 1, 1156, 1, 828, 0) #Locked Jungle Chest with Piranha Gun
world.tiles.tileinfos[5*r + 3, 5*c + 1:5*c + 3, Ch.TILETYPE] = 41 #Dungeon Brick
states[r, c] = 1
while True:
    r = random.randint(0, ROW - 1)
    c = random.randint(50, COL - 51)
    if states[r, c] != 1:
        break
Place_Chest(world, 5*r + 1, 5*c + 1, 1571, 1, 864, 0) #Locked Corruption Chest with Scourge of the Corrupter
world.tiles.tileinfos[5*r + 3, 5*c + 1:5*c + 3, Ch.TILETYPE] = 41 #Dungeon Brick
states[r, c] = 1
while True:
    r = random.randint(0, ROW - 1)
    c = random.randint(50, COL - 51)
    if states[r, c] != 1:
        break
Place_Chest_Group2(world, 5*r + 1, 5*c + 1, 4607, 1, 468, 0) #Locked Desert Chest with Desert Tiger Staff
world.tiles.tileinfos[5*r + 3, 5*c + 1:5*c + 3, Ch.TILETYPE] = 41 #Dungeon Brick
states[r, c] = 1

world.tiles.exit_editmode()
world.saveV2()