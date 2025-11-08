import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from terrariaworld import TerrariaWorld
from enumeration import Channel, WallID
import cv2
import numpy as np

RGBcolor_on_diamond_gemspark = {
    0: "#B5B5C0",
    1: "#C85A69",
    2: "#C89369",
    3: "#C8CE69",
    4: "#8DCE69",
    5: "#54CE69",
    6: "#54CEA5",
    7: "#54CEE4",
    8: "#5493E4",
    9: "#545AE4",
    10: "#8D5AE4",
    11: "#C85AE4",
    12: "#C85AA5",
    13: "#C8333F",
    14: "#C8803F",
    15: "#C8CE3F",
    16: "#7ACE3F",
    17: "#2DCE3F",
    18: "#2DCE91",
    19: "#2DCEE4",
    20: "#2D80E4",
    21: "#2D33E4",
    22: "#7A33E4",
    23: "#C833E4",
    24: "#C83391",
    25: "#5A6070",
    26: "#C8CEE4",
    27: "#979DB0",
    28: "#C89F8F",
    29: "#262628",
    30: "#131816"
}

RGB_pallette = []

for idx in range(31):
    RGBinfo = RGBcolor_on_diamond_gemspark[idx][1:]
    R = int(RGBinfo[:2], 16)
    G = int(RGBinfo[2:4], 16)
    B = int(RGBinfo[4:], 16)
    RGB_pallette.append([R, G, B])

RGB_pallette_np = np.expand_dims(np.array(RGB_pallette, np.uint8), axis=1)

LAB_pallette_np = cv2.cvtColor(RGB_pallette_np, cv2.COLOR_RGB2LAB)


LAB_image_np = cv2.cvtColor(np.array(cv2.imread(input("file path : "), cv2.IMREAD_COLOR_RGB)), cv2.COLOR_RGB2LAB)
image_row, image_col, _ = LAB_image_np.shape

calculation1 = np.ndarray((image_row, image_col, 3, 31), np.int32)

calculation2 = np.tile(np.expand_dims(LAB_image_np, axis=-1), (1, 1, 1, 31))

for idx in range(31):
    calculation1[:, :, :, idx] = np.tile(np.expand_dims(np.expand_dims(LAB_pallette_np[idx], axis=0), axis=0), (image_row, image_col, 1))

err = np.sum((calculation1 - calculation2)**2, axis=2)
color = np.argmin(err, axis=2)

world = TerrariaWorld()

world.tiles.enter_editmode()

MINROW = 200
MINCOL = 4200 - image_col//2

world.tiles.tileinfos[MINROW:MINROW + image_row, MINCOL:MINCOL + image_col, Channel.WALL] = WallID.DiamondGemspark #diamond gemspark wall
world.tiles.tileinfos[MINROW:MINROW + image_row, MINCOL:MINCOL + image_col, Channel.WALLCOLOR] = color #setting color

world.tiles.exit_editmode()

world.save_world()