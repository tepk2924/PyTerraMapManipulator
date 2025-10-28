import struct
import io
import uuid

class WorldFileFormatException(Exception):
    pass

class World_1_4_4:
    #At least works for 1.4.4.....
    def __init__(self):
        self.versionnumber:int = None
        self.ischinese:bool = False
        self.filerevision:int = None
        self.isfavorite:bool = None
        self.tileframeimportant:list[bool] = None
        self.title:str = None
        self.seed:str = None
        self.worldgenversion:int = None
        self.worlduuid:uuid.UUID = None
        self.worldid:int = None
        self.leftworld:float = None
        self.rightworld:float = None
        self.topworld:float = None
        self.bottomworld:float = None
        self.tileshigh:int = None
        self.tileswide:int = None
        self.gamemode:int = None
        self.drunkworld:bool = None
        self.goodworld:bool = None
        self.tenthanniversaryworld:bool = None
        self.dontstarveworld:bool = None
        self.notthebeesworld:bool = None
        self.remixworld:bool = None
        self.notrapworld:bool = None
        self.zenithworld:bool = None
        self.creationtime:int = None
        self.moontype:int = None
        self.treeX:list[int] = [None, None, None]
        self.treeX0:int = None
        self.treeX1:int = None
        self.treeX2:int = None
        self.treestyle0:int = None
        self.treestyle1:int = None
        self.treestyle2:int = None
        self.treestyle3:int = None
        self.cavebackX:list[int] = [None, None, None]
        self.cavebackX0:int = None
        self.cavebackX1:int = None
        self.cavebackX2:int = None
        self.cavebackstyle0:int = None
        self.cavebackstyle1:int = None
        self.cavebackstyle2:int = None
        self.cavebackstyle3:int = None
        self.icebackstyle:int = None
        self.junglebackstyle:int = None
        self.hellbackstyle:int = None


    def read_boolean(self, f:io.BufferedReader) -> bool:
        return f.read(1) != b'\x00'

    def read_int8(self, f:io.BufferedReader) -> int:
        return struct.unpack('<b', f.read(1))[0]

    def read_uint8(self, f:io.BufferedReader) -> int:
        return struct.unpack('<B', f.read(1))[0]

    def read_int16(self, f:io.BufferedReader) -> int:
        return struct.unpack('<h', f.read(2))[0]
    
    def read_uint16(self, f:io.BufferedReader) -> int:
        return struct.unpack('<H', f.read(2))[0]

    def read_int32(self, f:io.BufferedReader) -> int:
        return struct.unpack('<i', f.read(4))[0]
    
    def read_uint32(self, f:io.BufferedReader) -> int:
        return struct.unpack('<I', f.read(4))[0]

    def read_int64(self, f:io.BufferedReader) -> int:
        return struct.unpack('<q', f.read(8))[0]
    
    def read_uint64(self, f:io.BufferedReader) -> int:
        return struct.unpack('<Q', f.read(8))[0]    

    def read_double(self, f:io.BufferedReader) -> float:
        return struct.unpack('<d', f.read(8))[0]

    def read_7bit_encoded_int(self, f):
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

    def read_string(self, f) -> str:
        strlen = self.read_7bit_encoded_int(f)
        return f.read(strlen).decode('utf-8')

    def loadV2(self):
        self.__init__()
        f = open(input("Map file path : "), "rb")
        self.versionnumber = self.read_uint32(f)

        tileframeimportant, section_ptrs = self.LoadSectionHeader(f)
        self.tileframeimportant = tileframeimportant

        if f.tell() != section_ptrs[0]:
            raise WorldFileFormatException("Unexpected Position: Invalid File Format Section")
        
        self.LoadHeaderFlags(f)

        f.close()

    def LoadSectionHeader(self, f):
        #loading section header
        headerformat = f.read(7).decode('ascii')
        filetype = f.read(1)
        self.filerevision = self.read_uint32(f)
        flags = self.read_uint64(f)
        self.isfavorite = ((flags & 1) == 1)
        sectioncount = self.read_int16(f)
        section_ptrs = []
        for _ in range(sectioncount):
            section_ptrs.append(self.read_int32(f))
        
        tileframeimportant = self.ReadBitArray(f)
        return tileframeimportant, section_ptrs
    
    def ReadBitArray(self, f):
        #read bit array
        bitarraylength = self.read_int16(f)
        data = 0
        bitmask = 128
        booleans = [False]*bitarraylength
        for idx in range(bitarraylength):
            if bitmask != 128:
                bitmask = bitmask << 1
            else:
                data = self.read_uint8(f)
                bitmask = 1
            if data & bitmask == bitmask:
                booleans[idx] = True
        return booleans
    
    def LoadHeaderFlags(self, f):
        self.title = self.read_string(f)

        self.seed = self.read_string(f)
        self.worldgenversion = self.read_uint64(f)

        self.worlduuid = uuid.UUID(bytes_le=f.read(16))

        self.worldid = self.read_int32(f)
        self.leftworld = float(self.read_int32(f))
        self.rightworld = float(self.read_int32(f))
        self.topworld = float(self.read_int32(f))
        self.bottomworld = float(self.read_int32(f))
        self.tileshigh = self.read_int32(f)
        self.tileswide = self.read_int32(f)

        self.gamemode = self.read_int32(f)
        self.drunkworld = self.read_boolean(f)
        self.goodworld = self.read_boolean(f)
        self.tenthanniversaryworld = self.read_boolean(f)
        self.dontstarveworld = self.read_boolean(f)
        self.notthebeesworld = self.read_boolean(f)
        self.remixworld = self.read_boolean(f)
        self.notrapworld = self.read_boolean(f)
        self.zenithworld = self.read_boolean(f)

        self.creationtime = self.read_int64(f)

        self.moontype = self.read_uint8(f)
        self.treeX[0] = self.read_int32(f)
        self.treeX[1] = self.read_int32(f)
        self.treeX[2] = self.read_int32(f)
        self.treeX0 = self.treeX[0]
        self.treeX1 = self.treeX[1]
        self.treeX2 = self.treeX[2]
        self.treestyle0 = self.read_int32(f)
        self.treestyle1 = self.read_int32(f)
        self.treestyle2 = self.read_int32(f)
        self.treestyle3 = self.read_int32(f)
        self.cavebackX[0] = self.read_int32(f)
        self.cavebackX[1] = self.read_int32(f)
        self.cavebackX[2] = self.read_int32(f)
        self.cavebackX0 = self.cavebackX[0]
        self.cavebackX1 = self.cavebackX[1]
        self.cavebackX2 = self.cavebackX[2]
        self.cavebackstyle0 = self.read_int32(f)
        self.cavebackstyle1 = self.read_int32(f)
        self.cavebackstyle2 = self.read_int32(f)
        self.cavebackstyle3 = self.read_int32(f)
        self.icebackstyle = self.read_int32(f)
        self.junglebackstyle = self.read_int32(f)
        self.hellbackstyle = self.read_int32(f)

        #TODO: 이 곳에서 더 진행할 것.

world = World_1_4_4()
world.loadV2()
print(world.__dict__)