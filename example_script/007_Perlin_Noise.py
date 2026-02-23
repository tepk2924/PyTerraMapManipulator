import numpy as np
import os
import sys
import multiprocessing
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from terrariaworld import TerrariaWorld
from enumeration import Channel, TileID, BrickStyle

def perlin_noise(R:int,
                 C:int,
                 sizes:list[int],
                 amps:list[int]):
    grid_points = np.zeros((R, C), dtype=np.float64)

    smooth = lambda x:3*x**2 - 2*x**3

    for idx, (size, amp) in enumerate(zip(sizes, amps), start=1):
        angle = np.random.random((R//size + 2, C//size + 2))*np.pi*2
        print(f"perlin noise iteration {idx}: angle generated")
        cos_small = np.cos(angle)
        sin_small = np.sin(angle)
        cos_large = np.repeat(np.repeat(cos_small, size, axis=0), size, axis=1)
        sin_large = np.repeat(np.repeat(sin_small, size, axis=0), size, axis=1)
        print(f"perlin noise iteration {idx}: basic cos, sin generated")
        UL_cos = cos_large[:R, :C]
        UR_cos = cos_large[:R, size:C+size]
        DL_cos = cos_large[size:R+size, :C]
        DR_cos = cos_large[size:R+size, size:C+size]
        UL_sin = sin_large[:R, :C]
        UR_sin = sin_large[:R, size:C+size]
        DL_sin = sin_large[size:R+size, :C]
        DR_sin = sin_large[size:R+size, size:C+size]
        print(f"perlin noise iteration {idx}: cos, sin complete")
        dx = (np.arange(R)%size/size).reshape(R, 1)
        dy = np.arange(C)%size/size
        dp_UL = dx*UL_cos + dy*UL_sin
        dp_UR = dx*UR_cos + (dy - 1)*UR_sin
        dp_DL = (dx - 1)*DL_cos + dy*DL_sin
        dp_DR = (dx - 1)*DR_cos + (dy - 1)*DR_sin
        print(f"perlin noise iteration {idx}: dot product complete")
        smoothdx = smooth(dx)
        smoothdy = smooth(dy)
        print(f"perlin noise iteration {idx}: smooth map complete")
        value = (dp_UL*(1 - smoothdx) + dp_DL*smoothdx)*(1 - smoothdy) + (dp_UR*(1 - smoothdx) + dp_DR*smoothdx)*smoothdy
        grid_points += amp*value
        print(f"perlin noise iteration {idx}: complete")
    return grid_points

def main():
    H = 2400
    W = 8400

    THRESHOLD = -0.1
    values = (perlin_noise(H + 1, W + 1, [40, 20, 10], [1, 0.2, 0.2]) >= THRESHOLD).astype(np.uint8)

    UL = values[:H, :W]
    UR = values[:H, 1:]
    DL = values[1:, :W]
    DR = values[1:, 1:]
    status = 8*UL + 4*UR + 2*DL + DR
    summation = UL + UR + DL + DR

    world = TerrariaWorld((H, W))

    world.tiles.enter_editmode()

    world.tiles.tileinfos[summation >= 3, Channel.TILETYPE] = TileID.GrayBrick
    world.tiles.tileinfos[status == 0b0111, Channel.BRICKSTYLE] = BrickStyle.SLOPETOPLEFT
    world.tiles.tileinfos[status == 0b1011, Channel.BRICKSTYLE] = BrickStyle.SLOPETOPRIGHT
    world.tiles.tileinfos[status == 0b1101, Channel.BRICKSTYLE] = BrickStyle.SLOPEBOTTOMLEFT
    world.tiles.tileinfos[status == 0b1110, Channel.BRICKSTYLE] = BrickStyle.SLOPEBOTTOMRIGHT

    world.tiles.exit_editmode()
    world.title = "perlin_noise"
    world.save_world("perlin_noise", multiprocessing.cpu_count())

if __name__ == "__main__":
    main()