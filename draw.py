from dataclasses import dataclass
import numpy as np

@dataclass
class vec2:
    r:int
    c:int
    
    def __add__(self, other):
        return vec2(self.r + other.r, self.c + other.c)
    
    def __sub__(self, other):
        return vec2(self.r - other.r, self.c - other.c)

    def __mul__(self, other):
        if isinstance(other, float | int):
            return vec2(self.r*other, self.c*other)
        else:
            raise ValueError

    def __rmul__(self, other):
        if isinstance(other, float | int):
            return vec2(self.r*other, self.c*other)
        else:
            raise ValueError
    
    def __round__(self):
        return vec2(round(self.r), round(self.c))
    
    def __iter__(self):
        yield self.r
        yield self.c

    def __str__(self):
        return f"({self.r}, {self.c})"
    
    def __complex__(self):
        return self.r + self.c*1j

def unit(angle:float) -> vec2:
    return vec2(np.cos(angle), np.sin(angle))

def get_boundary(arr:np.ndarray) -> np.ndarray:
    '''
    arr: np.ndarray with value of 0 or 1.
    '''
    rows, cols = arr.shape
    colvec_zero = np.zeros((rows, 1))
    rowvec_zero = np.zeros((1, cols))
    arr_L = np.concatenate((arr[:, 1:], colvec_zero), axis=1)
    arr_R = np.concatenate((colvec_zero, arr[:, :-1]), axis=1)
    arr_U = np.concatenate((arr[1:, :], rowvec_zero), axis=0)
    arr_D = np.concatenate((rowvec_zero, arr[:-1, :]), axis=0)
    return arr - np.where(arr_L + arr_R + arr_U + arr_D == 4, 1, 0)

def line_seg_mask(pt1:vec2,
                  pt2:vec2) -> list[list[int], list[int]]:
    ret_R, ret_C = [], []
    pt1_R, pt1_C = round(pt1)
    pt2_R, pt2_C = round(pt2)
    if abs(pt1_R - pt2_R) >= abs(pt1_C - pt2_C):
        if pt1_R > pt2_R:
            pt1_R, pt2_R = pt2_R, pt1_R
            pt1_C, pt2_C = pt2_C, pt1_C
        for row in range(pt1_R, pt2_R + 1):
            col = round(pt1_C + (pt2_C - pt1_C)*(row - pt1_R)/(pt2_R - pt1_R))
            ret_R.append(row)
            ret_C.append(col)
    else:
        if pt1_C > pt2_C:
            pt1_R, pt2_R = pt2_R, pt1_R
            pt1_C, pt2_C = pt2_C, pt1_C
        for col in range(pt1_C, pt2_C + 1):
            row = round(pt1_R + (pt2_R - pt1_R)*(col - pt1_C)/(pt2_C - pt1_C))
            ret_R.append(row)
            ret_C.append(col)
    return [ret_R, ret_C]

def polygon_boolean(rows:int,
                    cols:int,
                    polygon:list[vec2]) -> np.ndarray:
    arr = np.zeros((rows, cols), dtype=np.bool)
    total_winding = np.zeros((rows, cols), dtype=np.float32)
    complex_cords = np.arange(rows, dtype=np.int32).reshape(rows, 1) + np.arange(cols, dtype=np.int32)*1j
    for idx in range(len(polygon)):
        z1 = complex(polygon[idx - 1])
        z2 = complex(polygon[idx])
        current_winding = np.angle((z2 - complex_cords)*np.conjugate(z1 - complex_cords))
        total_winding += current_winding
    arr[np.abs(total_winding) >= np.pi] = True
    for idx in range(len(polygon)):
        arr[*line_seg_mask(polygon[idx - 1], polygon[idx])] = True
    return arr