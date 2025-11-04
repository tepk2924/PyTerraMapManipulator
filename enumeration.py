from enum import IntEnum

class BrickStyle(IntEnum):
    FULL = 0x0
    HALFBRICK = 0x1
    SLOPETOPRIGHT = 0x2
    SLOPETOPLEFT = 0x3
    SLOPEBOTTOMRIGHT = 0x4
    SLOPEBOTTOMLEFT = 0x5

class Liquid(IntEnum):
    NONE = 0x0
    WATER = 0x01
    LAVA = 0x02
    HONEY = 0x03
    SHIMMER = 0x08

class Ch(IntEnum):
    ACTUACTOR = 0
    BRICKSTYLE = 1
    INACTIVE = 2
    LIQUIDAMOUNT = 3
    LIQUIDTYPE = 4
    TILECOLOR = 5
    TILETYPE = 6
    U = 7
    V = 8
    WALL = 9
    WALLCOLOR = 10
    WIREBLUE = 11
    WIREGREEN = 12
    WIRERED = 13
    WIREYELLOW = 14
    FULLBRIGHTBLOCK = 15
    FULLBRIGHTWALL = 16
    INVISIBLEBLOCK = 17
    INVISIBLEWALL = 18

class GameMode(IntEnum):
    CLASSIC = 0
    EXPERT = 1
    MASTER = 2
    JOURNEY = 3