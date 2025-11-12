import sys
import numpy as np
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from terrariaworld import TerrariaWorld
from enumeration import WallID, Channel

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

big_radius = 400
big_circle = np.where(x**2 + y**2 <= big_radius**2, 1, 0)
result += get_boundary(big_circle)

ec_1 = [250, 75]
ec_2 = [262.5, 78.5]
ec_3 = [275, 82]
for angle in np.linspace(0, np.pi, 6, False):
    eclipse = np.where(((x*np.cos(angle) + y*np.sin(angle))/ec_1[0])**2 +
                       ((-x*np.sin(angle) + y*np.cos(angle))/ec_1[1])**2 <= 1, 1, 0)
    result += get_boundary(eclipse)
    eclipse = np.where(((x*np.cos(angle) + y*np.sin(angle))/ec_2[0])**2 +
                       ((-x*np.sin(angle) + y*np.cos(angle))/ec_2[1])**2 <= 1, 1, 0)
    result += get_boundary(eclipse)
    eclipse = np.where(((x*np.cos(angle) + y*np.sin(angle))/ec_3[0])**2 +
                       ((-x*np.sin(angle) + y*np.cos(angle))/ec_3[1])**2 <= 1, 1, 0)
    result += get_boundary(eclipse)

annulus_1 = np.where(270**2 <= x**2 + y**2, 1, 0)*np.where(x**2 + y**2 <= 290**2, 1, 0)
annulus_2 = np.where(335**2 <= x**2 + y**2, 1, 0)*np.where(x**2 + y**2 <= 345**2, 1, 0)
result += annulus_1
result += annulus_2

for angle in np.linspace(0, np.pi/2, 6, False):
    square = np.where(abs((x*np.cos(angle) + y*np.sin(angle))) + 
                      abs((-x*np.sin(angle) + y*np.cos(angle))) <= 400, 1, 0)
    result += get_boundary(square)

x_small = r[:41, :41] - 20
y_small = c[:41, :41] - 20
small_circle = get_boundary(np.where(x_small**2 + y_small**2 <= 15**2, 1, 0))
for angle in np.linspace(0, 2*np.pi, 24, False):
    center_R = int(450 + 368*np.cos(angle))
    center_C = int(450 + 368*np.sin(angle))
    result[center_R - 20:center_R + 21, center_C - 20:center_C + 21] += small_circle
    pt1 = vec2(center_R + 15*np.cos(angle), center_C + 15*np.sin(angle))
    pt2 = vec2(center_R + 15*np.cos(angle + np.pi/2), center_C + 15*np.sin(angle + np.pi/2))
    pt3 = vec2(center_R + 15*np.cos(angle + np.pi), center_C + 15*np.sin(angle + np.pi))
    pt4 = vec2(center_R + 15*np.cos(angle + 3*np.pi/2), center_C + 15*np.sin(angle + 3*np.pi/2))
    draw_line_seg(result, pt1, pt2)
    draw_line_seg(result, pt2, pt3)
    draw_line_seg(result, pt3, pt4)
    draw_line_seg(result, pt4, pt1)
    draw_line_seg(result, pt1, pt3)
    draw_line_seg(result, pt2, pt4)

for idx in range(0, 75, 15):
    result += np.where(np.abs(x) + np.abs(y) == idx, 1, 0)

for angle in np.linspace(0, 2*np.pi, 12, False):
    result += np.where((x - 170*np.cos(angle))**2 + (y - 170*np.sin(angle))**2 <= 40**2, 1, 0) * np.where((x - 181*np.cos(angle))**2 + (y - 181*np.sin(angle))**2 >= 30**2, 1, 0)
    draw_line_seg(result,
                  vec2(450, 450),
                  vec2(450 + 270*np.cos(angle), 450 + 270*np.sin(angle)))
    draw_line_seg(result,
                  vec2(450 + 150*np.cos(angle) + 10*np.sin(angle), 450 + 150*np.sin(angle) - 10*np.cos(angle)),
                  vec2(450 + 270*np.cos(angle) + 10*np.sin(angle), 450 + 270*np.sin(angle) - 10*np.cos(angle)))
    draw_line_seg(result,
                  vec2(450 + 150*np.cos(angle) - 10*np.sin(angle), 450 + 150*np.sin(angle) + 10*np.cos(angle)),
                  vec2(450 + 270*np.cos(angle) - 10*np.sin(angle), 450 + 270*np.sin(angle) + 10*np.cos(angle)))
    draw_line_seg(result,
                  vec2(450 + 180*np.cos(angle) + 30*np.sin(angle), 450 + 180*np.sin(angle) - 30*np.cos(angle)),
                  vec2(450 + 180*np.cos(angle) - 30*np.sin(angle), 450 + 180*np.sin(angle) + 30*np.cos(angle)))

center_X = 250
center_Y = 200
center_R = center_X + 450
center_C = center_Y + 450
result += np.where((x - center_X)**2 + (y - center_Y)**2 <= 130**2, 1, 0)
result *= np.where(120**2 <= (x - center_X)**2 + (y - center_Y)**2, 1, 0)
pts = [vec2(center_R + 120*np.cos(angle), center_C + 120*np.sin(angle)) for angle in np.linspace(0, 2*np.pi, 8, False)]
for _ in range(10):
    new_pts = []
    for idx in range(8):
        draw_line_seg(result, pts[idx], pts[(idx + 1)%8])
        new_pts.append(0.8*pts[idx] + 0.2*pts[(idx + 1)%8])
    pts = new_pts
for idx in [1, 3]:
    for jdx in range(8):
        draw_line_seg(result, pts[jdx], pts[(jdx + idx)%8])
result += np.where((x - center_X)**2 + (y - center_Y)**2 <= 20**2, 1, 0)

result = np.where(result >= 1, 1, 0)

color_scheme = np.int32((5*x + 3*y)/100)%12 + 13
color_scheme = color_scheme*result

world = TerrariaWorld(world_size = "small")
world.tiles.enter_editmode()

COL = world.tileswide
world.tiles.tileinfos[200:200 + SIZE, COL//2 - SIZE//2:COL//2 - SIZE//2 + SIZE, Channel.WALL] = result*(WallID.DiamondGemspark - WallID.Glass) + np.ones((SIZE, SIZE))*WallID.Glass
world.tiles.tileinfos[200:200 + SIZE, COL//2 - SIZE//2:COL//2 - SIZE//2 + SIZE, Channel.WALLCOLOR] = color_scheme
world.tiles.exit_editmode()

world.save_world("magic_circle")