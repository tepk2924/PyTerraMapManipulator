import sys
import os
import random
import numpy as np
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from terrariaworld import TerrariaWorld
from enumeration import GameMode, Channel, Liquid, TileID, ItemID, WallID, ChestUV, Chest2UV
from chest import Item

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
world.tiles.tileinfos[:, :, Channel.TILETYPE] = tile

#Generate Dungeon
'''
Dungeon : 5884 West, 148 Height
'''
world.dungeonY = 458 #Row
world.dungeonX = 1260 #Column
world.tiles.tileinfos[400, 1220:1300, Channel.TILETYPE] = TileID.BlueDungeonBrick
world.tiles.tileinfos[401:458, 1220:1300, Channel.TILETYPE] = -1 #Placing Air
world.tiles.tileinfos[458:460, 1220:1300, Channel.TILETYPE] = TileID.BlueDungeonBrick
states[80:92, 244:260] = 1

#Generate Shimmer Pond
world.tiles.tileinfos[1200:1220, 6200:6400, Channel.TILETYPE] = TileID.Stone #Placing Stone
world.tiles.tileinfos[1200:1205, 6280:6320, Channel.TILETYPE] = -1 #Placing Air to fill shimmer
world.tiles.tileinfos[1200:1205, 6280:6320, Channel.LIQUIDTYPE] = Liquid.SHIMMER
world.tiles.tileinfos[1200:1205, 6280:6320, Channel.LIQUIDAMOUNT] = 255
states[240:244, 1240:1280] = 1

#Generate Temple
world.tiles.tileinfos[1100:1158, 5800:5900, Channel.TILETYPE] = -1 #Placing Air
world.tiles.tileinfos[1100:1160, 5800:5900, Channel.WALL] = WallID.LihzahrdBrickUnsafe #Lih Wall (Mob spawnable)
world.tiles.tileinfos[1158:1160, 5800:5900, Channel.TILETYPE] = TileID.LihzahrdBrick #Placing Lihzarhd Brick
world.place_sprite(1156, 5850, TileID.Lihzahrd, 2, 3) #Placing Lih Altar
world.place_chest(1156, 5830, [Item(stacksize=10, netid=ItemID.LihzahrdPowerCell)], 576, 0) #Placing Chest with 10 Lih Cell
world.place_chest(1156, 5870, [Item(stacksize=10, netid=ItemID.LihzahrdPowerCell)], 576, 0) #Placing Chest with 10 Lih Cell
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
    world.tiles.tileinfos[5*r + 3, 5*c + 2, Channel.TILETYPE] = -1 #Placing Air
    world.tiles.tileinfos[5*r + 3, 5*c + 2, Channel.LIQUIDTYPE] = Liquid.WATER
    world.tiles.tileinfos[5*r + 3, 5*c + 2, Channel.LIQUIDAMOUNT] = 255
    world.tiles.tileinfos[5*r + 4, 5*c + 2, Channel.TILETYPE] = TileID.Bubble #Placing bubble to hold liquid
    world.tiles.tileinfos[5*r + 3, 5*c + 1, Channel.TILETYPE] = TileID.Bubble #Placing bubble to hold liquid
    world.tiles.tileinfos[5*r + 3, 5*c + 3, Channel.TILETYPE] = TileID.Bubble #Placing bubble to hold liquid
    states[r, c] = 1

#Generate Lava
for _ in range(1000):
    while True:
        r = random.randint(0, ROW - 1)
        c = random.randint(50, COL - 51)
        if states[r, c] != 1:
            break
    world.tiles.tileinfos[5*r + 3, 5*c + 2, Channel.TILETYPE] = -1 #Placing Air
    world.tiles.tileinfos[5*r + 3, 5*c + 2, Channel.LIQUIDTYPE] = Liquid.LAVA
    world.tiles.tileinfos[5*r + 3, 5*c + 2, Channel.LIQUIDAMOUNT] = 255
    world.tiles.tileinfos[5*r + 4, 5*c + 2, Channel.TILETYPE] = TileID.Bubble #Placing bubble to hold liquid
    world.tiles.tileinfos[5*r + 3, 5*c + 1, Channel.TILETYPE] = TileID.Bubble #Placing bubble to hold liquid
    world.tiles.tileinfos[5*r + 3, 5*c + 3, Channel.TILETYPE] = TileID.Bubble #Placing bubble to hold liquid
    states[r, c] = 1

#Generate Honey
for _ in range(500):
    while True:
        r = random.randint(0, ROW - 1)
        c = random.randint(50, COL - 51)
        if states[r, c] != 1:
            break
    world.tiles.tileinfos[5*r + 3, 5*c + 2, Channel.TILETYPE] = -1 #Placing Air
    world.tiles.tileinfos[5*r + 3, 5*c + 2, Channel.LIQUIDTYPE] = Liquid.HONEY
    world.tiles.tileinfos[5*r + 3, 5*c + 2, Channel.LIQUIDAMOUNT] = 255
    world.tiles.tileinfos[5*r + 4, 5*c + 2, Channel.TILETYPE] = TileID.Bubble #Placing bubble to hold liquid
    world.tiles.tileinfos[5*r + 3, 5*c + 1, Channel.TILETYPE] = TileID.Bubble #Placing bubble to hold liquid
    world.tiles.tileinfos[5*r + 3, 5*c + 3, Channel.TILETYPE] = TileID.Bubble #Placing bubble to hold liquid
    states[r, c] = 1

#Generating Altars
for _ in range(50):
    while True:
        r = random.randint(0, ROW - 1)
        c = random.randint(50, COL - 51)
        if states[r, c] != 1:
            break
    world.place_sprite(5*r + 1, 5*c + 1, TileID.DemonAltar, 2, 3) #Corruption Altar
    world.tiles.tileinfos[5*r + 3, 5*c + 1:5*c + 4, Channel.TILETYPE] = TileID.Ebonstone #Ebonstone Block
    states[r, c] = 1
for _ in range(50):
    while True:
        r = random.randint(0, ROW - 1)
        c = random.randint(50, COL - 51)
        if states[r, c] != 1:
            break
    world.place_sprite(5*r + 1, 5*c + 1, TileID.DemonAltar, 2, 3, 54, 0) #Crimson Altar
    world.tiles.tileinfos[5*r + 3, 5*c + 1:5*c + 4, Channel.TILETYPE] = TileID.Crimstone #Crimstone Block
    states[r, c] = 1

#Generating Hellforges
for _ in range(25):
    while True:
        r = random.randint(440, ROW - 1)
        c = random.randint(50, COL - 51)
        if states[r, c] != 1:
            break
    world.place_sprite(5*r + 1, 5*c + 1, TileID.Hellforge, 2, 3) #Hellforge
    world.tiles.tileinfos[5*r + 3, 5*c + 1:5*c + 4, Channel.TILETYPE] = TileID.ObsidianBrick #Obsidian Brick
    states[r, c] = 1

#Generating Orbs / Hearts
for _ in range(15):
    while True:
        r = random.randint(0, ROW - 1)
        c = random.randint(50, COL - 51)
        if states[r, c] != 1:
            break
    world.place_sprite(5*r + 1, 5*c + 1, TileID.ShadowOrbs, 2, 2) #Orb
    states[r, c] = 1
for _ in range(15):
    while True:
        r = random.randint(0, ROW - 1)
        c = random.randint(50, COL - 51)
        if states[r, c] != 1:
            break
    world.place_sprite(5*r + 1, 5*c + 1, TileID.ShadowOrbs, 2, 2, 36, 0) #Heart
    states[r, c] = 1

#Generating Biome Chests
while True:
    r = random.randint(0, ROW - 1)
    c = random.randint(50, COL - 51)
    if states[r, c] != 1:
        break
world.place_chest(5*r + 1, 5*c + 1, [Item(stacksize=1, netid=ItemID.VampireKnives)], *ChestUV.CrimsonChestLocked) #Locked Crimson Chest with Vampire Knives
world.tiles.tileinfos[5*r + 3, 5*c + 1:5*c + 3, Channel.TILETYPE] = TileID.BlueDungeonBrick #Dungeon Brick
states[r, c] = 1
while True:
    r = random.randint(0, ROW - 1)
    c = random.randint(50, COL - 51)
    if states[r, c] != 1:
        break
world.place_chest(5*r + 1, 5*c + 1, [Item(stacksize=1, netid=ItemID.StaffoftheFrostHydra)], *ChestUV.FrozenChestLocked) #Locked Ice Chest with Frost Hydra Staff
world.tiles.tileinfos[5*r + 3, 5*c + 1:5*c + 3, Channel.TILETYPE] = TileID.BlueDungeonBrick #Dungeon Brick
states[r, c] = 1
while True:
    r = random.randint(0, ROW - 1)
    c = random.randint(50, COL - 51)
    if states[r, c] != 1:
        break
world.place_chest(5*r + 1, 5*c + 1, [Item(stacksize=1, netid=ItemID.RainbowGun)], *ChestUV.HallowedChestLocked) #Locked Hallow Chest with Rainbow Gun
world.tiles.tileinfos[5*r + 3, 5*c + 1:5*c + 3, Channel.TILETYPE] = TileID.BlueDungeonBrick #Dungeon Brick
states[r, c] = 1
while True:
    r = random.randint(0, ROW - 1)
    c = random.randint(50, COL - 51)
    if states[r, c] != 1:
        break
world.place_chest(5*r + 1, 5*c + 1, [Item(stacksize=1, netid=ItemID.PiranhaGun)], *ChestUV.JungleChestLocked) #Locked Jungle Chest with Piranha Gun
world.tiles.tileinfos[5*r + 3, 5*c + 1:5*c + 3, Channel.TILETYPE] = TileID.BlueDungeonBrick #Dungeon Brick
states[r, c] = 1
while True:
    r = random.randint(0, ROW - 1)
    c = random.randint(50, COL - 51)
    if states[r, c] != 1:
        break
world.place_chest(5*r + 1, 5*c + 1, [Item(stacksize=1, netid=ItemID.ScourgeoftheCorruptor)], *ChestUV.CorruptionChestLocked) #Locked Corruption Chest with Scourge of the Corrupter
world.tiles.tileinfos[5*r + 3, 5*c + 1:5*c + 3, Channel.TILETYPE] = TileID.BlueDungeonBrick #Dungeon Brick
states[r, c] = 1
while True:
    r = random.randint(0, ROW - 1)
    c = random.randint(50, COL - 51)
    if states[r, c] != 1:
        break
world.place_chest_group2(5*r + 1, 5*c + 1, [Item(stacksize=1, netid=ItemID.StormTigerStaff)], *Chest2UV.DesertChestLocked) #Locked Desert Chest with Desert Tiger Staff
world.tiles.tileinfos[5*r + 3, 5*c + 1:5*c + 3, Channel.TILETYPE] = TileID.BlueDungeonBrick #Dungeon Brick
states[r, c] = 1

world.tiles.exit_editmode()
world.save_world()