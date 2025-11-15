import io
import struct

def read_boolean(f:io.BufferedReader) -> bool:
    return f.read(1) != b'\x00'

def read_int8(f:io.BufferedReader) -> int:
    return struct.unpack('<b', f.read(1))[0]

def read_uint8(f:io.BufferedReader) -> int:
    return struct.unpack('<B', f.read(1))[0]

def read_int16(f:io.BufferedReader) -> int:
    return struct.unpack('<h', f.read(2))[0]

def read_uint16(f:io.BufferedReader) -> int:
    return struct.unpack('<H', f.read(2))[0]

def read_int32(f:io.BufferedReader) -> int:
    return struct.unpack('<i', f.read(4))[0]

def read_uint32(f:io.BufferedReader) -> int:
    return struct.unpack('<I', f.read(4))[0]

def read_int64(f:io.BufferedReader) -> int:
    return struct.unpack('<q', f.read(8))[0]

def read_uint64(f:io.BufferedReader) -> int:
    return struct.unpack('<Q', f.read(8))[0]

def read_single(f:io.BufferedReader) -> float:
    return struct.unpack('<f', f.read(4))[0]

def read_double(f:io.BufferedReader) -> float:
    return struct.unpack('<d', f.read(8))[0]

def write_boolean(f:io.BufferedWriter, data:bool):
    f.write(struct.pack('?', data))

def write_int8(f:io.BufferedWriter, data:int):
    f.write(struct.pack('<b', data))

def write_uint8(f:io.BufferedWriter, data:int):
    f.write(struct.pack('<B', data))

def write_int16(f:io.BufferedWriter, data:int):
    f.write(struct.pack('<h', data))

def write_uint16(f:io.BufferedWriter, data:int):
    f.write(struct.pack('<H', data))

def write_int32(f:io.BufferedWriter, data:int):
    f.write(struct.pack('<i', data))

def write_uint32(f:io.BufferedWriter, data:int):
    f.write(struct.pack('<I', data))

def write_int64(f:io.BufferedWriter, data:int):
    f.write(struct.pack('<q', data))

def write_uint64(f:io.BufferedWriter, data:int):
    f.write(struct.pack('<Q', data))

def write_single(f:io.BufferedWriter, data:float):
    f.write(struct.pack('<f', data))

def write_double(f:io.BufferedWriter, data:float):
    f.write(struct.pack('<d', data))

def __read_7bit_encoded_int(f:io.BufferedWriter): #THX chatgpt
    result = 0
    shift = 0
    while True:
        b = f.read(1)
        if not b:
            raise EOFError("Unexpected EOF")
        b = b[0]
        result |= (b & 0x7F) << shift
        if b & 0x80 == 0:
            break
        shift += 7
    return result

def __write_7bit_encoded_int(f:io.BufferedWriter, value): #THX chatgpt
    while True:
        b = value & 0x7F
        value >>= 7
        if value:
            f.write(bytes([b | 0x80]))
        else:
            f.write(bytes([b]))
            break

def read_string(f:io.BufferedWriter) -> str: #THX chatgpt
    strlen = __read_7bit_encoded_int(f)
    return f.read(strlen).decode('utf-8')

def write_string(f:io.BufferedWriter, s: str): #THX chatgpt
    data = s.encode('utf-8')
    __write_7bit_encoded_int(f, len(data))
    f.write(data)