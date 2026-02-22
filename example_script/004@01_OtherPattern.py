import sys
import numpy as np
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from terrariaworld import TerrariaWorld
from enumeration import WallID, Channel, Paint
from draw import vec2, unit, line_seg_mask

def draw_line_seg(arr:np.ndarray,
                  pt1:vec2,
                  pt2:vec2) -> None:
    rows, cols = arr.shape
    arr[line_seg_mask(rows, cols, pt1, pt2)] = 1

SIZE = 901 #must be odd

result = np.zeros((SIZE, SIZE))

arange_size = np.arange(SIZE)
r = np.tile(np.expand_dims(arange_size, axis=1), (1, SIZE))
c = np.tile(np.expand_dims(arange_size, axis=0), (SIZE, 1))

x = r - SIZE//2
y = c - SIZE//2

sq = x**2 + y**2
d = np.sqrt(sq)
theta = np.atan2(y, x)

result += np.where((sq <= 400**2) & (sq >= 390**2), 1, 0)

star = np.where(sq <= 390**2, 1, 0)
for angle in np.linspace(0, 2*np.pi, 5, False):
    star *= np.where((x - 470*np.cos(angle))**2 + (y - 470*np.sin(angle))**2 >= 276**2, 1, 0)
result += star

O = vec2(SIZE//2, SIZE//2)
arr = [273, 276, 284, 288, 292, 296, 300, 308, 311]
for a in arr:
    for angle in np.linspace(0, 2*np.pi, 5, False):
        draw_line_seg(result,
                      O + a*unit(angle),
                      O + a*unit(angle + 2*np.pi/5))
        draw_line_seg(result,
                      O + a*unit(angle),
                      O + a*unit(angle + 4*np.pi/5))

def pentagon_ring(A, B):
    ret = np.zeros((SIZE, SIZE))
    for angle in np.linspace(0, 2*np.pi, 5, False):
        ret += np.where((x - A*np.cos(angle))**2 + (y - A*np.sin(angle))**2 <= B**2, 1, 0)
    Ax = A*np.cos(np.pi/5)
    Ay = A*np.sin(np.pi/5)
    for angle in np.linspace(0, 2*np.pi, 5, False):
        x_rot = x*np.cos(angle + np.pi/5) + y*np.sin(angle + np.pi/5)
        y_rot = -x*np.sin(angle + np.pi/5) + y*np.cos(angle + np.pi/5)
        ret += np.where((x_rot <= Ax + B) & (x_rot >= Ax - B) & (y_rot <= Ay) & (y_rot >= -Ay), 1, 0)
    ret = np.where(ret >= 1, 1, 0)
    return ret

result = np.where(pentagon_ring(160, 30) == 1, 0, result)
result += pentagon_ring(160, 20)
result = np.where(pentagon_ring(160, 10) == 1, 0, result)

result = np.where(100*np.abs(np.cos(2.5*theta)) >= d, 0, result)
result += np.where(90*np.abs(np.cos(2.5*theta)) >= d, 1, 0)
result = np.where(80*np.abs(np.cos(2.5*theta)) >= d, 0, result)
result += np.where(70*np.abs(np.cos(2.5*theta)) >= d, 1, 0)
result = np.where(60*np.abs(np.cos(2.5*theta)) >= d, 0, result)
result += np.where(50*np.abs(np.cos(2.5*theta)) >= d, 1, 0)

for angle in np.linspace(0, 2*np.pi, 5, False):
    x_rot = x*np.cos(angle + np.pi/5) + y*np.sin(angle + np.pi/5)
    result = np.where((x_rot >= 170) &
                      ((x - 470*np.cos(angle))**2 + (y - 470*np.sin(angle))**2 >= 286**2) &
                      ((x - 470*np.cos(angle + 2*np.pi/5))**2 + (y - 470*np.sin(angle + 2*np.pi/5))**2 >= 286**2), 0, result)

for angle in np.linspace(0, 2*np.pi, 5, False):
    result += np.where(((x - 292*np.cos(angle))**2 + (y - 292*np.sin(angle))**2 >= 98**2) & 
                       ((x - 292*np.cos(angle))**2 + (y - 292*np.sin(angle))**2 <= 108**2), 1, 0)

for angle1 in np.linspace(0, 2*np.pi, 5, False):
    for angle2 in np.linspace(0, 2*np.pi, 10, False):
        draw_line_seg(result,
                      O + 292*unit(angle1) + 103*unit(angle2),
                      O + 292*unit(angle1) + 103*unit(angle2 + 4*np.pi/5))
        draw_line_seg(result,
                      O + 292*unit(angle1) + 103*unit(angle2 + np.pi/10),
                      O + 292*unit(angle1) + 103*unit(angle2 + 9*np.pi/10))

for angle in np.linspace(0, 2*np.pi, 5, False):
    rel_x_alpha = x - 342*np.cos(0.466 + angle)
    rel_y_alpha = y - 342*np.sin(0.466 + angle)
    sq_alpha = rel_x_alpha**2 + rel_y_alpha**2
    dist_alpha = np.sqrt(sq_alpha)
    theta_alpha = np.atan2(rel_y_alpha, rel_x_alpha)
    result += np.where(sq_alpha <= 57**2, 1, 0)
    result = np.where(sq_alpha <= 47**2, 0, result)
    result += np.where((30 + 10*np.cos(5*(theta_alpha - 0.466 - angle)) >= dist_alpha) & 
                       (20 + 10*np.cos(5*(theta_alpha - 0.466 - angle)) <= dist_alpha), 1, 0)

    rel_x_beta = x - 342*np.cos(-0.466 + angle)
    rel_y_beta = y - 342*np.sin(-0.466 + angle)
    sq_beta = rel_x_beta**2 + rel_y_beta**2
    dist_beta = np.sqrt(sq_beta)
    theta_beta = np.atan2(rel_y_beta, rel_x_beta)
    result += np.where(sq_beta <= 57**2, 1, 0)
    result = np.where(sq_beta <= 47**2, 0, result)
    result += np.where((30 + 10*np.cos(5*(theta_beta + 0.466 - angle)) >= dist_beta) & 
                       (20 + 10*np.cos(5*(theta_beta + 0.466 - angle)) <= dist_beta), 1, 0)

for angle in np.linspace(0, 2*np.pi, 5, False):
    result += np.where((x - 210*np.cos(angle + np.pi/5))**2 + (y - 210*np.sin(angle + np.pi/5))**2 <= 48**2, 1, 0)
    result = np.where((x - 210*np.cos(angle + np.pi/5))**2 + (y - 210*np.sin(angle + np.pi/5))**2 <= 43**2, 0, result)

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