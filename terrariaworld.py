import struct
import io
import uuid
import datetime
import numpy as np
import sys
import os
import random
from tiles import Tiles
from chest import Chest, Item
from sign import Sign
from enumeration import BrickStyle, Liquid, Ch, GameMode

class WorldFileFormatException(Exception):
    pass

class TerrariaWorld:
    #At least making these works for 1.4.4.....
    def __init__(self,
                 world_size:str = "large"):
        self.version:int = 279 #1.4.4
        self.ischinese:bool = False
        self.filerevision:int = 0
        self.isfavorite:bool = False
        self.__initializetileframeimportant()
        self.__HeaderFlags_init(world_size)
        self.tiles:Tiles = Tiles(self.tileswide, self.tileshigh)
        self.chests:list[Chest] = []
        self.signs:list[Sign] = []
        self.__initializeotherdata()

    def __initializetileframeimportant(self):
        '''
        This decides whether tile type is block or sprite.
        self.tileframeimportant[tiletype] == True means tile of #tiletype is sprite.
        THIS SHOULE BE UPDATED UPON 1.4.5 ARRIVES AS WELL
        '''
        self.tileframeimportant:list[bool] = [False, False, False, True, True, True, False, False, False, False, True, True, True, True, True, True, True, True, True, True, True, True, False, False, True, False, True, True, True, True, False, True, False, True, True, True, True, False, False, False, False, False, True, False, False, False, False, False, False, True, True, False, False, False, False, True, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, True, True, True, True, False, False, True, True, True, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, False, False, True, False, False, True, True, False, False, False, False, False, False, False, False, False, False, True, True, False, True, True, False, False, True, True, True, True, True, True, True, True, False, True, True, True, True, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, True, True, True, True, False, False, False, True, False, False, False, False, False, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, True, False, True, True, False, True, False, False, True, True, True, True, True, True, False, False, False, False, False, False, True, True, False, False, True, False, True, False, True, True, True, True, True, True, True, True, True, True, True, True, True, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True, False, False, False, True, True, True, True, True, True, True, True, True, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, False, False, True, False, True, True, True, True, True, False, False, True, True, False, False, False, False, False, False, False, False, False, True, True, False, True, True, True, False, False, False, False, False, False, False, False, False, True, False, False, False, False, True, True, True, False, True, True, True, True, True, True, True, False, False, False, False, False, False, False, True, True, True, True, True, True, True, False, True, False, False, False, False, False, True, True, True, True, True, True, True, True, True, True, False, False, False, False, False, False, False, False, False, True, True, False, False, False, True, True, True, True, True, False, False, False, False, True, True, False, False, True, True, True, False, True, True, True, False, False, False, False, False, True, True, True, True, True, True, True, True, True, True, True, False, False, False, False, False, False, True, True, True, True, True, True, False, False, False, True, True, True, True, True, True, True, True, True, True, True, False, False, False, True, True, False, False, False, True, False, False, False, True, True, True, True, True, True, True, True, False, True, True, False, False, True, False, True, False, False, False, False, False, True, True, False, False, True, True, True, False, False, False, False, False, False, True, True, True, True, True, True, True, True, True, True, False, True, True, True, True, True, False, False, False, False, True, False, False, False, True, True, True, True, False, True, True, True, True, True, True, True, True, True, True, False, True, True, True, False, False, False, True, True, False, True, True, True, True, True, True, True, False, False, False, False, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, True, True, True, True, True, True, False, False, False, False, True, True, True, True, False, True, False, False, True, False, True, True, False, True, True, True, True, True, True, True, True, True, True, True, True, True, False, True, True, True, False, True, False, False, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]

    def __initializeotherdata(self):
        self.NPCMobs_data = b'\x00\x00\x00\x00\x01%\x00\x00\x00\x00\x00\x97\xe3G\x00\xa0\x16F\x00s\x1c\x00\x00]\x02\x00\x00\x01\x00\x00\x00\x00\x00\x00'
        self.tile_entities_data = b'\x00\x00\x00\x00'
        self.pressure_plate_data = b'\x00\x00\x00\x00'
        self.town_manager_data = b'\x00\x00\x00\x00'
        self.bestiary_data = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        self.creative_power_data = b'\x01\x00\x00\x00\x01\x08\x00\x00\x00\x00\x00\x01\t\x00\x00\x01\n\x00\x00\x01\x0c\x00\x00\x00\x00\x00\x01\r\x00\x00\x00'

    def __HeaderFlags_init(self,
                           world_size:str):
        world_size = world_size.lower()
        if world_size not in ["small", "medium", "large"]:
            print("World size unknown. Set to large.")
            world_size = "large"
        self.title:str = None
        self.seed:str = str(random.randint(0, (1 << 31) - 1)) #random
        self.worldgenversion:int = 1198295875585 #taken
        self.worldguid:uuid.UUID = uuid.uuid1()
        self.worldid:int = random.randint(0, (1 << 31) - 1) #random
        self.leftworld:float = 0.0 #always float 0.0?
        self.topworld:float = 0.0 #always float 0.0?
        if world_size == "small":
            self.tileshigh:int = 1200
            self.tileswide:int = 4200
        elif world_size == "medium":
            self.tileshigh:int = 1800
            self.tileswide:int = 6400
        else: #large
            self.tileshigh:int = 2400
            self.tileswide:int = 8400
        self.bottomworld:float = float(self.tileshigh*16)
        self.rightworld:float = float(self.tileswide*16)
        self.gamemode:int = 0 #classic
        self.drunkworld:bool = False
        self.goodworld:bool = False
        self.tenthanniversaryworld:bool = False
        self.dontstarveworld:bool = False
        self.notthebeesworld:bool = False
        self.remixworld:bool = False
        self.notrapworld:bool = False
        self.zenithworld:bool = False
        self.creationtime:int = -8584768520111393488
        self.moontype:int = 0
        if world_size == "small":
            self.treeX:list[int] = [1754, 4200, 4200]
        elif world_size == "medium":
            self.treeX:list[int] = [3194, 5443, 6400]
        else:
            self.treeX:list[int] = [3187, 3585, 5542]
        self.treeX0:int = self.treeX[0]
        self.treeX1:int = self.treeX[1]
        self.treeX2:int = self.treeX[2]
        self.treestyle0:int = 0
        self.treestyle1:int = 0
        self.treestyle2:int = 0
        self.treestyle3:int = 0
        if world_size == "small":
            self.cavebackX:list[int] = [2263, 4200, 4200]
        elif world_size == "medium":
            self.cavebackX:list[int] = [1291, 4147, 6400]
        else:
            self.cavebackX:list[int] = [3014, 4885, 7204]
        self.cavebackX0:int = self.cavebackX[0]
        self.cavebackX1:int = self.cavebackX[1]
        self.cavebackX2:int = self.cavebackX[2]
        self.cavebackstyle0:int = 0
        self.cavebackstyle1:int = 0
        self.cavebackstyle2:int = 0
        self.cavebackstyle3:int = 0
        self.icebackstyle:int = 0
        self.junglebackstyle:int = 0
        self.hellbackstyle:int = 0
        if world_size == "small":
            self.spawnX:int = 2104
            self.spawnY:int = 204
            self.groundlevel:float = 314.0
            self.rocklevel:float = 416.0
        elif world_size == "medium":
            self.spawnX:int = 3204
            self.spawnY:int = 391
            self.groundlevel:float = 467.0
            self.rocklevel:float = 719.0
        else:
            self.spawnX:int = 4197
            self.spawnY:int = 427
            self.groundlevel:float = 532.0
            self.rocklevel:float = 904.0
        self.time:float = 27000.0
        self.daytime:bool = False
        self.moonphase:int = 0
        self.bloodmoon:bool = False
        self.iseclipse:bool = False
        if world_size == "small":
            self.dungeonX:int = 3441 #taken
            self.dungeonY:int = 243 #taken
        elif world_size == "medium":
            self.dungeonX:int = 583 #taken
            self.dungeonY:int = 312 #taken
        else: #large
            self.dungeonX:int = 7283 #taken
            self.dungeonY:int = 605 #taken
        self.iscrimson:bool = False
        self.downedboss1eyeofcthulhu:bool = False
        self.downedboss2eaterofworlds:bool = False
        self.downedboss3skeletron:bool = False
        self.downedqueenbee:bool = False
        self.downedmechboss1thedestroyer:bool = False
        self.downedmechboss2thetwins:bool = False
        self.downedmechboss3skeletronprime:bool = False
        self.downedmechbossany:bool = False
        self.downedplantboss:bool = False
        self.downedgolemboss:bool = False
        self.downedslimekingboss:bool = False
        self.savedgoblin:bool = False
        self.savedwizard:bool = False
        self.savedmech:bool = False
        self.downedgoblins:bool = False
        self.downedclown:bool = False
        self.downedfrost:bool = False
        self.downedpirates:bool = False
        self.shadoworbsmashed:bool = False
        self.spawnmeteor:bool = False
        self.shadoworbcount:int = 0
        self.altarcount:int = 0
        self.hardmode:bool = False
        self.partyofdoom:bool = False
        self.invasiondelay:int = 0
        self.invasionsize:int = 0
        self.invasiontype:int = 0
        self.invasionX:float = 0.0
        self.slimeraintime:float = 0.0
        self.sundialcooldown:int = 0
        self.israining:bool = False
        self.tempraintime:int = 0
        self.tempmaxrain:float = 0
        self.savedoretierscobalt:int = -1
        self.savedoretiersmythril:int = -1
        self.savedoretiersadamantitie:int = -1
        self.bgtree:int = 0
        self.bgcorruption:int = 0
        self.bgjungle:int = 0
        self.bgsnow:int = 0
        self.bghallow:int = 0
        self.bgcrimson:int = 0
        self.bgdesert:int = 0
        self.bgocean:int = 0
        self.cloudbgactive:float = -64089.0 #taken
        self.numclouds:int = 200
        self.windspeedset:float = 0.0
        self.anglers:list[str] = []
        self.savedangler:bool = False
        self.anglerquest:int = 28
        self.savedstylist:bool = False
        self.savedtaxcollector:bool = False
        self.savedgolfer:bool = False
        self.invasionsizestart:int = 0
        self.cultistdelay:int = 0
        self.killedmobs:list[int] = [0]*688
        self.fastforwardtime:bool = False
        self.downedfishron:bool = False
        self.downedmartians:bool = False
        self.downedlunaticcultist:bool = False
        self.downedmoonlord:bool = False
        self.downedhalloweenking:bool = False
        self.downedhalloweentree:bool = False
        self.downedchristmasqueen:bool = False
        self.downedsanta:bool = False
        self.downedchristmastree:bool = False
        self.downedcelestialsolar:bool = False
        self.downedcelestialvortex:bool = False
        self.downedcelestialnebula:bool = False
        self.downedcelestialstardust:bool = False
        self.celestialsolaractive:bool = False
        self.celestialvortexactive:bool = False
        self.celestialnebulaactive:bool = False
        self.celestialstardustactive:bool = False
        self.apocalypse:bool = False
        self.partymanual:bool = False
        self.partygenuine:bool = False
        self.partycooldown:int = False
        self.partyingnpcs:list[int] = []
        self.sandstormhappening:bool = False
        self.sandstormtimeleft:int = 0
        self.sandstormseverity:float = 0.0
        self.sandstormintendedseverity:float = 0.0
        self.savedbartender:bool = False
        self.downeddd2invasiont1:bool = False
        self.downeddd2invasiont2:bool = False
        self.downeddd2invasiont3:bool = False
        self.mushroombg:int = 0
        self.underworldbg:int = 0
        self.bgtree2:int = 0
        self.bgtree3:int = 0
        self.bgtree4:int = 0
        self.combatbookused:bool = False
        self.lanternnightcooldown:int = 0
        self.lanternnightgenuine:bool = False
        self.lanternnightmanual:bool = False
        self.lanternnightnextnightisgenuine:bool = False
        self.treetopvariations:list[int] = [0]*13
        self.forcehalloweenfortoday:bool = False
        self.forcexmasfortoday:bool = False
        self.savedoretierscopper:int = 7
        self.savedoretiersiron:int = 6
        self.savedoretierssilver:int = 9
        self.savedoretiersgold:int = 8
        self.boughtcat:bool = False
        self.boughtdog:bool = False
        self.boughtbunny:bool = False
        self.downedempressoflight:bool = False
        self.downedqueenslime:bool = False
        self.downeddeerclops:bool = False
        self.unlockedslimebluespawn:bool = False
        self.unlockedmerchantspawn:bool = False
        self.unlockeddemolitionistspawn:bool = False
        self.unlockedpartygirlspawn:bool = False
        self.unlockeddyetraderspawn:bool = False
        self.unlockedtrufflespawn:bool = False
        self.unlockedarmsdealerspawn:bool = False
        self.unlockednursespawn:bool = False
        self.unlockedprincessspawn:bool = False
        self.combatbookvolumetwowasused:bool = False
        self.peddlerssatchelwasused:bool = False
        self.unlockedslimegreenspawn:bool = False
        self.unlockedslimeoldspawn:bool = False
        self.unlockedslimepurplespawn:bool = False
        self.unlockedslimerainbowspawn:bool = False
        self.unlockedslimeredspawn:bool = False
        self.unlockedslimeyellowspawn:bool = False
        self.unlockedslimecopperspawn:bool = False
        self.fastforwardtimetodusk:bool = False
        self.moondialcooldown:bool = False

    def __getsectioncount(self):
        return 11 if self.version >= 220 else 10

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

    def write_boolean(self, f:io.BufferedWriter, data:bool):
        f.write(struct.pack('?', data))
    
    def write_int8(self, f:io.BufferedWriter, data:int):
        f.write(struct.pack('<b', data))
    
    def write_uint8(self, f:io.BufferedWriter, data:int):
        f.write(struct.pack('<B', data))
    
    def write_int16(self, f:io.BufferedWriter, data:int):
        f.write(struct.pack('<h', data))

    def write_uint16(self, f:io.BufferedWriter, data:int):
        f.write(struct.pack('<H', data))
    
    def write_int32(self, f:io.BufferedWriter, data:int):
        f.write(struct.pack('<i', data))
    
    def write_uint32(self, f:io.BufferedWriter, data:int):
        f.write(struct.pack('<I', data))
    
    def write_int64(self, f:io.BufferedWriter, data:int):
        f.write(struct.pack('<q', data))
    
    def write_uint64(self, f:io.BufferedWriter, data:int):
        f.write(struct.pack('<Q', data))
    
    def write_single(self, f:io.BufferedWriter, data:float):
        f.write(struct.pack('<f', data))
    
    def write_double(self, f:io.BufferedWriter, data:float):
        f.write(struct.pack('<d', data))

    def read_7bit_encoded_int(self, f): #THX chatgpt
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

    def write_7bit_encoded_int(self, f, value): #THX chatgpt
        while True:
            b = value & 0x7F
            value >>= 7
            if value:
                f.write(bytes([b | 0x80]))
            else:
                f.write(bytes([b]))
                break

    def read_string(self, f) -> str: #THX chatgpt
        strlen = self.read_7bit_encoded_int(f)
        return f.read(strlen).decode('utf-8')
    
    def write_string(self, f, s: str): #THX chatgpt
        data = s.encode('utf-8')
        self.write_7bit_encoded_int(f, len(data))
        f.write(data)

    def loadV2(self,
               chest_verbose=False,
               sign_verbose=False,
               skip_header_flags=False,
               skip_tile_data=False):
        with open(input("Map file path : "), "rb") as f:
            self.version = self.read_uint32(f)

            tileframeimportant, section_ptrs = self.__LoadSectionHeader(f)
            self.tileframeimportant = tileframeimportant

            if f.tell() != section_ptrs[0]:
                raise WorldFileFormatException("Unexpected Position: Invalid File Format Section")
            
            if skip_header_flags:
                f.seek(section_ptrs[1])
            else:
                self.__LoadHeaderFlags(f)
                if f.tell() != section_ptrs[1]:
                    raise WorldFileFormatException("Unexpected Position: Invalid Header Flags")

            if skip_tile_data:
                f.seek(section_ptrs[2])
            else:
                self.tiles = self.__LoadTileData(f, self.tileswide, self.tileshigh, self.version, tileframeimportant)
                if f.tell() != section_ptrs[2]:
                    print("Correcting Position Error")
                    f.seek(section_ptrs[2])

            self.chests = self.__LoadChestData(f, chest_verbose)
            if f.tell() != section_ptrs[3]:
                raise WorldFileFormatException("Unexpected Position: Invalid Chest Data")
            
            self.signs = self.__LoadSignData(f, sign_verbose)
            #여기 즈음에 sign 데이터의 tile type이 진짜 표지판의 종류인지 검사하는 코드가 원래 있었음
            if f.tell() != section_ptrs[4]:
                raise WorldFileFormatException("Unexpected Position: Invalid Sign Data")
            
            if self.version >= 140:
                NPCMobs_data_len = section_ptrs[5] - section_ptrs[4]
                self.NPCMobs_data = f.read(NPCMobs_data_len)
                if f.tell() != section_ptrs[5]:
                    raise WorldFileFormatException("Unexpected Position: Invalid Mob and NPC Data")
                tile_entities_data_len = section_ptrs[6] - section_ptrs[5]
                self.tile_entities_data = f.read(tile_entities_data_len)
                if f.tell() != section_ptrs[6]:
                    raise WorldFileFormatException("Unexpected Position: Invalid Tile Entities Section")
            else:
                NPCMobs_data_len = section_ptrs[5] - section_ptrs[4]
                self.NPCMobs_data = f.read(NPCMobs_data_len)
                if f.tell() != section_ptrs[5]:
                    raise WorldFileFormatException("Unexpected Position: Invalid NPC Data")
            
            if self.version >= 170:
                pressure_plate_data_len = section_ptrs[7] - section_ptrs[6]
                self.pressure_plate_data = f.read(pressure_plate_data_len)
                if f.tell() != section_ptrs[7]:
                    raise WorldFileFormatException("Unexpected Position: Invalid Weighted Pressure Plate Section")
            
            if self.version >= 189:
                town_manager_data_len = section_ptrs[8] - section_ptrs[7]
                self.town_manager_data = f.read(town_manager_data_len)
                if f.tell() != section_ptrs[8]:
                    raise WorldFileFormatException("Unexpected Position: Invalid Town Manager Section")
            
            if self.version >= 210:
                besitary_data_len = section_ptrs[9] - section_ptrs[8]
                self.bestiary_data = f.read(besitary_data_len)
                if f.tell() != section_ptrs[9]:
                    raise WorldFileFormatException("Unexpected Position: Invalid Bestiary Section")
            
            if self.version >= 220:
                creative_power_len = section_ptrs[10] - section_ptrs[9]
                self.creative_power_data = f.read(creative_power_len)
                if f.tell() != section_ptrs[10]:
                    raise WorldFileFormatException("Unexpected Position: Invalid Bestiary Section")
            
            self.__LoadFooter(f)            

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

        if self.version >= 140:
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
            self.boughtdog = self.read_boolean(f)
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
                       tileframeimportant:list[bool]) -> Tiles:
        tiles = Tiles(maxX, maxY)
        total_tiles = maxX*maxY
        digits = len(str(total_tiles))
        barlen = 30
        backspace = 25 + 2*digits + barlen
        for x in range(maxX):
            progess = int(barlen*x/maxX)
            if x:
                sys.stdout.write(f'\x1b[{backspace}D')
            sys.stdout.write(f"loading tile {x*maxY:>{digits}d}/{total_tiles} done... [{"="*progess}{" "*(barlen - progess)}]")
            y = 0
            while y < maxY:
                single_tile, rle = self.__deserializetiledata(f, tileframeimportant, version)
                tiles.tileinfos[x, y, :] = single_tile
                while rle > 0:
                    y += 1
                    tiles.tileinfos[x, y, :] = tiles.tileinfos[x, y - 1, :]
                    rle -= 1
                y += 1
        sys.stdout.write(f'\x1b[{backspace}D')
        sys.stdout.write(f"loading tile {total_tiles}/{total_tiles} done... [{"="*barlen}]\n")
        return tiles

    def __deserializetiledata(self, f, tileframeimportant, version) -> tuple[list, int]:
        single_tile = [0]*19
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
            if not (header1 & 0b0010_0000):
                tiletype = self.read_uint8(f)
            else:
                lowerbyte = self.read_uint8(f)
                tiletype = self.read_uint8(f)
                tiletype = (tiletype << 8) | lowerbyte
            single_tile[Ch.TILETYPE] = tiletype

            if not tileframeimportant[tiletype]:
                single_tile[Ch.U] = 0
                single_tile[Ch.V] = 0
            else:
                single_tile[Ch.U] = self.read_int16(f)
                single_tile[Ch.V] = self.read_int16(f)

                if single_tile[Ch.TILETYPE] == 144: #reset timers
                    single_tile[Ch.V] = 0
            
            if header3 & 0b0000_1000:
                single_tile[Ch.TILECOLOR] = self.read_uint8(f)
        else:
            single_tile[Ch.TILETYPE] = -1


        if header1 & 0b0000_0100:
            single_tile[Ch.WALL] = self.read_uint8(f)
            if ((header3 & 0b0001_0000) == 0b0001_0000):
                single_tile[Ch.WALLCOLOR] = self.read_uint8(f)
        
        liquidtype = (header1 & 0b0001_1000) >> 3
        if liquidtype != 0:
            single_tile[Ch.LIQUIDAMOUNT] = self.read_uint8(f)
            single_tile[Ch.LIQUIDTYPE] = liquidtype

            if version >= 269 and ((header3 & 0b1000_0000) == 0b1000_0000):
                single_tile[Ch.LIQUIDTYPE] = Liquid.SHIMMER
        
        if header2 > 1:
            if header2 & 0b0000_0010:
                single_tile[Ch.WIRERED] = True
            if header2 & 0b0000_0100:
                single_tile[Ch.WIREBLUE] = True
            if header2 & 0b0000_1000:
                single_tile[Ch.WIREGREEN] = True
        
            brickstyle = ((header2 & 0b0111_0000) >> 4)
            #TODO: 아마도 해당 타일의 종류가 경사를 실제로 가지는 지 검사하는 코드(1528번 줄)인 거 같음. 나중에 여유 있을 때 구현하자.
            single_tile[Ch.BRICKSTYLE] = brickstyle

        if header3 > 1:
            if header3 & 0b0000_0010:
                single_tile[Ch.ACTUACTOR] = True
            
            if header3 & 0b0000_0100:
                single_tile[Ch.INACTIVE] = True
            
            if header3 & 0b0010_0000:
                single_tile[Ch.WIREYELLOW] = True
            
            if version >= 222:
                if header3 & 0b0100_0000:
                    single_tile[Ch.WALL] = (self.read_uint8(f) << 8) | single_tile[Ch.WALL]
        
        if (version >= 269 and header4 > 1):
            if header4 & 0b_0000_0010:
                single_tile[Ch.INVISIBLEBLOCK] = True
            if header4 & 0b_0000_0100:
                single_tile[Ch.INVISIBLEWALL] = True
            if header4 & 0b_0000_1000:
                single_tile[Ch.FULLBRIGHTBLOCK] = True
            if header4 & 0b_0001_0000:
                single_tile[Ch.FULLBRIGHTWALL] = True
        
        rlestoragetype = (header1 & 192) >> 6
        if rlestoragetype == 0:
            rle = 0
        elif rlestoragetype == 1:
            rle = self.read_uint8(f)
        else:
            rle = self.read_int16(f)
        
        return single_tile, rle

    def __LoadChestData(self, f, chest_verbose) -> list[Chest]:
        total_chests = self.read_int16(f)
        max_items = self.read_int16(f)
        CHEST_MAX = 40

        if max_items > CHEST_MAX:
            items_per_chest = CHEST_MAX
            overflowitems = max_items - CHEST_MAX
        else:
            items_per_chest = max_items
            overflowitems = 0

        chests = []

        for i in range(total_chests):
            X = self.read_int32(f)
            Y = self.read_int32(f)
            name = self.read_string(f)
            chest = Chest(X, Y, name)

            for slot in range(items_per_chest):
                stacksize = self.read_int16(f)
                chest.items[slot].stacksize = stacksize

                if stacksize > 0:
                    item_id = self.read_int32(f)
                    prefix = self.read_uint8(f)

                    chest.items[slot].netid = item_id
                    chest.items[slot].stacksize = stacksize
                    chest.items[slot].prefix = prefix
        
            for overflow in range(overflowitems):
                stacksize = self.read_int16(f)
                if stacksize > 0:
                    self.read_int32(f)
                    self.read_uint8(f)
            
            chests.append(chest)
        
        if chest_verbose:
            for chest in chests:
                print(chest)

        return chests

    def __LoadSignData(self, f, sign_verbose) -> list[Sign]:
        totalsigns = self.read_int16(f)

        signs = []

        for i in range(totalsigns):
            text = self.read_string(f)
            x = self.read_int32(f)
            y = self.read_int32(f)
            sign = Sign(text, x, y)

            signs.append(sign)
        
        if sign_verbose:
            for sign in signs:
                print(sign)        

        return signs

    def __LoadFooter(self, f):
        boolean_footer = self.read_boolean(f)
        # print(f"{boolean_footer = }")
        if not boolean_footer:
            raise WorldFileFormatException("Invalid Boolean Footer")
        
        title_footer = self.read_string(f)
        # print(f"{title_footer = }")
        if title_footer != self.title:
            raise WorldFileFormatException("Invalid World Title Footer")
        
        world_id_footer = self.read_int32(f)
        # print(f"{world_id_footer = }")
        if world_id_footer != self.worldid:
            raise WorldFileFormatException("Invalid World ID Footer")

    def saveV2(self):
        save_file_path = input("Saving File Path : ")
        if not save_file_path.endswith(".wld"):
            save_file_path = save_file_path + ".wld"

        if self.title is None:
            self.title = os.path.basename(save_file_path)[:-4]

        sectionpointers = [None]*self.__getsectioncount()

        with open(save_file_path, "wb") as f:
            sectionpointers[0] = self.__SaveSectionHeader(f, self.tileframeimportant)
            sectionpointers[1] = self.__SaveHeaderFlags(f)
            sectionpointers[2] = self.__SaveTiles(f, self.tileswide, self.tileshigh, self.tileframeimportant)
            sectionpointers[3] = self.__SaveChests(f)
            sectionpointers[4] = self.__SaveSigns(f)

            if self.version >= 140:
                f.write(self.NPCMobs_data)
                sectionpointers[5] = f.tell()
                f.write(self.tile_entities_data)
                sectionpointers[6] = f.tell()
            else:
                f.write(self.NPCMobs_data)
                sectionpointers[5] = f.tell()
            
            if self.version >= 170:
                f.write(self.pressure_plate_data)
                sectionpointers[7] = f.tell()
            
            if self.version >= 189:
                f.write(self.town_manager_data)
                sectionpointers[8] = f.tell()
            
            if self.version >= 210:
                f.write(self.bestiary_data)
                sectionpointers[9] = f.tell()
            
            if self.version >= 220:
                f.write(self.creative_power_data)
                sectionpointers[10] = f.tell()
            
            self.__SaveFooter(f)
            self.__UpdateSectionPointers(f, sectionpointers)

    def __SaveSectionHeader(self, f:io.BufferedWriter, tileframeimportant) -> int:
        self.write_uint32(f, self.version)

        if self.version >= 140:
            if self.ischinese:
                f.write('xindong'.encode('ascii'))
            else:
                f.write('relogic'.encode('ascii'))
            
            self.write_uint8(f, 2)

            self.write_uint32(f, self.filerevision)

            worldheaderflags = 0
            if self.isfavorite:
                worldheaderflags |= 1
            self.write_uint64(f, worldheaderflags)

        sectioncount = self.__getsectioncount()
        self.write_int16(f, sectioncount)

        for _ in range(sectioncount):
            self.write_int32(f, 0)
        
        self.__WriteBitArray(f, tileframeimportant)
        return f.tell()
    
    def __WriteBitArray(self, f, tileframeimportant):
        self.write_int16(f, len(tileframeimportant))

        data = 0
        bitmask = 1
        for i in range(len(tileframeimportant)):
            if tileframeimportant[i]:
                data = data | bitmask
            if bitmask != 128:
                bitmask = bitmask << 1
            else:
                self.write_uint8(f, data)
                data = 0
                bitmask = 1
        
        if bitmask != 1:
            self.write_uint8(f, data)
    
    def __SaveHeaderFlags(self, f:io.BufferedWriter) -> int:
        self.write_string(f, self.title)

        if self.version >= 179:
            if self.version == 179:
                seed = int(self.seed)
                self.write_int32(f, seed)
            else:
                seed = int(self.seed)
                self.write_string(f, str(seed))
            self.write_uint64(f, self.worldgenversion)
        
        if self.version >= 181:
            f.write(self.worldguid.bytes)
        
        self.write_int32(f, self.worldid)
        self.write_int32(f, int(self.leftworld))
        self.write_int32(f, int(self.rightworld))
        self.write_int32(f, int(self.topworld))
        self.write_int32(f, int(self.bottomworld))
        self.write_int32(f, self.tileshigh)
        self.write_int32(f, self.tileswide)

        if self.version >= 209:
            self.write_int32(f, self.gamemode)
            
            if self.version >= 222: self.write_boolean(f, self.drunkworld)
            if self.version >= 227: self.write_boolean(f, self.goodworld)
            if self.version >= 238: self.write_boolean(f, self.tenthanniversaryworld)
            if self.version >= 239: self.write_boolean(f, self.dontstarveworld)
            if self.version >= 241: self.write_boolean(f, self.notthebeesworld)
            if self.version >= 249: self.write_boolean(f, self.remixworld)
            if self.version >= 266: self.write_boolean(f, self.notrapworld)
            if self.version >= 266: self.write_boolean(f, self.zenithworld)
        elif self.version == 208:
            self.write_boolean(f, self.gamemode == 2)
        elif self.version == 112:
            self.write_boolean(f, self.gamemode == 1)
        else:
            pass

        if self.version >= 141:
            self.write_int64(f, self.creationtime)
        
        self.write_uint8(f, self.moontype)
        self.write_int32(f, self.treeX0)
        self.write_int32(f, self.treeX1)
        self.write_int32(f, self.treeX2)
        self.write_int32(f, self.treestyle0)
        self.write_int32(f, self.treestyle1)
        self.write_int32(f, self.treestyle2)
        self.write_int32(f, self.treestyle3)
        self.write_int32(f, self.cavebackX0)
        self.write_int32(f, self.cavebackX1)
        self.write_int32(f, self.cavebackX2)
        self.write_int32(f, self.cavebackstyle0)
        self.write_int32(f, self.cavebackstyle1)
        self.write_int32(f, self.cavebackstyle2)
        self.write_int32(f, self.cavebackstyle3)
        self.write_int32(f, self.icebackstyle)
        self.write_int32(f, self.junglebackstyle)
        self.write_int32(f, self.hellbackstyle)

        self.write_int32(f, self.spawnX)
        self.write_int32(f, self.spawnY)
        self.write_double(f, self.groundlevel)
        self.write_double(f, self.rocklevel)
        self.write_double(f, self.time)
        self.write_boolean(f, self.daytime)
        self.write_int32(f, self.moonphase)
        self.write_boolean(f, self.bloodmoon)
        self.write_boolean(f, self.iseclipse)
        self.write_int32(f, self.dungeonX)
        self.write_int32(f, self.dungeonY)

        self.write_boolean(f, self.iscrimson)

        self.write_boolean(f, self.downedboss1eyeofcthulhu)
        self.write_boolean(f, self.downedboss2eaterofworlds)
        self.write_boolean(f, self.downedboss3skeletron)
        self.write_boolean(f, self.downedqueenbee)
        self.write_boolean(f, self.downedmechboss1thedestroyer)
        self.write_boolean(f, self.downedmechboss2thetwins)
        self.write_boolean(f, self.downedmechboss3skeletronprime)
        self.write_boolean(f, self.downedmechbossany)
        self.write_boolean(f, self.downedplantboss)
        self.write_boolean(f, self.downedgolemboss)

        if self.version >= 118: self.write_boolean(f, self.downedslimekingboss)

        self.write_boolean(f, self.savedgoblin)
        self.write_boolean(f, self.savedwizard)
        self.write_boolean(f, self.savedmech)
        self.write_boolean(f, self.downedgoblins)
        self.write_boolean(f, self.downedclown)
        self.write_boolean(f, self.downedfrost)
        self.write_boolean(f, self.downedpirates)

        self.write_boolean(f, self.shadoworbsmashed)
        self.write_boolean(f, self.spawnmeteor)
        self.write_uint8(f, self.shadoworbcount)
        self.write_int32(f, self.altarcount)
        self.write_boolean(f, self.hardmode)
        if self.version >= 257: self.write_boolean(f, self.partyofdoom)
        self.write_int32(f, self.invasiondelay)
        self.write_int32(f, self.invasionsize)
        self.write_int32(f, self.invasiontype)
        self.write_double(f, self.invasionX)
        if self.version >= 118: self.write_double(f, self.slimeraintime)
        if self.version >= 113: self.write_uint8(f, self.sundialcooldown)

        self.write_boolean(f, self.israining)
        self.write_int32(f, self.tempraintime)
        self.write_single(f, self.tempmaxrain)
        self.write_int32(f, self.savedoretierscobalt)
        self.write_int32(f, self.savedoretiersmythril)
        self.write_int32(f, self.savedoretiersadamantitie)
        self.write_uint8(f, self.bgtree)
        self.write_uint8(f, self.bgcorruption)
        self.write_uint8(f, self.bgjungle)
        self.write_uint8(f, self.bgsnow)
        self.write_uint8(f, self.bghallow)
        self.write_uint8(f, self.bgcrimson)
        self.write_uint8(f, self.bgdesert)
        self.write_uint8(f, self.bgocean)
        self.write_int32(f, int(self.cloudbgactive))
        self.write_int16(f, self.numclouds)
        self.write_single(f, self.windspeedset)

        if self.version < 95: return f.tell()

        self.write_int32(f, len(self.anglers))

        for angler in self.anglers:
            self.write_string(f, angler)
        
        if self.version < 99: return f.tell()

        self.write_boolean(f, self.savedangler)

        if self.version < 101: return f.tell()

        self.write_int32(f, self.anglerquest)

        if self.version < 104: return f.tell()

        self.write_boolean(f, self.savedstylist)

        if self.version >= 129:
            self.write_boolean(f, self.savedtaxcollector)
        if self.version >= 201:
            self.write_boolean(f, self.savedgolfer)
        if self.version >= 107:
            self.write_int32(f, self.invasionsizestart)
        if self.version >= 108:
            self.write_int32(f, self.cultistdelay)
        
        if self.version < 109: return f.tell()

        number_of_mobs = len(self.killedmobs)
        self.write_int16(f, number_of_mobs)
        for i in range(number_of_mobs):
            self.write_int32(f, self.killedmobs[i])
        
        if self.version < 128: return f.tell()

        if self.version >= 140:
            self.write_boolean(f, self.fastforwardtime)
        
        if self.version < 131: return f.tell()

        self.write_boolean(f, self.downedfishron)

        if self.version >= 140:
            self.write_boolean(f, self.downedmartians)
            self.write_boolean(f, self.downedlunaticcultist)
            self.write_boolean(f, self.downedmoonlord)

        self.write_boolean(f, self.downedhalloweenking)
        self.write_boolean(f, self.downedhalloweentree)
        self.write_boolean(f, self.downedchristmasqueen)
        self.write_boolean(f, self.downedsanta)
        self.write_boolean(f, self.downedchristmastree)

        if self.version < 140: return f.tell()

        self.write_boolean(f, self.downedcelestialsolar)
        self.write_boolean(f, self.downedcelestialvortex)
        self.write_boolean(f, self.downedcelestialnebula)
        self.write_boolean(f, self.downedcelestialstardust)
        self.write_boolean(f, self.celestialsolaractive)
        self.write_boolean(f, self.celestialvortexactive)
        self.write_boolean(f, self.celestialnebulaactive)
        self.write_boolean(f, self.celestialstardustactive)
        self.write_boolean(f, self.apocalypse)

        if self.version >= 170:
            self.write_boolean(f, self.partymanual)
            self.write_boolean(f, self.partygenuine)
            self.write_int32(f, self.partycooldown)
            numparty = len(self.partyingnpcs)
            self.write_int32(f, numparty)
            for i in range(numparty):
                self.write_int32(f, numparty[i])
        
        if self.version >= 174:
            self.write_boolean(f, self.sandstormhappening)
            self.write_int32(f, self.sandstormtimeleft)
            self.write_single(f, self.sandstormseverity)
            self.write_single(f, self.sandstormintendedseverity)

        if self.version >= 178:
            self.write_boolean(f, self.savedbartender)
            self.write_boolean(f, self.downeddd2invasiont1)
            self.write_boolean(f, self.downeddd2invasiont2)
            self.write_boolean(f, self.downeddd2invasiont3)

        if self.version > 194:
            self.write_uint8(f, self.mushroombg)

        if self.version >= 215:
            self.write_uint8(f, self.underworldbg)
        
        if self.version >= 195:
            self.write_uint8(f, self.bgtree2)
            self.write_uint8(f, self.bgtree3)
            self.write_uint8(f, self.bgtree4)

        if self.version >= 204:
            self.write_boolean(f, self.combatbookused)
        
        if self.version >= 207:
            self.write_int32(f, self.lanternnightcooldown)
            self.write_boolean(f, self.lanternnightgenuine)
            self.write_boolean(f, self.lanternnightmanual)
            self.write_boolean(f, self.lanternnightnextnightisgenuine)

        if self.version >= 211:
            numtrees = len(self.treetopvariations)
            self.write_int32(f, numtrees)
            for i in range(numtrees):
                self.write_int32(f, self.treetopvariations[i])

        if self.version >= 212:
            self.write_boolean(f, self.forcehalloweenfortoday)
            self.write_boolean(f, self.forcexmasfortoday)

        if self.version >= 216:
            self.write_int32(f, self.savedoretierscopper)
            self.write_int32(f, self.savedoretiersiron)
            self.write_int32(f, self.savedoretierssilver)
            self.write_int32(f, self.savedoretiersgold)
        
        if self.version >= 217:
            self.write_boolean(f, self.boughtcat)
            self.write_boolean(f, self.boughtdog)
            self.write_boolean(f, self.boughtbunny)

        if self.version >= 223:
            self.write_boolean(f, self.downedempressoflight)
            self.write_boolean(f, self.downedqueenslime)
        
        if self.version >= 240:
            self.write_boolean(f, self.downeddeerclops)
        
        if self.version >= 250:
            self.write_boolean(f, self.unlockedslimebluespawn)
        
        if self.version >= 251:
            self.write_boolean(f, self.unlockedmerchantspawn)
            self.write_boolean(f, self.unlockeddemolitionistspawn)
            self.write_boolean(f, self.unlockedpartygirlspawn)
            self.write_boolean(f, self.unlockeddyetraderspawn)
            self.write_boolean(f, self.unlockedtrufflespawn)
            self.write_boolean(f, self.unlockedarmsdealerspawn)
            self.write_boolean(f, self.unlockednursespawn)
            self.write_boolean(f, self.unlockedprincessspawn)
        
        if self.version >= 259:
            self.write_boolean(f, self.combatbookvolumetwowasused)
        
        if self.version >= 260:
            self.write_boolean(f, self.peddlerssatchelwasused)
        
        if self.version >= 261:
            self.write_boolean(f, self.unlockedslimegreenspawn)
            self.write_boolean(f, self.unlockedslimeoldspawn)
            self.write_boolean(f, self.unlockedslimepurplespawn)
            self.write_boolean(f, self.unlockedslimerainbowspawn)
            self.write_boolean(f, self.unlockedslimeredspawn)
            self.write_boolean(f, self.unlockedslimeyellowspawn)
            self.write_boolean(f, self.unlockedslimecopperspawn)
        
        if self.version >= 264:
            self.write_boolean(f, self.fastforwardtimetodusk)
            self.write_uint8(f, self.moondialcooldown)
        
        return f.tell()

    def __SaveTiles(self,
                    f:io.BufferedWriter,
                    maxX:int,
                    maxY:int,
                    tileframeimportant:list[bool]) -> int:
        self.tiles.exit_editmode()
        total_tiles = maxX*maxY
        digits = len(str(total_tiles))
        barlen = 30
        backspace = 24 + 2*digits + barlen
        for x in range(maxX):
            progess = int(barlen*x/maxX)
            if x:
                sys.stdout.write(f'\x1b[{backspace}D')
            sys.stdout.write(f"saving tile {x*maxY:>{digits}d}/{total_tiles} done... [{"="*progess}{" "*(barlen - progess)}]")
            y = 0
            while y < maxY:
                tile = self.tiles.tileinfos[x, y]
                tiledata, dataindex, headerindex = self.__serializeTilaData(tile)

                header1 = tiledata[headerindex]

                rle = 0
                nexty = y + 1
                remainingy = maxY - y - 1
                while (remainingy > 0 and all(tile == self.tiles.tileinfos[x, nexty]) and int(tile[Ch.TILETYPE]) != 520 and int(tile[Ch.TILETYPE]) != 423):
                    rle += 1
                    remainingy -= 1
                    nexty += 1
                
                y = y + rle

                if rle > 0:
                    tiledata[dataindex] = rle & 0b1111_1111
                    dataindex += 1

                    if rle <= 255:
                        header1 |= 0b0100_0000
                    else:
                        header1 |= 0b1000_0000
                        tiledata[dataindex] = (rle & 0b11111111_00000000) >> 8
                        dataindex += 1
                
                tiledata[headerindex] = header1
                try:
                    for idx in range(headerindex, dataindex):
                        self.write_uint8(f, tiledata[idx])
                except struct.error:
                    print(tiledata)
                    exit(1)
                y += 1
        sys.stdout.write(f'\x1b[{backspace}D')
        sys.stdout.write(f"saving tile {total_tiles}/{total_tiles} done... [{"="*barlen}]\n")
        return f.tell()
    
    def __serializeTilaData(self,
                            tile:np.ndarray) -> tuple[list[int], int, int]:
        size = 16 if self.version >= 269 else 15 if self.version > 22 else 13

        dataindex = 4 if self.version >= 269 else 3

        tiledata = [0]*size

        header4 = 0
        header3 = 0
        header2 = 0
        header1 = 0

        TYPE = int(tile[Ch.TILETYPE])
        ISACTIVE = (TYPE != -1)
        U = int(tile[Ch.U])
        V = int(tile[Ch.V])
        TILECOLOR = int(tile[Ch.TILECOLOR])
        FULLBRIGHTBLOCK = bool(tile[Ch.FULLBRIGHTBLOCK])
        WALL = int(tile[Ch.WALL])
        WALLCOLOR = int(tile[Ch.WALLCOLOR])
        FULLBRIGHTWALL = bool(tile[Ch.FULLBRIGHTWALL])
        LIQUIDAMOUNT = int(tile[Ch.LIQUIDAMOUNT])
        LIQUIDTYPE = int(tile[Ch.LIQUIDTYPE])
        WIRERED = bool(tile[Ch.WIRERED])
        WIREBLUE = bool(tile[Ch.WIREBLUE])
        WIREGREEN = bool(tile[Ch.WIREGREEN])
        BRICKSTYLE = int(tile[Ch.BRICKSTYLE])
        ACTUATER = bool(tile[Ch.ACTUACTOR])
        INACTIVE = bool(tile[Ch.INACTIVE])
        WIREYELLOW = bool(tile[Ch.WIREYELLOW])
        INVISIBLEBLOCK = bool(tile[Ch.INVISIBLEBLOCK])
        INVISIBLEWALL = bool(tile[Ch.INVISIBLEWALL])

        if ISACTIVE:
            header1 |= 0b0000_0010

            tiledata[dataindex] = TYPE%256
            dataindex += 1

            if tile[Ch.TILETYPE] > 255:
                tiledata[dataindex] = TYPE >> 8
                dataindex += 1
                header1 |= 0b0010_0000

            if self.tileframeimportant[TYPE]:
                tiledata[dataindex] = U & 0xFF
                dataindex += 1
                tiledata[dataindex] = (U & 0xFF00) >> 8
                dataindex += 1
                tiledata[dataindex] = V & 0xFF
                dataindex += 1
                tiledata[dataindex] = (V & 0xFF00) >> 8
                dataindex += 1
            
            if self.version < 269:
                if TILECOLOR != 0 or FULLBRIGHTBLOCK:
                    color = TILECOLOR

                    if color == 0 and FULLBRIGHTBLOCK:
                        color = 31
                    
                    header3 |= 0b0000_1000
                    tiledata[dataindex] = color
                    dataindex += 1
            else:
                if int(tile[Ch.TILECOLOR] != 0) and TILECOLOR != 31:
                    color = TILECOLOR

                    header3 |= 0b0000_1000
                    tiledata[dataindex] = color
                    dataindex += 1
        
        if WALL != 0:
            header1 |= 0b0000_0100
            tiledata[dataindex] = WALL%256
            dataindex += 1

            if self.version < 269:
                if WALLCOLOR != 0 or FULLBRIGHTWALL:
                    color = WALLCOLOR

                    if color == 0 and self.version < 269 and FULLBRIGHTWALL:
                        color = 31
                    
                    header3 |= 0b0001_0000
                    tiledata[dataindex] = color
                    dataindex += 1
            else:
                if WALLCOLOR != 0 and WALLCOLOR != 31:
                    color = WALLCOLOR
                    header3 |= 0b0001_0000
                    tiledata[dataindex] = color
                    dataindex += 1

        if LIQUIDAMOUNT != 0 and LIQUIDTYPE != Liquid.NONE:
            if self.version >= 269 and LIQUIDTYPE == Liquid.SHIMMER:
                header3 |= 0b1000_0000
                header1 |= 0b0000_1000
            elif LIQUIDTYPE == Liquid.LAVA:
                header1 |= 0b0001_0000
            elif LIQUIDTYPE == Liquid.HONEY:
                header1 |= 0b0001_1000
            else:
                header1 |= 0b0000_1000
            
            tiledata[dataindex] = LIQUIDAMOUNT
            dataindex += 1
        
        if WIRERED:
            header2 |= 0b0000_0010
        if WIREBLUE:
            header2 |= 0b0000_0100
        if WIREGREEN:
            header2 |= 0b0000_1000
        
        header2 |= (BRICKSTYLE << 4)

        if ACTUATER:
            header3 |= 0b0000_0010
        if INACTIVE:
            header3 |= 0b0000_0100
        if WIREYELLOW:
            header3 |= 0b0010_0000
        
        if WALL > 255 and self.version >= 222:
            header3 |= 0b0100_0000
            tiledata[dataindex] = WALL >> 8
            dataindex += 1
        
        if self.version >= 269:
            if INVISIBLEBLOCK:
                header4 |= 0b0000_0010
            if INVISIBLEWALL:
                header4 |= 0b0000_0100
            if FULLBRIGHTBLOCK or TILECOLOR == 31:
                header4 |= 0b0000_1000
            if FULLBRIGHTWALL or TILECOLOR == 31:
                header4 |= 0b0001_0000
            
            headerindex = 3
            if header4 != 0:
                header3 |= 0b0000_0001
                tiledata[headerindex] = header4
                headerindex -= 1
        else:
            headerindex = 2
        
        if header3 != 0:
            header2 |= 0b0000_0001
            tiledata[headerindex] = header3
            headerindex -= 1
        if header2 != 0:
            header1 |= 0b0000_0001
            tiledata[headerindex] = header2
            headerindex -= 1
        tiledata[headerindex] = header1
        return tiledata, dataindex, headerindex

    def __SaveChests(self, f:io.BufferedWriter):
        count = len(self.chests)
        self.write_int16(f, count)
        MAXITEMS = 40
        self.write_int16(f, MAXITEMS)

        for chest in self.chests:
            self.write_int32(f, chest.X)
            self.write_int32(f, chest.Y)
            self.write_string(f, chest.name)
            for slot in range(MAXITEMS):
                item:Item = chest.items[slot]
                stacksize = item.stacksize
                self.write_int16(f, stacksize)

                if stacksize > 0:
                    item_id = item.netid
                    prefix = item.prefix
                    self.write_int32(f, item_id)
                    self.write_uint8(f, prefix)
        
        return f.tell()
    
    def __SaveSigns(self, f:io.BufferedWriter):
        count = len(self.signs)
        self.write_int16(f, count)
        for sign in self.signs:
            text = sign.text
            x = sign.x
            y = sign.y
            self.write_string(f, text)
            self.write_int32(f, x)
            self.write_int32(f, y)
        
        return f.tell()

    def __SaveFooter(self, f:io.BufferedWriter):
        self.write_boolean(f, True)
        self.write_string(f, self.title)
        self.write_int32(f, self.worldid)

    def __UpdateSectionPointers(self, f:io.BufferedWriter, sectionpointers:list[int]):
        f.seek(0)
        self.write_int32(f, self.version)
        seeking_pos = 0x18 if self.version >= 140 else 0x04
        f.seek(seeking_pos)
        self.write_int16(f, len(sectionpointers))
        for i in range(len(sectionpointers)):
            self.write_int32(f, sectionpointers[i])

if __name__ == "__main__":
    print(Ch.TILETYPE)