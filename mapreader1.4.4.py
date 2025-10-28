import struct
import io
import uuid
import datetime
import copy
from tile import Tile

class WorldFileFormatException(Exception):
    pass

class TerrariaWorld:
    #At least making these works for 1.4.4.....
    def __init__(self):
        self.__brickstyleenum()
        self.__liquidtypeenum()
        self.version:int = None
        self.ischinese:bool = None
        self.filerevision:int = None
        self.isfavorite:bool = None
        self.tileframeimportant:list[bool] = None
        self.__HeaderFlags_init()
        self.tiles:list[list[Tile]] = None
    
    def __brickstyleenum(self):
        self.FULL = 0x0
        self.HALFBRICK = 0x1
        self.SLOPETOPRIGHT = 0x2
        self.SLOPETOPLEFT = 0x3
        self.SLOPEBOTTOMRIGHT = 0x4
        self.SLOPEBOTTOMLEFT = 0x5

    def __liquidtypeenum(self):
        self.NONE = 0x0
        self.WATER = 0x01
        self.LAVA = 0x02
        self.HONEY = 0x03
        self.SHIMMER = 0x08

    def __HeaderFlags_init(self):
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
        self.partymanual:bool = None
        self.partygenuine:bool = None
        self.partycooldown:int = None
        self.partyingnpcs:list[int] = []
        self.sandstormhappening:bool = None
        self.sandstormtimeleft:int = None
        self.sandstormseverity:float = None
        self.sandstormintendedseverity:float = None
        self.savedbartender:bool = None
        self.downeddd2invasiont1:bool = None
        self.downeddd2invasiont2:bool = None
        self.downeddd2invasiont3:bool = None
        self.mushroombg:int = None
        self.underworldbg:int = None
        self.bgtree2:int = None
        self.bgtree3:int = None
        self.bgtree4:int = None
        self.combatbookused:bool = None
        self.lanternnightcooldown:int = None
        self.lanternnightgenuine:bool = None
        self.lanternnightmanual:bool = None
        self.lanternnightnextnightisgenuine:bool = None
        self.treetopvariations:list[int] = [0]*13
        self.forcehalloweenfortoday:bool = None
        self.forcexmasfortoday:bool = None
        self.savedoretierscopper:int = None
        self.savedoretiersiron:int = None
        self.savedoretierssilver:int = None
        self.savedoretiersgold:int = None
        self.boughtcat:bool = None
        self.boughtdog:bool = None
        self.boughtbunny:bool = None
        self.downedempressoflight:bool = None
        self.downedqueenslime:bool = None
        self.downeddeerclops:bool = None
        self.unlockedslimebluespawn:bool = None
        self.unlockedmerchantspawn:bool = None
        self.unlockeddemolitionistspawn:bool = None
        self.unlockedpartygirlspawn:bool = None
        self.unlockeddyetraderspawn:bool = None
        self.unlockedtrufflespawn:bool = None
        self.unlockedarmsdealerspawn:bool = None
        self.unlockednursespawn:bool = None
        self.unlockedprincessspawn:bool = None
        self.combatbookvolumetwowasused:bool = None
        self.peddlerssatchelwasused:bool = None
        self.unlockedslimegreenspawn:bool = None
        self.unlockedslimeoldspawn:bool = None
        self.unlockedslimepurplespawn:bool = None
        self.unlockedslimerainbowspawn:bool = None
        self.unlockedslimeredspawn:bool = None
        self.unlockedslimeyellowspawn:bool = None
        self.unlockedslimecopperspawn:bool = None
        self.fastforwardtimetodusk:bool = None
        self.moondialcooldown:bool = None

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
        f = open(input("Map file path : "), "rb")
        self.version = self.read_uint32(f)

        tileframeimportant, section_ptrs = self.__LoadSectionHeader(f)
        self.tileframeimportant = tileframeimportant

        if f.tell() != section_ptrs[0]:
            raise WorldFileFormatException("Unexpected Position: Invalid File Format Section")
        
        self.__LoadHeaderFlags(f)
        if f.tell() != section_ptrs[1]:
            raise WorldFileFormatException("Unexpected Position: Invalid Header Flags")

        self.tiles = self.__LoadTileData(f, self.tileswide, self.tileshigh, self.version, tileframeimportant)
        if f.tell() != section_ptrs[2]:
            print("Correcting Position Error")
            f.seek(section_ptrs[2])

        f.close()

    def __LoadSectionHeader(self, f:io.BufferedReader):
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
        
        tileframeimportant = self.__ReadBitArray(f)
        return tileframeimportant, section_ptrs
    
    def __ReadBitArray(self, f:io.BufferedReader):
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
    
    def __LoadHeaderFlags(self, f:io.BufferedReader):
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

        if self.version >= 170:
            self.partymanual = self.read_boolean(f)
            self.partygenuine = self.read_boolean(f)
            self.partycooldown = self.read_int32(f)
            numparty = self.read_int32(f)
            for _ in range(numparty):
                self.partyingnpcs.append(self.read_int32(f))
        
        if self.version >= 174:
            self.sandstormhappening = self.read_boolean(f)
            self.sandstormtimeleft = self.read_int32(f)
            self.sandstormseverity = self.read_single(f)
            self.sandstormintendedseverity = self.read_single(f)
        
        if self.version >= 178:
            self.savedbartender = self.read_boolean(f)
            self.downeddd2invasiont1 = self.read_boolean(f)
            self.downeddd2invasiont2 = self.read_boolean(f)
            self.downeddd2invasiont3 = self.read_boolean(f)
        
        if self.version > 194:
            self.mushroombg = self.read_uint8(f)
        
        if self.version >= 215:
            self.underworldbg = self.read_uint8(f)
        
        if self.version >= 195:
            self.bgtree2 = self.read_uint8(f)
            self.bgtree3 = self.read_uint8(f)
            self.bgtree4 = self.read_uint8(f)
        else:
            self.bgtree2 = self.bgtree
            self.bgtree3 = self.bgtree
            self.bgtree4 = self.bgtree

        if self.version >= 204:
            self.combatbookused = self.read_boolean(f)
        
        if self.version >= 207:
            self.lanternnightcooldown = self.read_int32(f)
            self.lanternnightgenuine = self.read_boolean(f)
            self.lanternnightmanual = self.read_boolean(f)
            self.lanternnightnextnightisgenuine = self.read_boolean(f)
        
        if self.version >= 211:
            numtrees = self.read_int32(f)
            self.treetopvariations = [0]*max([13, numtrees])
            for i in range(numtrees):
                self.treetopvariations[i] = self.read_int32(f)
        else:
            self.treetopvariations[0] = self.treestyle0
            self.treetopvariations[1] = self.treestyle1
            self.treetopvariations[2] = self.treestyle2
            self.treetopvariations[3] = self.treestyle3
            self.treetopvariations[4] = self.bgcorruption
            self.treetopvariations[5] = self.junglebackstyle
            self.treetopvariations[6] = self.bgsnow
            self.treetopvariations[7] = self.bghallow
            self.treetopvariations[8] = self.bgcrimson
            self.treetopvariations[9] = self.bgdesert
            self.treetopvariations[10] = self.bgocean
            self.treetopvariations[11] = self.mushroombg
            self.treetopvariations[12] = self.underworldbg

        if self.version >= 212:
            self.forcehalloweenfortoday = self.read_boolean(f)
            self.forcexmasfortoday = self.read_boolean(f)
        
        if self.version >= 216:
            self.savedoretierscopper = self.read_int32(f)
            self.savedoretiersiron = self.read_int32(f)
            self.savedoretierssilver = self.read_int32(f)
            self.savedoretiersgold = self.read_int32(f)
        else:
            self.savedoretierscopper = -1
            self.savedoretiersiron = -1
            self.savedoretierssilver = -1
            self.savedoretiersgold = -1
        
        if self.version >= 217:
            self.boughtcat = self.read_boolean(f)
            self.boughdog = self.read_boolean(f)
            self.boughtbunny = self.read_boolean(f)
        
        if self.version >= 223:
            self.downedempressoflight = self.read_boolean(f)
            self.downedqueenslime = self.read_boolean(f)
        
        if self.version >= 240:
            self.downeddeerclops = self.read_boolean(f)
        
        if self.version >= 250:
            self.unlockedslimebluespawn = self.read_boolean(f)
        
        if self.version >= 251:
            self.unlockedmerchantspawn = self.read_boolean(f)
            self.unlockeddemolitionistspawn = self.read_boolean(f)
            self.unlockedpartygirlspawn = self.read_boolean(f)
            self.unlockeddyetraderspawn = self.read_boolean(f)
            self.unlockedtrufflespawn = self.read_boolean(f)
            self.unlockedarmsdealerspawn = self.read_boolean(f)
            self.unlockednursespawn = self.read_boolean(f)
            self.unlockedprincessspawn = self.read_boolean(f)
        
        if self.version >= 259:
            self.combatbookvolumetwowasused = self.read_boolean(f)
        
        if self.version >= 260:
            self.peddlerssatchelwasused = self.read_boolean(f)
        
        if self.version >= 261:
            self.unlockedslimegreenspawn = self.read_boolean(f)
            self.unlockedslimeoldspawn = self.read_boolean(f)
            self.unlockedslimepurplespawn = self.read_boolean(f)
            self.unlockedslimerainbowspawn = self.read_boolean(f)
            self.unlockedslimeredspawn = self.read_boolean(f)
            self.unlockedslimeyellowspawn = self.read_boolean(f)
            self.unlockedslimecopperspawn = self.read_boolean(f)
        
        if self.version >= 264:
            self.fastforwardtimetodusk = self.read_boolean(f)
            self.moondialcooldown = self.read_uint8(f)
        
        return
    
    def __LoadTileData(self,
                       f:io.BufferedReader,
                       maxX:int,
                       maxY:int,
                       version:int,
                       tileframeimportant:list[bool]):
        tiles = [[None]*maxY for _ in range(maxX)]
        total_tiles = maxX*maxY
        for x in range(maxX):
            print(f"loading tile {x*maxY}/{total_tiles} done...")
            y = 0
            while y < maxY:
                tile, rle = self.__deserializetiledata(f, tileframeimportant, version)
                tiles[x][y] = tile
                while rle > 0:
                    y += 1
                    tiles[x][y] = copy.copy(tile)
                    rle -= 1
                y += 1
        return tiles

    def __deserializetiledata(self, f, tileframeimportant, version) -> tuple[Tile, int]:
        tile = Tile()
        tile.reset()
        tiletype = -1
        header4 = 0
        header3 = 0
        header2 = 0
        header1 = self.read_uint8(f)

        hasheader2 = False
        hasheader3 = False
        hasheader4 = False

        if header1 & 0b0000_0001:
            hasheader2 = True
            header2 = self.read_uint8(f)
        
        if hasheader2 and (header2 & 0b0000_0001):
            hasheader3 = True
            header3 = self.read_uint8(f)
        
        if version >= 269:
            if hasheader3 and (header3 & 0b0000_0001):
                hasheader4 = True
                header4 = self.read_uint8(f)
        
        isactive:bool = (header1 & 0b0000_0010) == 0b0000_0010

        if isactive:
            tile.isactive = isactive

            if not (header1 & 0b0010_0000):
                tiletype = self.read_uint8(f)
            else:
                lowerbyte = self.read_uint8(f)
                tiletype = self.read_uint8(f)
                tiletype = (tiletype << 8) | lowerbyte
            tile.type = tiletype

            if not tileframeimportant[tiletype]:
                tile.U = 0
                tile.V = 0
            else:
                tile.U = self.read_int16(f)
                tile.V = self.read_int16(f)

                if tile.type == 144: #reset timers
                    tile.V = 0
            
            if header3 & 0b0000_1000:
                tile.tilecolor = self.read_uint8(f)
        
        if header1 & 0b0000_0100:
            tile.wall = self.read_uint8(f)
            if ((header3 & 0b0001_0000) == 0b0001_0000):
                tile.wallcolor = self.read_uint8(f)
        
        liquidtype = (header1 & 0b0001_1000) >> 3
        if liquidtype != 0:
            tile.liquidamount = self.read_uint8(f)
            tile.liquidtype = liquidtype

            if version >= 269 and ((header3 & 0b1000_0000) == 0b1000_0000):
                tile.liquidtype = self.SHIMMER
        
        if header2 > 1:
            if header2 & 0b0000_0010:
                tile.wirered = True
            if header2 & 0b0000_0100:
                tile.wireblue = True
            if header2 & 0b0000_1000:
                tile.wiregreen = True
        
            brickstyle = ((header2 & 0b0111_0000) >> 4)
            #TODO: 아마도 해당 타일의 종류가 경사를 실제로 가지는 지 검사하는 코드(1528번 줄)인 거 같음. 나중에 여유 있을 때 구현하자.
            tile.brickstyle = brickstyle

        if header3 > 1:
            if header3 & 0b0000_0010:
                tile.actuator = True
            
            if header3 & 0b0000_0100:
                tile.inactive = True
            
            if header3 & 0b0010_0000:
                tile.wireyellow = True
            
            if version >= 222:
                if header3 & 0b0100_0000:
                    tile.wall = (self.read_uint8(f) << 8) | tile.wall
        
        if (version >= 269 and header4 > 1):
            if header4 & 0b_0000_0010:
                tile.invisibleblock = True
            if header4 & 0b_0000_0100:
                tile.invisiblewall = True
            if header4 & 0b_0000_1000:
                tile.fullbrightblock = True
            if header4 & 0b_0001_0000:
                tile.fullbrightwall = True
        
        rlestoragetype = (header1 & 192) >> 6
        if rlestoragetype == 0:
            rle = 0
        elif rlestoragetype == 1:
            rle = self.read_uint8(f)
        else:
            rle = self.read_int16(f)
        
        return tile, rle


world = TerrariaWorld()
world.loadV2()