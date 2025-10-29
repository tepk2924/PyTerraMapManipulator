import io
import struct

with open('aaaaaaaaaaa', 'wb') as f:
    f.write(struct.pack('<i', 100))
    print(f.tell())