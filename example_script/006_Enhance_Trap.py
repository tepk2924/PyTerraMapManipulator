import random
import numpy as np
import os
import sys
import multiprocessing
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from terrariaworld import TerrariaWorld
from enumeration import ItemID, TileID, Channel, BrickStyle, WallID, Liquid
from chest import Item

def main():
    input_path = input("월드 .wld파일 드래그해서 여기에 드롭, 또는 경로 입력 : ")
    dirname = os.path.dirname(input_path)
    base, extension = os.path.splitext(os.path.basename(input_path))

    output_path = os.path.join(dirname, base + "_TrapEnhanced" + extension)

    world = TerrariaWorld()
    world.load_world(file_path = input_path)

    if world.zenithworld or world.remixworld:
        raise ValueError("제니스 시드나 리믹스 시드에서는 실행 불가능. 닫으려면 엔터 누르기.")

    new_title = world.title + "_TrapEnhanced"
    world.title = new_title
    world.notrapworld = True

    dungeonR = world.dungeonY
    dungeonC = world.dungeonX

    world.tiles.enter_editmode()
    H, W = world.tileshigh, world.tileswide

    ground_level = int(world.groundlevel)

    #1. All Pressure Plates are invisible
    world.tiles.tileinfos[world.tiles.tileinfos[:, :, Channel.TILETYPE] == TileID.PressurePlates, Channel.INVISIBLEBLOCK] = 1

    #2. All dart traps are invisible
    dart_trap_mask = world.tiles.tileinfos[:, :, Channel.TILETYPE] == TileID.Traps
    world.tiles.tileinfos[dart_trap_mask, Channel.INVISIBLEBLOCK] = 1

    #3. All regular dart traps are upgraded to venomous ones
    regular_dart_trap_mask = dart_trap_mask & (world.tiles.tileinfos[:, :, Channel.FRAMEY] == 0)
    world.tiles.tileinfos[regular_dart_trap_mask, Channel.FRAMEY] = 90

    #4. Some dart traps spawns Queen bee
    left_looking_dart_trap_mask = np.where(dart_trap_mask & (world.tiles.tileinfos[:, :, Channel.FRAMEX] == 0) == True)
    right_looking_dart_trap_mask = np.where(dart_trap_mask & (world.tiles.tileinfos[:, :, Channel.FRAMEX] == 18) == True)
    queenbee_cnt = int(20*H*W/(8400*2400)) #Large : 20 Queen bees each
    for _ in range(queenbee_cnt):
        a = random.randint(0, len(left_looking_dart_trap_mask[0]) - 1)
        r, c = left_looking_dart_trap_mask[0][a] - 2, left_looking_dart_trap_mask[1][a] - 3
        world.place_sprite(r, c, TileID.Larva, 3, 3)
        world.tiles.tileinfos[r + 3, c:c + 3, Channel.TILETYPE] = TileID.Platforms
        world.tiles.tileinfos[r + 3, c:c + 3, Channel.FRAMEX] = 0
        world.tiles.tileinfos[r + 3, c:c + 3, Channel.FRAMEY] = 0
        world.tiles.tileinfos[r:r + 4, c:c + 3, Channel.INVISIBLEBLOCK] = 1
        b = random.randint(0, len(right_looking_dart_trap_mask[0]) - 1)
        r, c = right_looking_dart_trap_mask[0][b] - 2, right_looking_dart_trap_mask[1][b] + 1
        world.place_sprite(r, c, TileID.Larva, 3, 3)
        world.tiles.tileinfos[r + 3, c:c + 3, Channel.TILETYPE] = TileID.Platforms
        world.tiles.tileinfos[r + 3, c:c + 3, Channel.FRAMEX] = 0
        world.tiles.tileinfos[r + 3, c:c + 3, Channel.FRAMEY] = 0
        world.tiles.tileinfos[r:r + 4, c:c + 3, Channel.INVISIBLEBLOCK] = 1

    #5. Dungeon Entrance is blocked by lizahrd bricks.
    dungeon_partition = world.tiles.tileinfos[dungeonR - 50:dungeonR + 50, dungeonC - 50:dungeonC + 50, :]
    #5-1. inactive dungeon brick is gone
    inactive_brick_mask = dungeon_partition[:, :, Channel.INACTIVE] == 1
    dungeon_partition[inactive_brick_mask, Channel.INACTIVE] = 0
    dungeon_partition[inactive_brick_mask, Channel.TILETYPE] = TileID.Air
    #5-2. all non_dungeonbrick is gone
    non_brick_mask = (dungeon_partition[:, :, Channel.TILETYPE] != TileID.BlueDungeonBrick) & (dungeon_partition[:, :, Channel.TILETYPE] != TileID.PinkDungeonBrick) & (dungeon_partition[:, :, Channel.TILETYPE] != TileID.GreenDungeonBrick)
    dungeon_partition[non_brick_mask, Channel.FRAMEX] = 0
    dungeon_partition[non_brick_mask, Channel.FRAMEY] = 0
    dungeon_partition[non_brick_mask, Channel.TILETYPE] = TileID.Air
    dungeon_partition[non_brick_mask, Channel.BRICKSTYLE] = BrickStyle.FULL
    #5-3. Fill the air with lihzahrd brick
    dungeon_partition[dungeon_partition[:, :, Channel.TILETYPE] == TileID.Air, Channel.TILETYPE] = TileID.LihzahrdBrick
    for idx in range(100):
        for jdx in range(100):
            if dungeon_partition[idx, jdx, Channel.TILETYPE] == TileID.LihzahrdBrick and not (45 <= idx < 55 and 45 <= jdx < 55):
                dungeon_partition[idx, jdx, Channel.BRICKSTYLE] = random.choice([BrickStyle.SLOPEBOTTOMLEFT, BrickStyle.SLOPEBOTTOMRIGHT, BrickStyle.SLOPETOPLEFT, BrickStyle.SLOPETOPRIGHT])

    #6. Creating Logic Sensor Mines
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
        world.place_logic_sensor(r + 5, c, "player_above")
        world.tiles.tileinfos[r + 5, c, Channel.INVISIBLEBLOCK] = 1
        world.tiles.tileinfos[r:r + 6, c, Channel.WIREBLUE] = 1

    #7. All Chest contains Gas Trap & Remove Dead Man's Sweater
    for chest in world.chests:
        for idx in range(40):
            if chest.items[idx].netid == ItemID.DeadMansSweater:
                chest.items[idx] = Item(stacksize=0, netid=ItemID.NoItem)
        chest.items[39] = Item(stacksize=1, netid=ItemID.GasTrap)

    #8. Surface Mines
    mine_cnt = int(400*W/8400) #Large : 400 mines
    block_list = [TileID.Grass, TileID.Dirt, TileID.Sand, TileID.JungleGrass, TileID.SnowBlock, TileID.IceBlock, TileID.CorruptGrass, TileID.CrimsonGrass, TileID.Ebonstone, TileID.Crimstone, TileID.Ebonsand, TileID.Crimsand]
    plant_list = [TileID.Plants, TileID.CorruptPlants, TileID.CrimsonPlants]
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
            if world.tiles.tileinfos[r, c, Channel.TILETYPE] in plant_list:
                world.tiles.tileinfos[r, c, Channel.FRAMEX] = 0
                world.tiles.tileinfos[r, c, Channel.FRAMEY] = 0
                r += 1
                break
        world.tiles.tileinfos[r - 1, c, Channel.TILETYPE] = TileID.LandMine
        world.tiles.tileinfos[r - 1, c, Channel.INVISIBLEBLOCK] = 1
        world.tiles.tileinfos[r, c, Channel.BRICKSTYLE] = BrickStyle.FULL

    #9. Torch God Trap
    torch_god_cnt = int(20*H*W/(8400*2400))
    for _ in range(torch_god_cnt):
        r_center, c_center = random.randint(ground_level + 50, H - 200), random.randint(100, W - 100)
        area = world.tiles.tileinfos[r_center - 50:r_center + 51, c_center - 50: c_center + 51, :]
        for _ in range(2000):
            r, c = random.randint(0, 100), random.randint(0, 100)
            if area[r, c, Channel.TILETYPE] == TileID.Air and area[r, c, Channel.LIQUIDAMOUNT] == 0:
                area[r, c, Channel.TILETYPE] = TileID.Torches
                area[r, c, Channel.FRAMEX] = 0
                area[r, c, Channel.FRAMEY] = 0
                area[r, c, Channel.INVISIBLEBLOCK] = 1
                if area[r, c, Channel.WALL] == WallID.Air:
                    area[r, c, Channel.WALL] = WallID.Stone
                    area[r, c, Channel.INVISIBLEWALL] = 1
                
    #10. Invisible Lava Bubbles
    lava_bubble_cnt = int(1000*H*W/(8400*2400))
    for _ in range(lava_bubble_cnt):
        while True:
            r, c = random.randint(50, ground_level), random.randint(50, W - 50)
            if world.tiles.tileinfos[r, c, Channel.TILETYPE] == TileID.Air:
                break
        world.tiles.tileinfos[r, c, Channel.TILETYPE] = TileID.Bubble
        world.tiles.tileinfos[r, c, Channel.LIQUIDTYPE] = Liquid.LAVA
        world.tiles.tileinfos[r, c, Channel.LIQUIDAMOUNT] = 255
        world.tiles.tileinfos[r, c, Channel.INVISIBLEBLOCK] = 1

    #11. Boulders rain down every night
    world.time = 13500.0
    boulder_cnt = 250
    base_H = 20
    start_c = int(world.spawnX) - 3*boulder_cnt//2
    if start_c < 0:
        start_c = 0
    over = start_c + 3*boulder_cnt - (W - 1)
    if over > 0:
        start_c -= over
    for idx in range(boulder_cnt):
        world.place_sprite(base_H + 2, start_c + 3*idx, TileID.BoulderStatue, 3, 2)
    world.tiles.tileinfos[base_H + 1, start_c:start_c + 3*boulder_cnt, Channel.TILETYPE] = TileID.Stone
    world.tiles.tileinfos[base_H + 1:base_H + 5, start_c:start_c + 3*boulder_cnt, Channel.INVISIBLEBLOCK] = 1
    world.place_logic_sensor(base_H, start_c, "night")
    world.tiles.tileinfos[base_H, start_c, Channel.INVISIBLEBLOCK] = 1
    world.tiles.tileinfos[base_H + 2, start_c:start_c + 3*boulder_cnt, Channel.WIREYELLOW] = 1
    world.tiles.tileinfos[base_H:base_H + 2, start_c, Channel.WIREYELLOW] = 1

    #12. All normal boulders are converted to bouncy boulders.
    world.tiles.tileinfos[world.tiles.tileinfos[:, :, Channel.TILETYPE] == TileID.Boulder, Channel.TILETYPE] = TileID.BouncyBoulder
    
    world.tiles.exit_editmode()

    world.save_world(save_file_path = output_path, process_units=multiprocessing.cpu_count())
    input("월드 생성 완료. 프로그램을 닫으려면 엔터 누르기...")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        input("프로그램을 닫으려면 엔터 누르기...")