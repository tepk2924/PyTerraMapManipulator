import sys
import numpy as np
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from terrariaworld import TerrariaWorld
from enumeration import TileID, Channel

world = TerrariaWorld()
loading_path = input(".wld file path to remove queen bee larva : ")
world.load_world(file_path=loading_path)

world.tiles.enter_editmode()

queen_bee_mask = np.where(world.tiles.tileinfos[:, :, Channel.TILETYPE] == TileID.Larva)
queen_bee_mask_row = queen_bee_mask[0]
queen_bee_mask_col = queen_bee_mask[1]

for r, c in zip(queen_bee_mask_row, queen_bee_mask_col):
    world.tiles.tileinfos[r, c, Channel.TILETYPE] = -1
    world.tiles.tileinfos[r, c, Channel.U] = 0
    world.tiles.tileinfos[r, c, Channel.V] = 0

world.tiles.exit_editmode()
saving_path = input("saving queen bee larva-free world path : ")
world.save_world(save_file_path=saving_path)