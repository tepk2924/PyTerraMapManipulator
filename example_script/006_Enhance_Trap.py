import random
import numpy as np
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from terrariaworld import TerrariaWorld
from enumeration import ItemID, TileID, Channel, BrickStyle
from chest import Item

input_path = input("Drag and Drop : ")
dirname = os.path.dirname(input_path)
base, extension = os.path.splitext(os.path.basename(input_path))

output_path = os.path.join(dirname, base + "_TrapEnhanced" + extension)

world = TerrariaWorld()
world.load_world(file_path = input_path)

new_title = world.title + "_TrapEnhanced"
world.title = new_title
world.notrapworld = True

dungeonR = world.dungeonY
dungeonC = world.dungeonX

world.tiles.enter_editmode()
H, W = world.tileshigh, world.tileswide

#1. All Pressure Plates are invisible
world.tiles.tileinfos[world.tiles.tileinfos[:, :, Channel.TILETYPE] == TileID.PressurePlates, Channel.INVISIBLEBLOCK] = 1

#2. All dart traps are invisible
dart_trap_mask = world.tiles.tileinfos[:, :, Channel.TILETYPE] == TileID.Traps
world.tiles.tileinfos[dart_trap_mask, Channel.INVISIBLEBLOCK] = 1

#3. All regular dart traps are upgraded to venomous ones
regular_dart_trap_mask = dart_trap_mask & (world.tiles.tileinfos[:, :, Channel.FRAMEY] == 0)
world.tiles.tileinfos[regular_dart_trap_mask, Channel.FRAMEY] = 90

#4. Dungeon Entrance is blocked by lizahrd bricks.
dungeon_partition = world.tiles.tileinfos[dungeonR - 50:dungeonR + 50, dungeonC - 50:dungeonC + 50, :]
#4-1. inactive dungeon brick is gone
inactive_brick_mask = dungeon_partition[:, :, Channel.INACTIVE] == 1
dungeon_partition[inactive_brick_mask, Channel.INACTIVE] = 0
dungeon_partition[inactive_brick_mask, Channel.TILETYPE] = TileID.Air
#4-2. all non_dungeonbrick is gone
non_brick_mask = (dungeon_partition[:, :, Channel.TILETYPE] != TileID.BlueDungeonBrick) & (dungeon_partition[:, :, Channel.TILETYPE] != TileID.PinkDungeonBrick) & (dungeon_partition[:, :, Channel.TILETYPE] != TileID.GreenDungeonBrick)
dungeon_partition[non_brick_mask, Channel.FRAMEX] = 0
dungeon_partition[non_brick_mask, Channel.FRAMEY] = 0
dungeon_partition[non_brick_mask, Channel.TILETYPE] = TileID.Air
dungeon_partition[non_brick_mask, Channel.BRICKSTYLE] = BrickStyle.FULL
#4-3. Fill the air with lihzahrd brick
dungeon_partition[dungeon_partition[:, :, Channel.TILETYPE] == TileID.Air, Channel.TILETYPE] = TileID.LihzahrdBrick

#5. Creating Logic Sensor Mines
mine_cnt = int(1000*H*W/(8400*2400)) #Large : 1000 mines
block_list = [TileID.Dirt, TileID.Stone, TileID.Mud, TileID.Sandstone, TileID.HardenedSand, TileID.SnowBlock, TileID.IceBlock]
for _ in range(mine_cnt):
    while True:
        r, c = random.randint(50, H - 50), random.randint(50, W - 50)
        if world.tiles.tileinfos[r - 1, c, Channel.TILETYPE] in block_list and \
           world.tiles.tileinfos[r, c, Channel.TILETYPE] in block_list and \
           world.tiles.tileinfos[r + 1, c, Channel.TILETYPE] in block_list and \
           world.tiles.tileinfos[r + 4, c, Channel.TILETYPE] in block_list and \
           world.tiles.tileinfos[r + 5, c, Channel.TILETYPE] in block_list:
            break
    world.tiles.tileinfos[r, c, Channel.TILETYPE] = TileID.Explosives
    world.tiles.tileinfos[r, c, Channel.INVISIBLEBLOCK] = 1
    world.place_logic_player_above(r + 5, c)
    world.tiles.tileinfos[r + 5, c, Channel.INVISIBLEBLOCK] = 1
    world.tiles.tileinfos[r:r + 6, c, Channel.WIREBLUE] = 1

#6. All Chest contains Gas Trap
for chest in world.chests:
    chest.items[39] = Item(stacksize=1, netid=ItemID.GasTrap)

#7. Surface Mines
mine_cnt = int(200*W/8400) #Large : 200 mines
block_list = [TileID.Grass, TileID.Dirt, TileID.Sand, TileID.JungleGrass, TileID.SnowBlock, TileID.IceBlock, TileID.CorruptGrass, TileID.CrimsonGrass]
for _ in range(mine_cnt):
    while True:
        c = random.randint(50, W - 50)
        r = 1
        while True:
            if world.tiles.tileinfos[r, c, Channel.TILETYPE] != TileID.Air:
                break
            r += 1
        if world.tiles.tileinfos[r, c, Channel.TILETYPE] in block_list:
            break
    world.tiles.tileinfos[r - 1, c, Channel.TILETYPE] = TileID.LandMine
    world.tiles.tileinfos[r - 1, c, Channel.INVISIBLEBLOCK] = 1
    world.tiles.tileinfos[r, c, Channel.BRICKSTYLE] = BrickStyle.FULL

world.tiles.exit_editmode()

world.save_world(save_file_path = output_path)