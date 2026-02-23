import sys
import numpy as np
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import importlib
patternlib = importlib.import_module("004#_PatternLib")
import multiprocessing
from draw import vec2, unit, polygon_boolean

def draw_polygon(result:np.ndarray,
                 polygon:list[vec2]) -> None:
    polygon_integer = [*map(round, polygon)]
    min_r = min([pt.r for pt in polygon_integer])
    max_r = max([pt.r for pt in polygon_integer])
    min_c = min([pt.c for pt in polygon_integer])
    max_c = max([pt.c for pt in polygon_integer])
    min_r -= 2
    max_r += 2
    min_c -= 2
    max_c += 2
    window = result[min_r:max_r + 1, min_c:max_c + 1]
    polygon_integer_norm = []
    for pt in polygon_integer:
        polygon_integer_norm.append(pt - vec2(min_r, min_c))
    window += polygon_boolean(max_r + 1 - min_r, max_c + 1 - min_c, polygon_integer_norm)

def erase_polygon(result:np.ndarray,
                  polygon:list[vec2]) -> None:
    polygon_integer = [*map(round, polygon)]
    min_r = min([pt.r for pt in polygon_integer])
    max_r = max([pt.r for pt in polygon_integer])
    min_c = min([pt.c for pt in polygon_integer])
    max_c = max([pt.c for pt in polygon_integer])
    min_r -= 2
    max_r += 2
    min_c -= 2
    max_c += 2
    window = result[min_r:max_r + 1, min_c:max_c + 1]
    polygon_integer_norm = []
    for pt in polygon_integer:
        polygon_integer_norm.append(pt - vec2(min_r, min_c))
    window[polygon_boolean(max_r + 1 - min_r, max_c + 1 - min_c, polygon_integer_norm)] = 0

def main():
    SIZE = 1601 #must be odd

    result = np.zeros((SIZE, SIZE), dtype=np.uint8)

    r = np.tile(np.arange(SIZE).reshape(SIZE, 1), (1, SIZE))
    c = np.tile(np.arange(SIZE).reshape(1, SIZE), (SIZE, 1))

    x = r - SIZE//2
    y = c - SIZE//2

    mid = vec2(SIZE//2, SIZE//2)

    result += (sum([polygon_boolean(SIZE, SIZE, [mid + 400*unit(angle + bngle) for bngle in np.linspace(0, 2*np.pi, 5, False)]) for angle in np.linspace(0, 2*np.pi/5, 2, False)])%2 == 1)

    for angle in np.linspace(0, 2*np.pi, 10, False):
        patternlib.draw_line_seg(result, mid + 30*unit(angle), mid + 30*unit(angle + 3*np.pi/5))
        patternlib.draw_line_seg(result, mid, mid + 340*unit(angle + np.pi/10))
        patternlib.draw_line_seg(result, mid + 320*unit(angle + np.pi/10), mid + 320*unit(angle + 3*np.pi/10))
        draw_polygon(result, [mid + 30*unit(angle),
                              mid + 300*unit(angle + np.pi/12),
                              mid + 300*unit(angle - np.pi/12)])
        erase_polygon(result, [mid + 70*unit(angle),
                               mid + 280*unit(angle + np.pi/15),
                               mid + 280*unit(angle - np.pi/15)])
        pt1 = mid + 69*unit(angle)
        pt2 = mid + 270*unit(angle)
        pt3 = pt2 + 64*unit(angle + 3*np.pi/4)
        pt4 = pt2 + 64*unit(angle - 3*np.pi/4)
        patternlib.draw_line_seg(result, pt1, pt2)
        patternlib.draw_line_seg(result, pt2, pt3)
        patternlib.draw_line_seg(result, pt2, pt4)
        pt5 = mid + 200*unit(angle)
        for idx in range(11):
            patternlib.draw_line_seg(result, pt5, pt5 + 90*unit(angle - np.pi/4 + idx*np.pi/20))

        pt6 = pt5 + 10*unit(angle + 3*np.pi/4)
        pt7 = pt6 - 70*unit(angle)
        pt8 = pt6 + 40*unit(angle + np.pi/4)
        draw_polygon(result, [pt6, pt7, pt8])

        pt9 = pt5 + 10*unit(angle - 3*np.pi/4)
        pt10 = pt9 - 70*unit(angle)
        pt11 = pt9 + 40*unit(angle - np.pi/4)
        draw_polygon(result, [pt9, pt10, pt11])

    for angle in np.linspace(np.pi/5, 11*np.pi/5, 5, False):
        pt1 = mid + 700*unit(angle)
        pt2 = mid + 700*unit(angle + 2*np.pi/5)
        draw_polygon(result, [mid + 450*unit(angle),
                              mid + 390*unit(angle + np.pi/10),
                              pt1,
                              mid + 390*unit(angle - np.pi/10)])
        draw_polygon(result, [pt1 + 20*unit(angle + 3*np.pi/5),
                              pt2 + 20*unit(angle - 1*np.pi/5),
                              mid + 420*unit(angle + np.pi/5)])

    color_scheme = np.int32((5*x + 3*y)/100)%12 + 13
    patternlib.export_pattern(result, color_scheme, "other_pattern_02", min(4, multiprocessing.cpu_count()))

if __name__ == "__main__":
    main()