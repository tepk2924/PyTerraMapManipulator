import struct
import io
import uuid
import datetime

class WorldFileFormatException(Exception):
    pass

class TerrariaWorld:
    #At least making these works for 1.4.4.....
    def __init__(self):
        self.version:int = None
        self.ischinese:bool = None
        self.filerevision:int = None
        self.isfavorite:bool = None
        self.tileframeimportant:list[bool] = None
        self.title:str = None
        self.seed:str = None
        self.worldgenversion:int = None
        self.worldguid:uuid.UUID = None
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
        self.spawnX:int = None
        self.spawnY:int = None
        self.groundlevel:float = None
        self.rocklevel:float = None
        self.time:float = None
        self.daytime:bool = None
        self.moonphase:int = None
        self.bloodmoon:bool = None
        self.iseclipse:bool = None
        self.dungeonX:int = None
        self.dungeonY:int = None
        self.iscrimson:bool = None
        self.downedboss1eyeofcthulhu:bool = None
        self.downedboss2eaterofworlds:bool = None
        self.downedboss3skeletron:bool = None
        self.downedqueenbee:bool = None
        self.downedmechboss1thedestroyer:bool = None
        self.downedmechboss2thetwins:bool = None
        self.downedmechboss3skeletronprime:bool = None
        self.downedmechbossany:bool = None
        self.downedplantboss:bool = None
        self.downedgolemboss:bool = None
        self.downedslimekingboss:bool = None
        self.savedgoblin:bool = None
        self.savedwizard:bool = None
        self.savedmech:bool = None
        self.downedgoblins:bool = None
        self.downedclown:bool = None
        self.downedfrost:bool = None
        self.downedpirates:bool = None
        self.shadoworbsmashed:bool = None
        self.spawnmeteor:bool = None
        self.shadoworbcount:int = None
        self.altarcount:int = None
        self.hardmode:bool = None
        self.partyofdoom:bool = None
        self.invasiondelay:int = None
        self.invasionsize:int = None
        self.invasiontype:int = None
        self.invasionX:float = None
        self.slimeraintime:float = None
        self.sundialcooldown:int = None
        self.israining:bool = None
        self.tempraintime:int = None
        self.tempmaxrain:float = None
        self.savedoretierscobalt:int = None
        self.savedoretiersmythril:int = None
        self.savedoretiersadamantitie:int = None
        self.bgtree:int = None
        self.bgcorruption:int = None
        self.bgjungle:int = None
        self.bgsnow:int = None
        self.bghallow:int = None
        self.bgcrimson:int = None
        self.bgdesert:int = None
        self.bgocean:int = None
        self.cloudbgactive:float = None
        self.numclouds:int = None
        self.windspeedset:float = None
        self.anglers:list[str] = []
        self.savedangler:bool = None
        self.anglerquest:int = None
        self.savedstylist:bool = None
        self.savedtaxcollector:bool = None
        self.savedgolfer:bool = None
        self.invasionsizestart:int = None
        self.cultistdelay:int = None
        self.killedmobs:list[int] = []
        self.fastforwardtime:bool = None
        self.downedfishron:bool = None
        self.downedmartians:bool = None
        self.downedlunaticcultist:bool = None
        self.downedmoonlord:bool = None
        self.downedhalloweenking:bool = None
        self.downedhalloweentree:bool = None
        self.downedchristmasqueen:bool = None
        self.downedsanta:bool = None
        self.downedchristmastree:bool = None
        self.downedcelestialsolar:bool = None
        self.downedcelestialvortex:bool = None
        self.downedcelestialnebula:bool = None
        self.downedcelestialstardust:bool = None
        self.celestialsolaractive:bool = None
        self.celestialvortexactive:bool = None
        self.celestialnebulaactive:bool = None
        self.celestialstardustactive:bool = None
        self.apocalypse:bool = None

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

    def read_single(self, f:io.BufferedReader) -> float:
        return struct.unpack('<f', f.read(4))[0]

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
        self.version = self.read_uint32(f)

        tileframeimportant, section_ptrs = self.LoadSectionHeader(f)
        self.tileframeimportant = tileframeimportant

        if f.tell() != section_ptrs[0]:
            raise WorldFileFormatException("Unexpected Position: Invalid File Format Section")
        
        self.LoadHeaderFlags(f)

        f.close()

    def LoadSectionHeader(self, f:io.BufferedReader):
        #loading section header
        if self.version >= 140:
            tmp = f.tell()
            self.ischinese = (f.read(1).decode('ascii') == 'x')
            f.seek(tmp)
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

        if self.version >= 179:
            if self.version == 179:
                #TODO: ???
                self.seed = str(self.read_int32(f))
            else:
                self.seed = self.read_string(f)
            self.worldgenversion = self.read_uint64(f)
        else:
            self.seed = ""
        if self.version >= 181:
            self.worldguid = uuid.UUID(bytes_le=f.read(16))
        else:
            self.worldguid = uuid.uuid1()

        self.worldid = self.read_int32(f)
        self.leftworld = float(self.read_int32(f))
        self.rightworld = float(self.read_int32(f))
        self.topworld = float(self.read_int32(f))
        self.bottomworld = float(self.read_int32(f))
        self.tileshigh = self.read_int32(f)
        self.tileswide = self.read_int32(f)

        if self.version >= 209:
            self.gamemode = self.read_int32(f)

            if self.version >= 222: self.drunkworld = self.read_boolean(f)
            if self.version >= 227: self.goodworld = self.read_boolean(f)
            if self.version >= 238: self.tenthanniversaryworld = self.read_boolean(f)
            if self.version >= 239: self.dontstarveworld = self.read_boolean(f)
            if self.version >= 241: self.notthebeesworld = self.read_boolean(f)
            if self.version >= 249: self.remixworld = self.read_boolean(f)
            if self.version >= 266: self.notrapworld = self.read_boolean(f)
            self.zenithworld = (self.remixworld and self.drunkworld) if self.version < 267 else self.read_boolean(f)
        elif self.version == 208:
            self.gamemode = 2 if self.read_boolean(f) else 0
        elif self.version == 112:
            self.gamemode = 1 if self.read_boolean(f) else 0
        else:
            self.gamemode = 0

        self.creationtime = self.read_int64(f) if self.version >= 141 else int(datetime.datetime.now().timestamp())

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

        self.spawnX = self.read_int32(f)
        self.spawnY = self.read_int32(f)
        self.groundlevel = self.read_double(f)
        self.rocklevel = self.read_double(f)
        self.time = self.read_double(f)
        self.daytime = self.read_boolean(f)
        self.moonphase = self.read_int32(f)
        self.bloodmoon = self.read_boolean(f)
        self.iseclipse = self.read_boolean(f)
        self.dungeonX = self.read_int32(f)
        self.dungeonY = self.read_int32(f)

        self.iscrimson = self.read_boolean(f)

        self.downedboss1eyeofcthulhu = self.read_boolean(f)
        self.downedboss2eaterofworlds = self.read_boolean(f)
        self.downedboss3skeletron = self.read_boolean(f)
        self.downedqueenbee = self.read_boolean(f)
        self.downedmechboss1thedestroyer = self.read_boolean(f)
        self.downedmechboss2thetwins = self.read_boolean(f)
        self.downedmechboss3skeletronprime = self.read_boolean(f)
        self.downedmechbossany = self.read_boolean(f)
        self.downedplantboss = self.read_boolean(f)
        self.downedgolemboss = self.read_boolean(f)

        if self.version >= 118: self.downedslimekingboss = self.read_boolean(f)

        self.savedgoblin = self.read_boolean(f)
        self.savedwizard = self.read_boolean(f)
        self.savedmech = self.read_boolean(f)
        self.downedgoblins = self.read_boolean(f)
        self.downedclown = self.read_boolean(f)
        self.downedfrost = self.read_boolean(f)
        self.downedpirates = self.read_boolean(f)

        self.shadoworbsmashed = self.read_boolean(f)
        self.spawnmeteor = self.read_boolean(f)
        self.shadoworbcount = self.read_uint8(f)
        self.altarcount = self.read_int32(f)
        self.hardmode = self.read_boolean(f)
        if self.version >= 257: self.partyofdoom = self.read_boolean(f)
        self.invasiondelay = self.read_int32(f)
        self.invasionsize = self.read_int32(f)
        self.invasiontype = self.read_int32(f)
        self.invasionX = self.read_double(f)
        if self.version >= 118: self.slimeraintime = self.read_double(f)
        if self.version >= 113: self.sundialcooldown = self.read_uint8(f)
        
        self.israining = self.read_boolean(f)
        self.tempraintime = self.read_int32(f)
        self.tempmaxrain = self.read_single(f)
        self.savedoretierscobalt = self.read_int32(f)
        self.savedoretiersmythril = self.read_int32(f)
        self.savedoretiersadamantitie = self.read_int32(f)
        self.bgtree = self.read_uint8(f)
        self.bgcorruption = self.read_uint8(f)
        self.bgjungle = self.read_uint8(f)
        self.bgsnow = self.read_uint8(f)
        self.bghallow = self.read_uint8(f)
        self.bgcrimson = self.read_uint8(f)
        self.bgdesert = self.read_uint8(f)
        self.bgocean = self.read_uint8(f)
        self.cloudbgactive = float(self.read_int32(f))
        self.numclouds = self.read_int16(f)
        self.windspeedset = self.read_single(f)
        
        if self.version < 95: return

        for _ in range(self.read_int32(f)):
            self.anglers.append(self.read_string(f))
        
        if self.version < 99: return

        self.savedangler = self.read_boolean(f)

        if self.version < 101: return
        self.anglerquest = self.read_int32(f)

        if self.version < 104: return

        self.savedstylist = self.read_boolean(f)

        if self.version >= 140:
            self.savedtaxcollector = self.read_boolean(f)
        if self.version >= 201:
            self.savedgolfer = self.read_boolean(f)
        if self.version >= 107:
            self.invasionsizestart = self.read_int32(f)
        self.cultistdelay = self.read_int32(f) if self.version >= 108 else 86400

        if self.version < 109: return

        self.killedmobs.clear()
        number_of_mobs = self.read_int16(f)
        for _ in range(number_of_mobs):
            self.killedmobs.append(self.read_int32(f))
        
        if self.version < 128: return

        if self.version > 140:
            self.fastforwardtime = self.read_boolean(f)
        
        if self.version < 131: return

        self.downedfishron = self.read_boolean(f)
        
        if self.version >= 140:
            self.downedmartians = self.read_boolean(f)
            self.downedlunaticcultist = self.read_boolean(f)
            self.downedmoonlord = self.read_boolean(f)
        
        self.downedhalloweenking = self.read_boolean(f)
        self.downedhalloweentree = self.read_boolean(f)
        self.downedchristmasqueen = self.read_boolean(f)
        self.downedsanta = self.read_boolean(f)
        self.downedchristmastree = self.read_boolean(f)

        if self.version < 140: return

        self.downedcelestialsolar = self.read_boolean(f)
        self.downedcelestialvortex = self.read_boolean(f)
        self.downedcelestialnebula = self.read_boolean(f)
        self.downedcelestialstardust = self.read_boolean(f)
        self.celestialsolaractive = self.read_boolean(f)
        self.celestialvortexactive = self.read_boolean(f)
        self.celestialnebulaactive = self.read_boolean(f)
        self.celestialstardustactive = self.read_boolean(f)
        self.apocalypse = self.read_boolean(f)

world = TerrariaWorld()
world.loadV2()
print(world.__dict__)