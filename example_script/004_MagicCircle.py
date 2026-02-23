import sys
import numpy as np
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import importlib
patternlib = importlib.import_module("004#_PatternLib")
from draw import vec2, unit, get_boundary

SIZE = 901 #must be odd

result = np.zeros((SIZE, SIZE), dtype=np.uint8)

arange_size = np.arange(SIZE)
r = np.tile(np.expand_dims(arange_size, axis=1), (1, SIZE))
c = np.tile(np.expand_dims(arange_size, axis=0), (SIZE, 1))

x = r - SIZE//2
y = c - SIZE//2
sq = x**2 + y**2

big_radius = 400
big_circle = np.where(sq <= big_radius**2, 1, 0)
result += get_boundary(big_circle)

ec_1 = [250, 75]
ec_2 = [262.5, 78.5]
ec_3 = [275, 82]
for angle in np.linspace(0, np.pi, 6, False):
    rot_x = x*np.cos(angle) + y*np.sin(angle)
    rot_y = -x*np.sin(angle) + y*np.cos(angle)
    ellipse = np.where((rot_x/ec_1[0])**2 +
                       (rot_y/ec_1[1])**2 <= 1, 1, 0)
    result += get_boundary(ellipse)
    ellipse = np.where((rot_x/ec_2[0])**2 +
                       (rot_y/ec_2[1])**2 <= 1, 1, 0)
    result += get_boundary(ellipse)
    ellipse = np.where((rot_x/ec_3[0])**2 +
                       (rot_y/ec_3[1])**2 <= 1, 1, 0)
    result += get_boundary(ellipse)

annulus_1 = np.where((270**2 <= sq) & (sq <= 290**2), 1, 0)
annulus_2 = np.where((335**2 <= sq) & (sq <= 345**2), 1, 0)
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
    center_vec = vec2(center_R, center_C)
    result[center_R - 20:center_R + 21, center_C - 20:center_C + 21] += small_circle
    pt1 = center_vec + 15*unit(angle)
    pt2 = center_vec + 15*unit(angle + np.pi/2)
    pt3 = center_vec + 15*unit(angle + np.pi)
    pt4 = center_vec + 15*unit(angle + 3*np.pi/2)
    patternlib.draw_line_seg(result, pt1, pt2)
    patternlib.draw_line_seg(result, pt2, pt3)
    patternlib.draw_line_seg(result, pt3, pt4)
    patternlib.draw_line_seg(result, pt4, pt1)
    patternlib.draw_line_seg(result, pt1, pt3)
    patternlib.draw_line_seg(result, pt2, pt4)

for idx in range(0, 75, 15):
    result += np.where(np.abs(x) + np.abs(y) == idx, 1, 0)

O = vec2(SIZE//2, SIZE//2)
for angle in np.linspace(0, 2*np.pi, 12, False):
    result += np.where(((x - 170*np.cos(angle))**2 + (y - 170*np.sin(angle))**2 <= 40**2) & ((x - 181*np.cos(angle))**2 + (y - 181*np.sin(angle))**2 >= 30**2), 1, 0)
    patternlib.draw_line_seg(result,
                  O,
                  O + 270*unit(angle))
    patternlib.draw_line_seg(result,
                  O + 150*unit(angle) + 10*unit(angle + np.pi/2),
                  O + 270*unit(angle) + 10*unit(angle + np.pi/2))
    patternlib.draw_line_seg(result,
                  O + 150*unit(angle) + 10*unit(angle - np.pi/2),
                  O + 270*unit(angle) + 10*unit(angle - np.pi/2))
    patternlib.draw_line_seg(result,
                  O + 180*unit(angle) + 30*unit(angle + np.pi/2),
                  O + 180*unit(angle) + 30*unit(angle - np.pi/2))

center_X = 250
center_Y = 200
center_R = center_X + 450
center_C = center_Y + 450
result += np.where((x - center_X)**2 + (y - center_Y)**2 <= 130**2, 1, 0)
result *= np.where(120**2 <= (x - center_X)**2 + (y - center_Y)**2, 1, 0)
pts = [vec2(center_R, center_C) + 120*unit(angle) for angle in np.linspace(0, 2*np.pi, 8, False)]
for _ in range(10):
    new_pts = []
    for idx in range(8):
        patternlib.draw_line_seg(result, pts[idx], pts[(idx + 1)%8])
        new_pts.append(0.8*pts[idx] + 0.2*pts[(idx + 1)%8])
    pts = new_pts
for idx in [1, 3]:
    for jdx in range(8):
        patternlib.draw_line_seg(result, pts[jdx], pts[(jdx + idx)%8])
result += np.where((x - center_X)**2 + (y - center_Y)**2 <= 20**2, 1, 0)

color_scheme = np.int32((5*x + 3*y)/100)%12 + 13
patternlib.export_pattern(result, color_scheme, "magic_circle")