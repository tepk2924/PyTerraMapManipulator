import struct

# def read_uint8(f):
#     return struct.unpack('<B', f.read(1))[0]

# file_path = input(": ")

# with open(file_path, "rb") as f:
#     length = len(f.read())
# arr = []

# with open(file_path, "rb") as f:
#     for _ in range(length):
#         arr.append(read_uint8(f))

# print(arr)

from tile import Tile

arr = []

for i in range(20160000):
    tile = Tile()
    tile.reset()
    arr.append(tile)
    if i % 100000 == 0:
        print(i, "done")

print("done!")