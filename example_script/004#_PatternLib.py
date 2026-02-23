import sys
import numpy as np
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from terrariaworld import TerrariaWorld
from enumeration import WallID, Channel, Paint
from draw import vec2, line_seg_mask

def draw_line_seg(arr:np.ndarray,
                  pt1:vec2,
                  pt2:vec2) -> None:
    arr[*line_seg_mask(pt1, pt2)] = 1

def export_pattern(result:np.ndarray,
                   color_scheme:np.ndarray,
                   world_name:str,
                   process_units:int=1) -> None:
    rows, cols = result.shape
    result = np.where(result >= 1, 1, 0)
    color_scheme = color_scheme*result
    color_scheme = np.where(color_scheme == 0, Paint.NEGATIVE, color_scheme)

    MARGIN = 50
    world = TerrariaWorld(world_size = (MARGIN + rows + MARGIN, MARGIN + cols + MARGIN))
    world.tiles.enter_editmode()
    world.spawnX = MARGIN + cols//2
    world.spawnY = MARGIN + rows//2

    world.tiles.tileinfos[MARGIN:MARGIN + rows, MARGIN:MARGIN + cols, Channel.WALL] = WallID.DiamondGemspark
    world.tiles.tileinfos[MARGIN:MARGIN + rows, MARGIN:MARGIN + cols, Channel.WALLCOLOR] = color_scheme
    world.tiles.exit_editmode()

    world.save_world(world_name + ".wld", process_units)