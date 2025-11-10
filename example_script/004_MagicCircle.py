import sys
import numpy as np
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from terrariaworld import TerrariaWorld
from enumeration import WallID, Channel

def get_boundary(arr:np.ndarray):
    rows, cols = arr.shape
    colvec_zero = np.zeros((rows, 1))
    rowvec_zero = np.zeros((1, cols))
    arr_L = np.concatenate((arr[:, 1:], colvec_zero), axis=1)
    arr_R = np.concatenate((colvec_zero, arr[:, :-1]), axis=1)
    arr_U = np.concatenate((arr[1:, :], rowvec_zero), axis=0)
    arr_D = np.concatenate((rowvec_zero, arr[:-1, :]), axis=0)
    return arr - np.where(arr_L + arr_R + arr_U + arr_D == 4, 1, 0)
    

SIZE = 901 #must be odd

result = np.zeros((SIZE, SIZE))

arange_size = np.arange(SIZE)
row_idx = np.tile(np.expand_dims(arange_size, axis=1), (1, SIZE))
col_idx = np.tile(np.expand_dims(arange_size, axis=0), (SIZE, 1))

x = row_idx - SIZE//2
y = col_idx - SIZE//2

big_radius = 400
big_circle = np.where(x**2 + y**2 <= big_radius**2, 1, 0)
result += get_boundary(big_circle)

ec_1 = [250, 75]
ec_2 = [262.5, 78.5]
ec_3 = [275, 82]
for angle in np.linspace(0, np.pi, 4, False):
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
annulus_2 = np.where(330**2 <= x**2 + y**2, 1, 0)*np.where(x**2 + y**2 <= 340**2, 1, 0)
result += annulus_1
result += annulus_2

for angle in np.linspace(0, np.pi/2, 6, False):
    square = np.where(abs((x*np.cos(angle) + y*np.sin(angle))) + 
                      abs((-x*np.sin(angle) + y*np.cos(angle))) <= 400, 1, 0)
    result += get_boundary(square)

x_small = row_idx[:41, :41] - 20
y_small = col_idx[:41, :41] - 20
small_circle = get_boundary(np.where(x_small**2 + y_small**2 <= 15**2, 1, 0))
for angle in np.linspace(0, 2*np.pi, 24, False):
    center_X = int(450 + 368*np.cos(angle))
    center_Y = int(450 + 368*np.sin(angle))
    result[center_X - 20:center_X + 21, center_Y - 20:center_Y + 21] += small_circle

for idx in range(0, 75, 15):
    result += np.where(np.abs(x) + np.abs(y) == idx, 1, 0)

for angle in np.linspace(0, 2*np.pi, 8, False):
    result += np.where((x - 170*np.cos(angle))**2 + (y - 170*np.sin(angle))**2 <= 40**2, 1, 0) * np.where((x - 181*np.cos(angle))**2 + (y - 181*np.sin(angle))**2 >= 30**2, 1, 0)

result = np.where(result >= 1, 1, 0)

color_scheme = np.int32((5*x + 3*y)/100)%12 + 1
color_scheme = color_scheme*result

world = TerrariaWorld(world_size = "small")
world.tiles.enter_editmode()

COL = world.tileswide
world.tiles.tileinfos[200:200 + SIZE, COL//2 - SIZE//2:COL//2 - SIZE//2 + SIZE, Channel.WALL] = result*(WallID.DiamondGemspark - WallID.Glass) + np.ones((SIZE, SIZE))*WallID.Glass
world.tiles.tileinfos[200:200 + SIZE, COL//2 - SIZE//2:COL//2 - SIZE//2 + SIZE, Channel.WALLCOLOR] = color_scheme
world.tiles.exit_editmode()

world.save_world("magic_circle")