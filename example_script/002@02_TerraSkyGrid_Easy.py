import sys
import os
import random
import numpy as np
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from terrariaworld import TerrariaWorld
from enumeration import GameMode, Channel, Liquid, TileID, ItemID, WallID, ChestFrameXY, Chest2FrameXY, PrefixID
from chest import Item

world = TerrariaWorld()
world.gamemode = GameMode.MASTER

world.spawnX = 4202
world.spawnY = 397

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

world.tiles.tileinfos[398, 4197, Channel.TILETYPE] = TileID.Grass
world.tiles.tileinfos[398, 4202, Channel.TILETYPE] = TileID.Grass
world.tiles.tileinfos[398, 4207, Channel.TILETYPE] = TileID.Grass
world.tiles.tileinfos[393, 4197, Channel.TILETYPE] = TileID.Grass
world.tiles.tileinfos[393, 4202, Channel.TILETYPE] = TileID.Grass
world.tiles.tileinfos[393, 4207, Channel.TILETYPE] = TileID.Grass

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
world.place_chest_group1(1156, 5830, [Item(stacksize=10, netid=ItemID.LihzahrdPowerCell)], 576, 0) #Placing Chest with 10 Lih Cell
world.place_chest_group1(1156, 5870, [Item(stacksize=10, netid=ItemID.LihzahrdPowerCell)], 576, 0) #Placing Chest with 10 Lih Cell
states[220:232, 1160:1180] = 1

#To spawn-proof
states[79:89, 830:850] = 1

#Generate Water
for _ in range(2000):
    while True:
        r = random.randint(10, ROW - 10)
        c = random.randint(10, COL - 10)
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
        r = random.randint(10, ROW - 10)
        c = random.randint(10, COL - 10)
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
        r = random.randint(10, ROW - 10)
        c = random.randint(10, COL - 10)
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
        r = random.randint(10, ROW - 10)
        c = random.randint(10, COL - 10)
        if states[r, c] != 1:
            break
    world.place_sprite(5*r + 1, 5*c + 1, TileID.DemonAltar, 2, 3) #Corruption Altar
    world.tiles.tileinfos[5*r + 3, 5*c + 1:5*c + 4, Channel.TILETYPE] = TileID.Ebonstone #Ebonstone Block
    states[r, c] = 1
for _ in range(50):
    while True:
        r = random.randint(10, ROW - 10)
        c = random.randint(10, COL - 10)
        if states[r, c] != 1:
            break
    world.place_sprite(5*r + 1, 5*c + 1, TileID.DemonAltar, 2, 3, 54, 0) #Crimson Altar
    world.tiles.tileinfos[5*r + 3, 5*c + 1:5*c + 4, Channel.TILETYPE] = TileID.Crimstone #Crimstone Block
    states[r, c] = 1

#Generating Hellforges
for _ in range(30):
    while True:
        r = random.randint(440, ROW - 10)
        c = random.randint(10, COL - 10)
        if states[r, c] != 1:
            break
    world.place_sprite(5*r + 1, 5*c + 1, TileID.Hellforge, 2, 3) #Hellforge
    world.tiles.tileinfos[5*r + 3, 5*c + 1:5*c + 4, Channel.TILETYPE] = TileID.ObsidianBrick #Obsidian Brick
    states[r, c] = 1

#Generating Orbs / Hearts
for _ in range(20):
    while True:
        r = random.randint(10, ROW - 10)
        c = random.randint(10, COL - 10)
        if states[r, c] != 1:
            break
    world.place_sprite(5*r + 1, 5*c + 1, TileID.ShadowOrbs, 2, 2) #Orb
    states[r, c] = 1
for _ in range(20):
    while True:
        r = random.randint(10, ROW - 10)
        c = random.randint(10, COL - 10)
        if states[r, c] != 1:
            break
    world.place_sprite(5*r + 1, 5*c + 1, TileID.ShadowOrbs, 2, 2, 36, 0) #Heart
    states[r, c] = 1

#Generating Life Crystal
for _ in range(100):
    while True:
        r = random.randint(10, ROW - 10)
        c = random.randint(10, COL - 10)
        if states[r, c] != 1:
            break
    world.place_sprite(5*r + 1, 5*c + 1, TileID.Heart, 2, 2)
    world.tiles.tileinfos[5*r + 3, 5*c + 1:5*c + 3, Channel.TILETYPE] = TileID.Stone
    states[r, c] = 1

#Generating Biome Chests
while True:
    r = random.randint(10, ROW - 10)
    c = random.randint(10, COL - 10)
    if states[r, c] != 1:
        break
world.place_chest_group1(5*r + 1, 5*c + 1, [Item(stacksize=1, netid=ItemID.VampireKnives)], *ChestFrameXY.CrimsonChestLocked) #Locked Crimson Chest with Vampire Knives
world.tiles.tileinfos[5*r + 3, 5*c + 1:5*c + 3, Channel.TILETYPE] = TileID.BlueDungeonBrick #Dungeon Brick
states[r, c] = 1
while True:
    r = random.randint(10, ROW - 10)
    c = random.randint(10, COL - 10)
    if states[r, c] != 1:
        break
world.place_chest_group1(5*r + 1, 5*c + 1, [Item(stacksize=1, netid=ItemID.StaffoftheFrostHydra)], *ChestFrameXY.FrozenChestLocked) #Locked Ice Chest with Frost Hydra Staff
world.tiles.tileinfos[5*r + 3, 5*c + 1:5*c + 3, Channel.TILETYPE] = TileID.BlueDungeonBrick #Dungeon Brick
states[r, c] = 1
while True:
    r = random.randint(10, ROW - 10)
    c = random.randint(10, COL - 10)
    if states[r, c] != 1:
        break
world.place_chest_group1(5*r + 1, 5*c + 1, [Item(stacksize=1, netid=ItemID.RainbowGun)], *ChestFrameXY.HallowedChestLocked) #Locked Hallow Chest with Rainbow Gun
world.tiles.tileinfos[5*r + 3, 5*c + 1:5*c + 3, Channel.TILETYPE] = TileID.BlueDungeonBrick #Dungeon Brick
states[r, c] = 1
while True:
    r = random.randint(10, ROW - 10)
    c = random.randint(10, COL - 10)
    if states[r, c] != 1:
        break
world.place_chest_group1(5*r + 1, 5*c + 1, [Item(stacksize=1, netid=ItemID.PiranhaGun)], *ChestFrameXY.JungleChestLocked) #Locked Jungle Chest with Piranha Gun
world.tiles.tileinfos[5*r + 3, 5*c + 1:5*c + 3, Channel.TILETYPE] = TileID.BlueDungeonBrick #Dungeon Brick
states[r, c] = 1
while True:
    r = random.randint(10, ROW - 10)
    c = random.randint(10, COL - 10)
    if states[r, c] != 1:
        break
world.place_chest_group1(5*r + 1, 5*c + 1, [Item(stacksize=1, netid=ItemID.ScourgeoftheCorruptor)], *ChestFrameXY.CorruptionChestLocked) #Locked Corruption Chest with Scourge of the Corrupter
world.tiles.tileinfos[5*r + 3, 5*c + 1:5*c + 3, Channel.TILETYPE] = TileID.BlueDungeonBrick #Dungeon Brick
states[r, c] = 1
while True:
    r = random.randint(10, ROW - 10)
    c = random.randint(10, COL - 10)
    if states[r, c] != 1:
        break
world.place_chest_group2(5*r + 1, 5*c + 1, [Item(stacksize=1, netid=ItemID.StormTigerStaff)], *Chest2FrameXY.DesertChestLocked) #Locked Desert Chest with Desert Tiger Staff
world.tiles.tileinfos[5*r + 3, 5*c + 1:5*c + 3, Channel.TILETYPE] = TileID.BlueDungeonBrick #Dungeon Brick
states[r, c] = 1

#Generating Surface Loot Chest
surface_loot_pool = [
    Item(stacksize=1, netid=ItemID.Spear),
    Item(stacksize=1, netid=ItemID.Blowpipe),
    Item(stacksize=1, netid=ItemID.WoodenBoomerang),
    Item(stacksize=1, netid=ItemID.Aglet),
    Item(stacksize=1, netid=ItemID.ClimbingClaws),
    Item(stacksize=1, netid=ItemID.Umbrella),
    Item(stacksize=1, netid=ItemID.CordageGuide),
    Item(stacksize=1, netid=ItemID.WandofSparking),
    Item(stacksize=1, netid=ItemID.Radar),
    Item(stacksize=1, netid=ItemID.PortableStool),
]
for idx in range(30):
    while True:
        r = random.randint(20, 120)
        c = random.randint(10, COL - 10)
        if states[r, c] != 1:
            break
    world.place_chest_group1(5*r + 1, 5*c + 1, [surface_loot_pool[idx%10]], *ChestFrameXY.WoodenChest)
    world.tiles.tileinfos[5*r + 3, 5*c + 1:5*c + 3, Channel.TILETYPE] = TileID.Grass
    states[r, c] = 1

#Generating Underground + Cavern Loot Chest
underground_loot_pool = [
    Item(stacksize=1, netid=ItemID.Extractinator),
    Item(stacksize=1, netid=ItemID.BandofRegeneration),
    Item(stacksize=1, netid=ItemID.MagicMirror),
    Item(stacksize=1, netid=ItemID.CloudinaBottle),
    Item(stacksize=1, netid=ItemID.HermesBoots),
    Item(stacksize=1, netid=ItemID.Mace),
    Item(stacksize=1, netid=ItemID.ShoeSpikes),
]
for idx in range(119):
    while True:
        r = random.randint(120, 440)
        c = random.randint(10, COL - 10)
        if states[r, c] != 1:
            break
    world.place_chest_group1(5*r + 1, 5*c + 1, [underground_loot_pool[idx%7]], *ChestFrameXY.GoldChest)
    world.tiles.tileinfos[5*r + 3, 5*c + 1:5*c + 3, Channel.TILETYPE] = TileID.Stone
    states[r, c] = 1

#Generating Sky Loot Chest
sky_loot_pool = [
    Item(stacksize=1, netid=ItemID.Starfury),
    Item(stacksize=1, netid=ItemID.LuckyHorseshoe),
    Item(stacksize=1, netid=ItemID.CelestialMagnet),
    Item(stacksize=1, netid=ItemID.SkyMill),
]
for idx in range(12):
    while True:
        r = random.randint(10, 20)
        c = random.randint(10, COL - 10)
        if states[r, c] != 1:
            break
    world.place_chest_group1(5*r + 1, 5*c + 1, [sky_loot_pool[idx%4]], *ChestFrameXY.SkywareChest)
    world.tiles.tileinfos[5*r + 3, 5*c + 1:5*c + 3, Channel.TILETYPE] = TileID.Sunplate
    states[r, c] = 1

#Generating Desert Loot Chest
desert_loot_pool = [
    Item(stacksize=1, netid=ItemID.MagicConch),
    Item(stacksize=1, netid=ItemID.MysticCoilSnake),
    Item(stacksize=1, netid=ItemID.AncientChisel),
    Item(stacksize=1, netid=ItemID.SandBoots),
    Item(stacksize=1, netid=ItemID.ThunderSpear),
    Item(stacksize=1, netid=ItemID.ThunderStaff),
    Item(stacksize=1, netid=ItemID.CatBast)
]
for idx in range(21):
    while True:
        r = random.randint(120, 440)
        c = random.randint(10, COL - 10)
        if states[r, c] != 1:
            break
    world.place_chest_group2(5*r + 1, 5*c + 1, [desert_loot_pool[idx%7]], *Chest2FrameXY.DesertChest)
    world.tiles.tileinfos[5*r + 3, 5*c + 1:5*c + 3, Channel.TILETYPE] = TileID.Sandstone
    states[r, c] = 1

#Generating Jungle Loot Chest
jungle_loot_pool = [
    Item(stacksize=1, netid=ItemID.FeralClaws),
    Item(stacksize=1, netid=ItemID.AnkletoftheWind),
    Item(stacksize=1, netid=ItemID.StaffofRegrowth),
    Item(stacksize=1, netid=ItemID.Boomstick),
    Item(stacksize=1, netid=ItemID.FlowerBoots),
    Item(stacksize=1, netid=ItemID.FiberglassFishingPole),
    Item(stacksize=1, netid=ItemID.Seaweed),
]
for idx in range(21):
    while True:
        r = random.randint(120, 440)
        c = random.randint(10, COL - 10)
        if states[r, c] != 1:
            break
    world.place_chest_group1(5*r + 1, 5*c + 1, [jungle_loot_pool[idx%7]], *ChestFrameXY.IvyChest)
    world.tiles.tileinfos[5*r + 3, 5*c + 1:5*c + 3, Channel.TILETYPE] = TileID.JungleGrass
    states[r, c] = 1

world.tiles.exit_editmode()
world.save_world("TerraSkyGrid_Easy")