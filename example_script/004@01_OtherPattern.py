import sys
import numpy as np
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from terrariaworld import TerrariaWorld
from enumeration import WallID, Channel, Paint

class vec2:
    def __init__(self, r, c):
        self.r = r
        self.c = c
    
    def __add__(self, other):
        return vec2(self.r + other.r, self.c + other.c)

    def __rmul__(self, other):
        return vec2(self.r*other, self.c*other)
    
    def round(self):
        return vec2(round(self.r), round(self.c))
    
    def __repr__(self):
        return f"({self.r}, {self.c})"

def get_boundary(arr:np.ndarray) -> np.ndarray:
    rows, cols = arr.shape
    colvec_zero = np.zeros((rows, 1))
    rowvec_zero = np.zeros((1, cols))
    arr_L = np.concatenate((arr[:, 1:], colvec_zero), axis=1)
    arr_R = np.concatenate((colvec_zero, arr[:, :-1]), axis=1)
    arr_U = np.concatenate((arr[1:, :], rowvec_zero), axis=0)
    arr_D = np.concatenate((rowvec_zero, arr[:-1, :]), axis=0)
    return arr - np.where(arr_L + arr_R + arr_U + arr_D == 4, 1, 0)

def draw_line_seg(arr:np.ndarray,
                  pt1:vec2,
                  pt2:vec2) -> None:
    pt1_R, pt1_C = round(pt1.r), round(pt1.c)
    pt2_R, pt2_C = round(pt2.r), round(pt2.c)
    if abs(pt1_R - pt2_R) >= abs(pt1_C - pt2_C):
        if pt1_R > pt2_R:
            pt1_R, pt2_R = pt2_R, pt1_R
            pt1_C, pt2_C = pt2_C, pt1_C
        for row in range(pt1_R, pt2_R + 1):
            col = round(pt1_C + (pt2_C - pt1_C)*(row - pt1_R)/(pt2_R - pt1_R))
            arr[row, col] = 1
    else:
        if pt1_C > pt2_C:
            pt1_R, pt2_R = pt2_R, pt1_R
            pt1_C, pt2_C = pt2_C, pt1_C
        for col in range(pt1_C, pt2_C + 1):
            row = round(pt1_R + (pt2_R - pt1_R)*(col - pt1_C)/(pt2_C - pt1_C))
            arr[row, col] = 1

SIZE = 901 #must be odd

result = np.zeros((SIZE, SIZE))

arange_size = np.arange(SIZE)
r = np.tile(np.expand_dims(arange_size, axis=1), (1, SIZE))
c = np.tile(np.expand_dims(arange_size, axis=0), (SIZE, 1))

x = r - SIZE//2
y = c - SIZE//2

result += np.where(x**2 + y**2 <= 350**2, 1, 0) * np.where(x**2 + y**2 >= 340**2, 1, 0)

disk = np.where(x**2 + y**2 <= 340**2, 1, 0)
for angle in np.linspace(0, 2*np.pi, 5, False):
    disk *= np.where((x - 405*np.cos(angle))**2 + (y - 405*np.sin(angle))**2 >= 238**2, 1, 0)
result += disk

result = np.where(result >= 1, 1, 0)

color_scheme = np.int32((5*x + 3*y)/100)%12 + 13
color_scheme = color_scheme*result
color_scheme = np.where(color_scheme == 0, Paint.NEGATIVE, color_scheme)

MARGIN = 50
world = TerrariaWorld(world_size = (MARGIN + SIZE + MARGIN, MARGIN + SIZE + MARGIN))
world.tiles.enter_editmode()
world.spawnX = MARGIN + SIZE//2
world.spawnY = MARGIN + SIZE//2

world.tiles.tileinfos[MARGIN:MARGIN + SIZE, MARGIN:MARGIN + SIZE, Channel.WALL] = WallID.DiamondGemspark
world.tiles.tileinfos[MARGIN:MARGIN + SIZE, MARGIN:MARGIN + SIZE, Channel.WALLCOLOR] = color_scheme
world.tiles.exit_editmode()

world.save_world("other_circle_01")