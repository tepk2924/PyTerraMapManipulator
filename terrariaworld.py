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
from pressureplate import PressurePlate
from tileentity import TileEntity
from enumeration import BrickStyle, Liquid, Channel, GameMode, TileID, TileEntityType, ItemID

class WorldFileFormatException(Exception):
    pass

class WorldFileSaveError(Exception):
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
        self.pressure_plates:list[PressurePlate] = []
        self.tile_entities:list[TileEntity] = []
        self.__initializeotherdata()

    #SHOULE BE UPDATED UPON 1.4.5 ARRIVES
    def __initializetileframeimportant(self):
        '''
        This decides whether tile type is block or sprite.
        self.tileframeimportant[tiletype] == True means tile of #tiletype is sprite.
        THIS SHOULE BE UPDATED UPON 1.4.5 ARRIVES AS WELL
        '''
        self.tileframeimportant:list[bool] = [False, False, False, True, True, True, False, False, False, False, True, True, True, True, True, True, True, True, True, True, True, True, False, False, True, False, True, True, True, True, False, True, False, True, True, True, True, False, False, False, False, False, True, False, False, False, False, False, False, True, True, False, False, False, False, True, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, True, True, True, True, False, False, True, True, True, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, False, False, True, False, False, True, True, False, False, False, False, False, False, False, False, False, False, True, True, False, True, True, False, False, True, True, True, True, True, True, True, True, False, True, True, True, True, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, True, True, True, True, False, False, False, True, False, False, False, False, False, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, True, False, True, True, False, True, False, False, True, True, True, True, True, True, False, False, False, False, False, False, True, True, False, False, True, False, True, False, True, True, True, True, True, True, True, True, True, True, True, True, True, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True, False, False, False, True, True, True, True, True, True, True, True, True, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, False, False, True, False, True, True, True, True, True, False, False, True, True, False, False, False, False, False, False, False, False, False, True, True, False, True, True, True, False, False, False, False, False, False, False, False, False, True, False, False, False, False, True, True, True, False, True, True, True, True, True, True, True, False, False, False, False, False, False, False, True, True, True, True, True, True, True, False, True, False, False, False, False, False, True, True, True, True, True, True, True, True, True, True, False, False, False, False, False, False, False, False, False, True, True, False, False, False, True, True, True, True, True, False, False, False, False, True, True, False, False, True, True, True, False, True, True, True, False, False, False, False, False, True, True, True, True, True, True, True, True, True, True, True, False, False, False, False, False, False, True, True, True, True, True, True, False, False, False, True, True, True, True, True, True, True, True, True, True, True, False, False, False, True, True, False, False, False, True, False, False, False, True, True, True, True, True, True, True, True, False, True, True, False, False, True, False, True, False, False, False, False, False, True, True, False, False, True, True, True, False, False, False, False, False, False, True, True, True, True, True, True, True, True, True, True, False, True, True, True, True, True, False, False, False, False, True, False, False, False, True, True, True, True, False, True, True, True, True, True, True, True, True, True, True, False, True, True, True, False, False, False, True, True, False, True, True, True, True, True, True, True, False, False, False, False, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, True, True, True, True, True, True, False, False, False, False, True, True, True, True, False, True, False, False, True, False, True, True, False, True, True, True, True, True, True, True, True, True, True, True, True, True, False, True, True, True, False, True, False, False, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]

    def __initializeotherdata(self):
        self.NPCMobs_data = b'\x00\x00\x00\x00\x01%\x00\x00\x00\x00\x00\x97\xe3G\x00\xa0\x16F\x00s\x1c\x00\x00]\x02\x00\x00\x01\x00\x00\x00\x00\x00\x00'
        # self.tile_entities_data = b'\x00\x00\x00\x00'
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
        self.gamemode:int = GameMode.CLASSIC #classic
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

    def __read_boolean(self, f:io.BufferedReader) -> bool:
        return f.read(1) != b'\x00'

    def __read_int8(self, f:io.BufferedReader) -> int:
        return struct.unpack('<b', f.read(1))[0]

    def __read_uint8(self, f:io.BufferedReader) -> int:
        return struct.unpack('<B', f.read(1))[0]

    def __read_int16(self, f:io.BufferedReader) -> int:
        return struct.unpack('<h', f.read(2))[0]
    
    def __read_uint16(self, f:io.BufferedReader) -> int:
        return struct.unpack('<H', f.read(2))[0]

    def __read_int32(self, f:io.BufferedReader) -> int:
        return struct.unpack('<i', f.read(4))[0]
    
    def __read_uint32(self, f:io.BufferedReader) -> int:
        return struct.unpack('<I', f.read(4))[0]
    
    def __read_int64(self, f:io.BufferedReader) -> int:
        return struct.unpack('<q', f.read(8))[0]
    
    def __read_uint64(self, f:io.BufferedReader) -> int:
        return struct.unpack('<Q', f.read(8))[0]

    def __read_single(self, f:io.BufferedReader) -> float:
        return struct.unpack('<f', f.read(4))[0]

    def __read_double(self, f:io.BufferedReader) -> float:
        return struct.unpack('<d', f.read(8))[0]

    def __write_boolean(self, f:io.BufferedWriter, data:bool):
        f.write(struct.pack('?', data))
    
    def __write_int8(self, f:io.BufferedWriter, data:int):
        f.write(struct.pack('<b', data))
    
    def __write_uint8(self, f:io.BufferedWriter, data:int):
        f.write(struct.pack('<B', data))
    
    def __write_int16(self, f:io.BufferedWriter, data:int):
        f.write(struct.pack('<h', data))

    def __write_uint16(self, f:io.BufferedWriter, data:int):
        f.write(struct.pack('<H', data))
    
    def __write_int32(self, f:io.BufferedWriter, data:int):
        f.write(struct.pack('<i', data))
    
    def __write_uint32(self, f:io.BufferedWriter, data:int):
        f.write(struct.pack('<I', data))
    
    def __write_int64(self, f:io.BufferedWriter, data:int):
        f.write(struct.pack('<q', data))
    
    def __write_uint64(self, f:io.BufferedWriter, data:int):
        f.write(struct.pack('<Q', data))
    
    def __write_single(self, f:io.BufferedWriter, data:float):
        f.write(struct.pack('<f', data))
    
    def __write_double(self, f:io.BufferedWriter, data:float):
        f.write(struct.pack('<d', data))

    def __read_7bit_encoded_int(self, f): #THX chatgpt
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

    def __write_7bit_encoded_int(self, f, value): #THX chatgpt
        while True:
            b = value & 0x7F
            value >>= 7
            if value:
                f.write(bytes([b | 0x80]))
            else:
                f.write(bytes([b]))
                break

    def __read_string(self, f) -> str: #THX chatgpt
        strlen = self.__read_7bit_encoded_int(f)
        return f.read(strlen).decode('utf-8')
    
    def __write_string(self, f, s: str): #THX chatgpt
        data = s.encode('utf-8')
        self.__write_7bit_encoded_int(f, len(data))
        f.write(data)

    def load_world(self,
                   file_path=None,
                   chest_verbose=False,
                   sign_verbose=False,
                   skip_header_flags=False,
                   skip_tile_data=False,
                   ):
        if file_path is None:
            file_path = input("Map file path : ")
        with open(file_path, "rb") as f:
            self.version = self.__read_uint32(f)

            tileframeimportant, section_ptrs = self.__LoadSectionHeader(f)
            self.tileframeimportant = tileframeimportant

            if f.tell() != section_ptrs[0]:
                raise WorldFileFormatException("Unexpected Position: Invalid File Format Section")
            
            if skip_header_flags:
                f.seek(section_ptrs[1])
            else:
                #World Informations
                self.__LoadHeaderFlags(f)
                if f.tell() != section_ptrs[1]:
                    raise WorldFileFormatException("Unexpected Position: Invalid Header Flags")

            if skip_tile_data:
                f.seek(section_ptrs[2])
            else:
                #World Tile Datas
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
                self.tile_entities = self.__LoadTileEntity(f)
                if f.tell() != section_ptrs[6]:
                    raise WorldFileFormatException("Unexpected Position: Invalid Tile Entities Section")
            else:
                NPCMobs_data_len = section_ptrs[5] - section_ptrs[4]
                self.NPCMobs_data = f.read(NPCMobs_data_len)
                if f.tell() != section_ptrs[5]:
                    raise WorldFileFormatException("Unexpected Position: Invalid NPC Data")
            
            if self.version >= 170:
                #.wld file saves weighted pressure plates that were being stepped on while player exiting the world. Interesting.
                self.pressure_plates = self.__LoadPressurePlate(f)
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
            self.filerevision = self.__read_uint32(f)
            flags = self.__read_uint64(f)
            self.isfavorite = ((flags & 1) == 1)
        sectioncount = self.__read_int16(f)
        section_ptrs = []
        for _ in range(sectioncount):
            section_ptrs.append(self.__read_int32(f))
        
        tileframeimportant = self.__ReadBitArray(f)
        return tileframeimportant, section_ptrs
    
    def __ReadBitArray(self, f:io.BufferedReader):
        #read bit array
        bitarraylength = self.__read_int16(f)
        data = 0
        bitmask = 128
        booleans = [False]*bitarraylength
        for idx in range(bitarraylength):
            if bitmask != 128:
                bitmask = bitmask << 1
            else:
                data = self.__read_uint8(f)
                bitmask = 1
            if data & bitmask == bitmask:
                booleans[idx] = True
        return booleans
    
    def __LoadHeaderFlags(self, f:io.BufferedReader):
        self.title = self.__read_string(f)

        if self.version >= 179:
            if self.version == 179:
                #TODO: ???
                self.seed = str(self.__read_int32(f))
            else:
                self.seed = self.__read_string(f)
            self.worldgenversion = self.__read_uint64(f)
        else:
            self.seed = ""
        if self.version >= 181:
            self.worldguid = uuid.UUID(bytes_le=f.read(16))
        else:
            self.worldguid = uuid.uuid1()

        self.worldid = self.__read_int32(f)
        self.leftworld = float(self.__read_int32(f))
        self.rightworld = float(self.__read_int32(f))
        self.topworld = float(self.__read_int32(f))
        self.bottomworld = float(self.__read_int32(f))
        self.tileshigh = self.__read_int32(f)
        self.tileswide = self.__read_int32(f)

        if self.version >= 209:
            self.gamemode = self.__read_int32(f)

            if self.version >= 222: self.drunkworld = self.__read_boolean(f)
            if self.version >= 227: self.goodworld = self.__read_boolean(f)
            if self.version >= 238: self.tenthanniversaryworld = self.__read_boolean(f)
            if self.version >= 239: self.dontstarveworld = self.__read_boolean(f)
            if self.version >= 241: self.notthebeesworld = self.__read_boolean(f)
            if self.version >= 249: self.remixworld = self.__read_boolean(f)
            if self.version >= 266: self.notrapworld = self.__read_boolean(f)
            self.zenithworld = (self.remixworld and self.drunkworld) if self.version < 267 else self.__read_boolean(f)
        elif self.version == 208:
            self.gamemode = 2 if self.__read_boolean(f) else 0
        elif self.version == 112:
            self.gamemode = 1 if self.__read_boolean(f) else 0
        else:
            self.gamemode = 0

        self.creationtime = self.__read_int64(f) if self.version >= 141 else int(datetime.datetime.now().timestamp())

        self.moontype = self.__read_uint8(f)
        self.treeX[0] = self.__read_int32(f)
        self.treeX[1] = self.__read_int32(f)
        self.treeX[2] = self.__read_int32(f)
        self.treeX0 = self.treeX[0]
        self.treeX1 = self.treeX[1]
        self.treeX2 = self.treeX[2]
        self.treestyle0 = self.__read_int32(f)
        self.treestyle1 = self.__read_int32(f)
        self.treestyle2 = self.__read_int32(f)
        self.treestyle3 = self.__read_int32(f)
        self.cavebackX[0] = self.__read_int32(f)
        self.cavebackX[1] = self.__read_int32(f)
        self.cavebackX[2] = self.__read_int32(f)
        self.cavebackX0 = self.cavebackX[0]
        self.cavebackX1 = self.cavebackX[1]
        self.cavebackX2 = self.cavebackX[2]
        self.cavebackstyle0 = self.__read_int32(f)
        self.cavebackstyle1 = self.__read_int32(f)
        self.cavebackstyle2 = self.__read_int32(f)
        self.cavebackstyle3 = self.__read_int32(f)
        self.icebackstyle = self.__read_int32(f)
        self.junglebackstyle = self.__read_int32(f)
        self.hellbackstyle = self.__read_int32(f)

        self.spawnX = self.__read_int32(f)
        self.spawnY = self.__read_int32(f)
        self.groundlevel = self.__read_double(f)
        self.rocklevel = self.__read_double(f)
        self.time = self.__read_double(f)
        self.daytime = self.__read_boolean(f)
        self.moonphase = self.__read_int32(f)
        self.bloodmoon = self.__read_boolean(f)
        self.iseclipse = self.__read_boolean(f)
        self.dungeonX = self.__read_int32(f)
        self.dungeonY = self.__read_int32(f)

        self.iscrimson = self.__read_boolean(f)

        self.downedboss1eyeofcthulhu = self.__read_boolean(f)
        self.downedboss2eaterofworlds = self.__read_boolean(f)
        self.downedboss3skeletron = self.__read_boolean(f)
        self.downedqueenbee = self.__read_boolean(f)
        self.downedmechboss1thedestroyer = self.__read_boolean(f)
        self.downedmechboss2thetwins = self.__read_boolean(f)
        self.downedmechboss3skeletronprime = self.__read_boolean(f)
        self.downedmechbossany = self.__read_boolean(f)
        self.downedplantboss = self.__read_boolean(f)
        self.downedgolemboss = self.__read_boolean(f)

        if self.version >= 118: self.downedslimekingboss = self.__read_boolean(f)

        self.savedgoblin = self.__read_boolean(f)
        self.savedwizard = self.__read_boolean(f)
        self.savedmech = self.__read_boolean(f)
        self.downedgoblins = self.__read_boolean(f)
        self.downedclown = self.__read_boolean(f)
        self.downedfrost = self.__read_boolean(f)
        self.downedpirates = self.__read_boolean(f)

        self.shadoworbsmashed = self.__read_boolean(f)
        self.spawnmeteor = self.__read_boolean(f)
        self.shadoworbcount = self.__read_uint8(f)
        self.altarcount = self.__read_int32(f)
        self.hardmode = self.__read_boolean(f)
        if self.version >= 257: self.partyofdoom = self.__read_boolean(f)
        self.invasiondelay = self.__read_int32(f)
        self.invasionsize = self.__read_int32(f)
        self.invasiontype = self.__read_int32(f)
        self.invasionX = self.__read_double(f)
        if self.version >= 118: self.slimeraintime = self.__read_double(f)
        if self.version >= 113: self.sundialcooldown = self.__read_uint8(f)
        
        self.israining = self.__read_boolean(f)
        self.tempraintime = self.__read_int32(f)
        self.tempmaxrain = self.__read_single(f)
        self.savedoretierscobalt = self.__read_int32(f)
        self.savedoretiersmythril = self.__read_int32(f)
        self.savedoretiersadamantitie = self.__read_int32(f)
        self.bgtree = self.__read_uint8(f)
        self.bgcorruption = self.__read_uint8(f)
        self.bgjungle = self.__read_uint8(f)
        self.bgsnow = self.__read_uint8(f)
        self.bghallow = self.__read_uint8(f)
        self.bgcrimson = self.__read_uint8(f)
        self.bgdesert = self.__read_uint8(f)
        self.bgocean = self.__read_uint8(f)
        self.cloudbgactive = float(self.__read_int32(f))
        self.numclouds = self.__read_int16(f)
        self.windspeedset = self.__read_single(f)
        
        if self.version < 95: return

        for _ in range(self.__read_int32(f)):
            self.anglers.append(self.__read_string(f))
        
        if self.version < 99: return

        self.savedangler = self.__read_boolean(f)

        if self.version < 101: return

        self.anglerquest = self.__read_int32(f)

        if self.version < 104: return

        self.savedstylist = self.__read_boolean(f)

        if self.version >= 140:
            self.savedtaxcollector = self.__read_boolean(f)
        if self.version >= 201:
            self.savedgolfer = self.__read_boolean(f)
        if self.version >= 107:
            self.invasionsizestart = self.__read_int32(f)
        self.cultistdelay = self.__read_int32(f) if self.version >= 108 else 86400

        if self.version < 109: return

        self.killedmobs.clear()
        number_of_mobs = self.__read_int16(f)
        for _ in range(number_of_mobs):
            self.killedmobs.append(self.__read_int32(f))
        
        if self.version < 128: return

        if self.version >= 140:
            self.fastforwardtime = self.__read_boolean(f)
        
        if self.version < 131: return

        self.downedfishron = self.__read_boolean(f)
        
        if self.version >= 140:
            self.downedmartians = self.__read_boolean(f)
            self.downedlunaticcultist = self.__read_boolean(f)
            self.downedmoonlord = self.__read_boolean(f)
        
        self.downedhalloweenking = self.__read_boolean(f)
        self.downedhalloweentree = self.__read_boolean(f)
        self.downedchristmasqueen = self.__read_boolean(f)
        self.downedsanta = self.__read_boolean(f)
        self.downedchristmastree = self.__read_boolean(f)

        if self.version < 140: return

        self.downedcelestialsolar = self.__read_boolean(f)
        self.downedcelestialvortex = self.__read_boolean(f)
        self.downedcelestialnebula = self.__read_boolean(f)
        self.downedcelestialstardust = self.__read_boolean(f)
        self.celestialsolaractive = self.__read_boolean(f)
        self.celestialvortexactive = self.__read_boolean(f)
        self.celestialnebulaactive = self.__read_boolean(f)
        self.celestialstardustactive = self.__read_boolean(f)
        self.apocalypse = self.__read_boolean(f)

        if self.version >= 170:
            self.partymanual = self.__read_boolean(f)
            self.partygenuine = self.__read_boolean(f)
            self.partycooldown = self.__read_int32(f)
            numparty = self.__read_int32(f)
            for _ in range(numparty):
                self.partyingnpcs.append(self.__read_int32(f))
        
        if self.version >= 174:
            self.sandstormhappening = self.__read_boolean(f)
            self.sandstormtimeleft = self.__read_int32(f)
            self.sandstormseverity = self.__read_single(f)
            self.sandstormintendedseverity = self.__read_single(f)
        
        if self.version >= 178:
            self.savedbartender = self.__read_boolean(f)
            self.downeddd2invasiont1 = self.__read_boolean(f)
            self.downeddd2invasiont2 = self.__read_boolean(f)
            self.downeddd2invasiont3 = self.__read_boolean(f)
        
        if self.version > 194:
            self.mushroombg = self.__read_uint8(f)
        
        if self.version >= 215:
            self.underworldbg = self.__read_uint8(f)
        
        if self.version >= 195:
            self.bgtree2 = self.__read_uint8(f)
            self.bgtree3 = self.__read_uint8(f)
            self.bgtree4 = self.__read_uint8(f)
        else:
            self.bgtree2 = self.bgtree
            self.bgtree3 = self.bgtree
            self.bgtree4 = self.bgtree

        if self.version >= 204:
            self.combatbookused = self.__read_boolean(f)
        
        if self.version >= 207:
            self.lanternnightcooldown = self.__read_int32(f)
            self.lanternnightgenuine = self.__read_boolean(f)
            self.lanternnightmanual = self.__read_boolean(f)
            self.lanternnightnextnightisgenuine = self.__read_boolean(f)
        
        if self.version >= 211:
            numtrees = self.__read_int32(f)
            self.treetopvariations = [0]*max([13, numtrees])
            for i in range(numtrees):
                self.treetopvariations[i] = self.__read_int32(f)
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
            self.forcehalloweenfortoday = self.__read_boolean(f)
            self.forcexmasfortoday = self.__read_boolean(f)
        
        if self.version >= 216:
            self.savedoretierscopper = self.__read_int32(f)
            self.savedoretiersiron = self.__read_int32(f)
            self.savedoretierssilver = self.__read_int32(f)
            self.savedoretiersgold = self.__read_int32(f)
        else:
            self.savedoretierscopper = -1
            self.savedoretiersiron = -1
            self.savedoretierssilver = -1
            self.savedoretiersgold = -1
        
        if self.version >= 217:
            self.boughtcat = self.__read_boolean(f)
            self.boughtdog = self.__read_boolean(f)
            self.boughtbunny = self.__read_boolean(f)
        
        if self.version >= 223:
            self.downedempressoflight = self.__read_boolean(f)
            self.downedqueenslime = self.__read_boolean(f)
        
        if self.version >= 240:
            self.downeddeerclops = self.__read_boolean(f)
        
        if self.version >= 250:
            self.unlockedslimebluespawn = self.__read_boolean(f)
        
        if self.version >= 251:
            self.unlockedmerchantspawn = self.__read_boolean(f)
            self.unlockeddemolitionistspawn = self.__read_boolean(f)
            self.unlockedpartygirlspawn = self.__read_boolean(f)
            self.unlockeddyetraderspawn = self.__read_boolean(f)
            self.unlockedtrufflespawn = self.__read_boolean(f)
            self.unlockedarmsdealerspawn = self.__read_boolean(f)
            self.unlockednursespawn = self.__read_boolean(f)
            self.unlockedprincessspawn = self.__read_boolean(f)
        
        if self.version >= 259:
            self.combatbookvolumetwowasused = self.__read_boolean(f)
        
        if self.version >= 260:
            self.peddlerssatchelwasused = self.__read_boolean(f)
        
        if self.version >= 261:
            self.unlockedslimegreenspawn = self.__read_boolean(f)
            self.unlockedslimeoldspawn = self.__read_boolean(f)
            self.unlockedslimepurplespawn = self.__read_boolean(f)
            self.unlockedslimerainbowspawn = self.__read_boolean(f)
            self.unlockedslimeredspawn = self.__read_boolean(f)
            self.unlockedslimeyellowspawn = self.__read_boolean(f)
            self.unlockedslimecopperspawn = self.__read_boolean(f)
        
        if self.version >= 264:
            self.fastforwardtimetodusk = self.__read_boolean(f)
            self.moondialcooldown = self.__read_uint8(f)
        
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
        header1 = self.__read_uint8(f)

        hasheader2 = False
        hasheader3 = False
        hasheader4 = False

        if header1 & 0b0000_0001:
            hasheader2 = True
            header2 = self.__read_uint8(f)
        
        if hasheader2 and (header2 & 0b0000_0001):
            hasheader3 = True
            header3 = self.__read_uint8(f)
        
        if version >= 269:
            if hasheader3 and (header3 & 0b0000_0001):
                hasheader4 = True
                header4 = self.__read_uint8(f)
        
        isactive:bool = (header1 & 0b0000_0010) == 0b0000_0010

        if isactive:
            if not (header1 & 0b0010_0000):
                tiletype = self.__read_uint8(f)
            else:
                lowerbyte = self.__read_uint8(f)
                tiletype = self.__read_uint8(f)
                tiletype = (tiletype << 8) | lowerbyte
            single_tile[Channel.TILETYPE] = tiletype

            if not tileframeimportant[tiletype]:
                single_tile[Channel.FRAMEX] = 0
                single_tile[Channel.FRAMEY] = 0
            else:
                single_tile[Channel.FRAMEX] = self.__read_int16(f)
                single_tile[Channel.FRAMEY] = self.__read_int16(f)

                if single_tile[Channel.TILETYPE] == 144: #reset timers
                    single_tile[Channel.FRAMEY] = 0
            
            if header3 & 0b0000_1000:
                single_tile[Channel.TILECOLOR] = self.__read_uint8(f)
        else:
            single_tile[Channel.TILETYPE] = -1


        if header1 & 0b0000_0100:
            single_tile[Channel.WALL] = self.__read_uint8(f)
            if ((header3 & 0b0001_0000) == 0b0001_0000):
                single_tile[Channel.WALLCOLOR] = self.__read_uint8(f)
        
        liquidtype = (header1 & 0b0001_1000) >> 3
        if liquidtype != 0:
            single_tile[Channel.LIQUIDAMOUNT] = self.__read_uint8(f)
            single_tile[Channel.LIQUIDTYPE] = liquidtype

            if version >= 269 and ((header3 & 0b1000_0000) == 0b1000_0000):
                single_tile[Channel.LIQUIDTYPE] = Liquid.SHIMMER
        
        if header2 > 1:
            if header2 & 0b0000_0010:
                single_tile[Channel.WIRERED] = True
            if header2 & 0b0000_0100:
                single_tile[Channel.WIREBLUE] = True
            if header2 & 0b0000_1000:
                single_tile[Channel.WIREGREEN] = True
        
            brickstyle = ((header2 & 0b0111_0000) >> 4)
            #TODO: 아마도 해당 타일의 종류가 경사를 실제로 가지는 지 검사하는 코드(1528번 줄)인 거 같음. 나중에 여유 있을 때 구현하자.
            single_tile[Channel.BRICKSTYLE] = brickstyle

        if header3 > 1:
            if header3 & 0b0000_0010:
                single_tile[Channel.ACTUACTOR] = True
            
            if header3 & 0b0000_0100:
                single_tile[Channel.INACTIVE] = True
            
            if header3 & 0b0010_0000:
                single_tile[Channel.WIREYELLOW] = True
            
            if version >= 222:
                if header3 & 0b0100_0000:
                    single_tile[Channel.WALL] = (self.__read_uint8(f) << 8) | single_tile[Channel.WALL]
        
        if (version >= 269 and header4 > 1):
            if header4 & 0b_0000_0010:
                single_tile[Channel.INVISIBLEBLOCK] = True
            if header4 & 0b_0000_0100:
                single_tile[Channel.INVISIBLEWALL] = True
            if header4 & 0b_0000_1000:
                single_tile[Channel.FULLBRIGHTBLOCK] = True
            if header4 & 0b_0001_0000:
                single_tile[Channel.FULLBRIGHTWALL] = True
        
        rlestoragetype = (header1 & 192) >> 6
        if rlestoragetype == 0:
            rle = 0
        elif rlestoragetype == 1:
            rle = self.__read_uint8(f)
        else:
            rle = self.__read_int16(f)
        
        return single_tile, rle

    def __LoadChestData(self, f, chest_verbose) -> list[Chest]:
        total_chests = self.__read_int16(f)
        max_items = self.__read_int16(f)
        CHEST_MAX = 40

        if max_items > CHEST_MAX:
            items_per_chest = CHEST_MAX
            overflowitems = max_items - CHEST_MAX
        else:
            items_per_chest = max_items
            overflowitems = 0

        chests = []

        for i in range(total_chests):
            X = self.__read_int32(f)
            Y = self.__read_int32(f)
            name = self.__read_string(f)
            chest = Chest(X, Y, name)

            for slot in range(items_per_chest):
                stacksize = self.__read_int16(f)
                chest.items[slot].stacksize = stacksize

                if stacksize > 0:
                    item_id = self.__read_int32(f)
                    prefix = self.__read_uint8(f)

                    chest.items[slot].netid = item_id
                    chest.items[slot].stacksize = stacksize
                    chest.items[slot].prefix = prefix
        
            for overflow in range(overflowitems):
                stacksize = self.__read_int16(f)
                if stacksize > 0:
                    self.__read_int32(f)
                    self.__read_uint8(f)
            
            chests.append(chest)
        
        if chest_verbose:
            for chest in chests:
                print(chest)

        return chests

    def __LoadSignData(self, f, sign_verbose) -> list[Sign]:
        totalsigns = self.__read_int16(f)

        signs = []

        for i in range(totalsigns):
            text = self.__read_string(f)
            x = self.__read_int32(f)
            y = self.__read_int32(f)
            sign = Sign(text, x, y)

            signs.append(sign)
        
        if sign_verbose:
            for sign in signs:
                print(sign)        

        return signs

    def __LoadTileEntity(self, f:io.BufferedReader) -> list[TileEntity]:
        count = self.__read_int32(f)
        ret = []
        for counter in range(count):
            entity_type = self.__read_uint8(f)
            entity_id = self.__read_int32(f)
            posX = self.__read_int16(f)
            posY = self.__read_int16(f)
            entity = TileEntity(type=entity_type,
                                entity_id=entity_id,
                                posX=posX,
                                posY=posY)
            
            if entity_type == TileEntityType.TrainingDummy:
                entity.attribute["npc"] = self.__read_int16(f)
            elif entity_type in [TileEntityType.ItemFrame,
                                 TileEntityType.WeaponRack,
                                 TileEntityType.FoodPlatter]:
                entity.attribute["item"] = self.__LoadItem4TileEntity(f)
            elif entity_type == TileEntityType.LogicSensor:
                entity.attribute["logiccheck"] = self.__read_uint8(f)
                entity.attribute["on"] = self.__read_boolean(f)
            elif entity_type == TileEntityType.DisplayDoll:
                item_bitmask = self.__read_uint8(f)
                dye_bitmask = self.__read_uint8(f)
                items:list[Item] = [Item() for _ in range(8)]
                dyes:list[Item] = [Item() for _ in range(8)]
                for idx in range(8):
                    if item_bitmask & (1 << idx):
                        items[idx] = self.__LoadItem4TileEntity(f)
                for idx in range(8):
                    if dye_bitmask & (1 << idx):
                        dyes[idx] = self.__LoadItem4TileEntity(f)
                entity.attribute["items"] = items
                entity.attribute["dyes"] = dyes
            elif entity_type == TileEntityType.HatRack:
                slots_bitmask = self.__read_uint8(f)
                items:list[Item] = [Item() for _ in range(2)]
                dyes:list[Item] = [Item() for _ in range(2)]
                for idx in range(2):
                    if slots_bitmask & (1 << idx):
                        items[idx] = self.__LoadItem4TileEntity(f)
                for idx in range(2):
                    if slots_bitmask & (1 << (idx + 2)):
                        items[idx] = self.__LoadItem4TileEntity(f)
                entity.attribute["items"] = items
                entity.attribute["dyes"] = dyes
            elif entity_type == TileEntityType.TeleportationPylon:
                pass
            else:
                raise WorldFileFormatException("Unknown TileEntity Type.")
            ret.append(entity)
        return ret

    def __LoadItem4TileEntity(self, f) -> Item:
        netid = self.__read_int16(f)
        prefix = self.__read_uint8(f)
        stacksize = self.__read_int16(f)
        return Item(netid=netid, prefix=prefix, stacksize=stacksize)


    def __LoadPressurePlate(self, f) -> list[PressurePlate]:
        count = self.__read_int32(f)
        ret = []
        for counter in range(count):
            posX = self.__read_int32(f)
            posY = self.__read_int32(f)
            ret.append(PressurePlate(posX, posY))
        return ret

    def __LoadFooter(self, f):
        boolean_footer = self.__read_boolean(f)
        # print(f"{boolean_footer = }")
        if not boolean_footer:
            raise WorldFileFormatException("Invalid Boolean Footer")
        
        title_footer = self.__read_string(f)
        # print(f"{title_footer = }")
        if title_footer != self.title:
            raise WorldFileFormatException("Invalid World Title Footer")
        
        world_id_footer = self.__read_int32(f)
        # print(f"{world_id_footer = }")
        if world_id_footer != self.worldid:
            raise WorldFileFormatException("Invalid World ID Footer")

    def place_sprite(self,
                     row:int,
                     col:int,
                     sprite_number:int,
                     sprite_rownum:int,
                     sprite_colnum:int,
                     frame_X_shift:int=0,
                     frame_Y_shift:int=0):
        self.tiles.tileinfos[row:row + sprite_rownum, col:col + sprite_colnum, Channel.TILETYPE] = sprite_number
        for r in range(sprite_rownum):
            for c in range(sprite_colnum):
                self.tiles.tileinfos[row + r, col + c, Channel.FRAMEX] = 18*c + frame_X_shift
                self.tiles.tileinfos[row + r, col + c, Channel.FRAMEY] = 18*r + frame_Y_shift

    def place_chest(self,
                    row:int,
                    col:int,
                    item_list:list[Item],
                    frame_X_shift:int=0,
                    frame_Y_shift:int=0):
        self.place_sprite(row, col, TileID.Containers, 2, 2, frame_X_shift, frame_Y_shift)
        chest = Chest(col, row, "")
        if len(item_list) > 40:
            item_list = item_list[:40]
            print("Item list is too long (more than 40). Taking the first 40 items")
        for idx in range(len(item_list)):
            chest.items[idx] = item_list[idx]
        self.chests.append(chest)
    
    def place_chest_group2(self,
                           row:int,
                           col:int,
                           item_list:list[Item],
                           frame_X_shift:int=0,
                           frame_Y_shift:int=0):
        self.place_sprite(row, col, TileID.Containers2, 2, 2, frame_X_shift, frame_Y_shift)
        chest = Chest(col, row, "")
        if len(item_list) > 40:
            item_list = item_list[:40]
            print("Item list is too long (more than 40). Taking the first 40 items")
        for idx in range(len(item_list)):
            chest.items[idx] = item_list[idx]
        self.chests.append(chest)

    def save_world(self,
                   save_file_path:str=None):
        if save_file_path is None:
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
                sectionpointers[6] = self.__SaveTileEntity(f)
            else:
                f.write(self.NPCMobs_data)
                sectionpointers[5] = f.tell()
            
            if self.version >= 170:
                sectionpointers[7] = self.__SavePressurePlate(f)
            
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
        self.__write_uint32(f, self.version)

        if self.version >= 140:
            if self.ischinese:
                f.write('xindong'.encode('ascii'))
            else:
                f.write('relogic'.encode('ascii'))
            
            self.__write_uint8(f, 2)

            self.__write_uint32(f, self.filerevision)

            worldheaderflags = 0
            if self.isfavorite:
                worldheaderflags |= 1
            self.__write_uint64(f, worldheaderflags)

        sectioncount = self.__getsectioncount()
        self.__write_int16(f, sectioncount)

        for _ in range(sectioncount):
            self.__write_int32(f, 0)
        
        self.__WriteBitArray(f, tileframeimportant)
        return f.tell()
    
    def __WriteBitArray(self, f, tileframeimportant):
        self.__write_int16(f, len(tileframeimportant))

        data = 0
        bitmask = 1
        for i in range(len(tileframeimportant)):
            if tileframeimportant[i]:
                data = data | bitmask
            if bitmask != 128:
                bitmask = bitmask << 1
            else:
                self.__write_uint8(f, data)
                data = 0
                bitmask = 1
        
        if bitmask != 1:
            self.__write_uint8(f, data)
    
    def __SaveHeaderFlags(self, f:io.BufferedWriter) -> int:
        self.__write_string(f, self.title)

        if self.version >= 179:
            if self.version == 179:
                seed = int(self.seed)
                self.__write_int32(f, seed)
            else:
                seed = int(self.seed)
                self.__write_string(f, str(seed))
            self.__write_uint64(f, self.worldgenversion)
        
        if self.version >= 181:
            f.write(self.worldguid.bytes)
        
        self.__write_int32(f, self.worldid)
        self.__write_int32(f, int(self.leftworld))
        self.__write_int32(f, int(self.rightworld))
        self.__write_int32(f, int(self.topworld))
        self.__write_int32(f, int(self.bottomworld))
        self.__write_int32(f, self.tileshigh)
        self.__write_int32(f, self.tileswide)

        if self.version >= 209:
            self.__write_int32(f, self.gamemode)
            
            if self.version >= 222: self.__write_boolean(f, self.drunkworld)
            if self.version >= 227: self.__write_boolean(f, self.goodworld)
            if self.version >= 238: self.__write_boolean(f, self.tenthanniversaryworld)
            if self.version >= 239: self.__write_boolean(f, self.dontstarveworld)
            if self.version >= 241: self.__write_boolean(f, self.notthebeesworld)
            if self.version >= 249: self.__write_boolean(f, self.remixworld)
            if self.version >= 266: self.__write_boolean(f, self.notrapworld)
            if self.version >= 266: self.__write_boolean(f, self.zenithworld)
        elif self.version == 208:
            self.__write_boolean(f, self.gamemode == 2)
        elif self.version == 112:
            self.__write_boolean(f, self.gamemode == 1)
        else:
            pass

        if self.version >= 141:
            self.__write_int64(f, self.creationtime)
        
        self.__write_uint8(f, self.moontype)
        self.__write_int32(f, self.treeX0)
        self.__write_int32(f, self.treeX1)
        self.__write_int32(f, self.treeX2)
        self.__write_int32(f, self.treestyle0)
        self.__write_int32(f, self.treestyle1)
        self.__write_int32(f, self.treestyle2)
        self.__write_int32(f, self.treestyle3)
        self.__write_int32(f, self.cavebackX0)
        self.__write_int32(f, self.cavebackX1)
        self.__write_int32(f, self.cavebackX2)
        self.__write_int32(f, self.cavebackstyle0)
        self.__write_int32(f, self.cavebackstyle1)
        self.__write_int32(f, self.cavebackstyle2)
        self.__write_int32(f, self.cavebackstyle3)
        self.__write_int32(f, self.icebackstyle)
        self.__write_int32(f, self.junglebackstyle)
        self.__write_int32(f, self.hellbackstyle)

        self.__write_int32(f, self.spawnX)
        self.__write_int32(f, self.spawnY)
        self.__write_double(f, self.groundlevel)
        self.__write_double(f, self.rocklevel)
        self.__write_double(f, self.time)
        self.__write_boolean(f, self.daytime)
        self.__write_int32(f, self.moonphase)
        self.__write_boolean(f, self.bloodmoon)
        self.__write_boolean(f, self.iseclipse)
        self.__write_int32(f, self.dungeonX)
        self.__write_int32(f, self.dungeonY)

        self.__write_boolean(f, self.iscrimson)

        self.__write_boolean(f, self.downedboss1eyeofcthulhu)
        self.__write_boolean(f, self.downedboss2eaterofworlds)
        self.__write_boolean(f, self.downedboss3skeletron)
        self.__write_boolean(f, self.downedqueenbee)
        self.__write_boolean(f, self.downedmechboss1thedestroyer)
        self.__write_boolean(f, self.downedmechboss2thetwins)
        self.__write_boolean(f, self.downedmechboss3skeletronprime)
        self.__write_boolean(f, self.downedmechbossany)
        self.__write_boolean(f, self.downedplantboss)
        self.__write_boolean(f, self.downedgolemboss)

        if self.version >= 118: self.__write_boolean(f, self.downedslimekingboss)

        self.__write_boolean(f, self.savedgoblin)
        self.__write_boolean(f, self.savedwizard)
        self.__write_boolean(f, self.savedmech)
        self.__write_boolean(f, self.downedgoblins)
        self.__write_boolean(f, self.downedclown)
        self.__write_boolean(f, self.downedfrost)
        self.__write_boolean(f, self.downedpirates)

        self.__write_boolean(f, self.shadoworbsmashed)
        self.__write_boolean(f, self.spawnmeteor)
        self.__write_uint8(f, self.shadoworbcount)
        self.__write_int32(f, self.altarcount)
        self.__write_boolean(f, self.hardmode)
        if self.version >= 257: self.__write_boolean(f, self.partyofdoom)
        self.__write_int32(f, self.invasiondelay)
        self.__write_int32(f, self.invasionsize)
        self.__write_int32(f, self.invasiontype)
        self.__write_double(f, self.invasionX)
        if self.version >= 118: self.__write_double(f, self.slimeraintime)
        if self.version >= 113: self.__write_uint8(f, self.sundialcooldown)

        self.__write_boolean(f, self.israining)
        self.__write_int32(f, self.tempraintime)
        self.__write_single(f, self.tempmaxrain)
        self.__write_int32(f, self.savedoretierscobalt)
        self.__write_int32(f, self.savedoretiersmythril)
        self.__write_int32(f, self.savedoretiersadamantitie)
        self.__write_uint8(f, self.bgtree)
        self.__write_uint8(f, self.bgcorruption)
        self.__write_uint8(f, self.bgjungle)
        self.__write_uint8(f, self.bgsnow)
        self.__write_uint8(f, self.bghallow)
        self.__write_uint8(f, self.bgcrimson)
        self.__write_uint8(f, self.bgdesert)
        self.__write_uint8(f, self.bgocean)
        self.__write_int32(f, int(self.cloudbgactive))
        self.__write_int16(f, self.numclouds)
        self.__write_single(f, self.windspeedset)

        if self.version < 95: return f.tell()

        self.__write_int32(f, len(self.anglers))

        for angler in self.anglers:
            self.__write_string(f, angler)
        
        if self.version < 99: return f.tell()

        self.__write_boolean(f, self.savedangler)

        if self.version < 101: return f.tell()

        self.__write_int32(f, self.anglerquest)

        if self.version < 104: return f.tell()

        self.__write_boolean(f, self.savedstylist)

        if self.version >= 129:
            self.__write_boolean(f, self.savedtaxcollector)
        if self.version >= 201:
            self.__write_boolean(f, self.savedgolfer)
        if self.version >= 107:
            self.__write_int32(f, self.invasionsizestart)
        if self.version >= 108:
            self.__write_int32(f, self.cultistdelay)
        
        if self.version < 109: return f.tell()

        number_of_mobs = len(self.killedmobs)
        self.__write_int16(f, number_of_mobs)
        for i in range(number_of_mobs):
            self.__write_int32(f, self.killedmobs[i])
        
        if self.version < 128: return f.tell()

        if self.version >= 140:
            self.__write_boolean(f, self.fastforwardtime)
        
        if self.version < 131: return f.tell()

        self.__write_boolean(f, self.downedfishron)

        if self.version >= 140:
            self.__write_boolean(f, self.downedmartians)
            self.__write_boolean(f, self.downedlunaticcultist)
            self.__write_boolean(f, self.downedmoonlord)

        self.__write_boolean(f, self.downedhalloweenking)
        self.__write_boolean(f, self.downedhalloweentree)
        self.__write_boolean(f, self.downedchristmasqueen)
        self.__write_boolean(f, self.downedsanta)
        self.__write_boolean(f, self.downedchristmastree)

        if self.version < 140: return f.tell()

        self.__write_boolean(f, self.downedcelestialsolar)
        self.__write_boolean(f, self.downedcelestialvortex)
        self.__write_boolean(f, self.downedcelestialnebula)
        self.__write_boolean(f, self.downedcelestialstardust)
        self.__write_boolean(f, self.celestialsolaractive)
        self.__write_boolean(f, self.celestialvortexactive)
        self.__write_boolean(f, self.celestialnebulaactive)
        self.__write_boolean(f, self.celestialstardustactive)
        self.__write_boolean(f, self.apocalypse)

        if self.version >= 170:
            self.__write_boolean(f, self.partymanual)
            self.__write_boolean(f, self.partygenuine)
            self.__write_int32(f, self.partycooldown)
            numparty = len(self.partyingnpcs)
            self.__write_int32(f, numparty)
            for i in range(numparty):
                self.__write_int32(f, numparty[i])
        
        if self.version >= 174:
            self.__write_boolean(f, self.sandstormhappening)
            self.__write_int32(f, self.sandstormtimeleft)
            self.__write_single(f, self.sandstormseverity)
            self.__write_single(f, self.sandstormintendedseverity)

        if self.version >= 178:
            self.__write_boolean(f, self.savedbartender)
            self.__write_boolean(f, self.downeddd2invasiont1)
            self.__write_boolean(f, self.downeddd2invasiont2)
            self.__write_boolean(f, self.downeddd2invasiont3)

        if self.version > 194:
            self.__write_uint8(f, self.mushroombg)

        if self.version >= 215:
            self.__write_uint8(f, self.underworldbg)
        
        if self.version >= 195:
            self.__write_uint8(f, self.bgtree2)
            self.__write_uint8(f, self.bgtree3)
            self.__write_uint8(f, self.bgtree4)

        if self.version >= 204:
            self.__write_boolean(f, self.combatbookused)
        
        if self.version >= 207:
            self.__write_int32(f, self.lanternnightcooldown)
            self.__write_boolean(f, self.lanternnightgenuine)
            self.__write_boolean(f, self.lanternnightmanual)
            self.__write_boolean(f, self.lanternnightnextnightisgenuine)

        if self.version >= 211:
            numtrees = len(self.treetopvariations)
            self.__write_int32(f, numtrees)
            for i in range(numtrees):
                self.__write_int32(f, self.treetopvariations[i])

        if self.version >= 212:
            self.__write_boolean(f, self.forcehalloweenfortoday)
            self.__write_boolean(f, self.forcexmasfortoday)

        if self.version >= 216:
            self.__write_int32(f, self.savedoretierscopper)
            self.__write_int32(f, self.savedoretiersiron)
            self.__write_int32(f, self.savedoretierssilver)
            self.__write_int32(f, self.savedoretiersgold)
        
        if self.version >= 217:
            self.__write_boolean(f, self.boughtcat)
            self.__write_boolean(f, self.boughtdog)
            self.__write_boolean(f, self.boughtbunny)

        if self.version >= 223:
            self.__write_boolean(f, self.downedempressoflight)
            self.__write_boolean(f, self.downedqueenslime)
        
        if self.version >= 240:
            self.__write_boolean(f, self.downeddeerclops)
        
        if self.version >= 250:
            self.__write_boolean(f, self.unlockedslimebluespawn)
        
        if self.version >= 251:
            self.__write_boolean(f, self.unlockedmerchantspawn)
            self.__write_boolean(f, self.unlockeddemolitionistspawn)
            self.__write_boolean(f, self.unlockedpartygirlspawn)
            self.__write_boolean(f, self.unlockeddyetraderspawn)
            self.__write_boolean(f, self.unlockedtrufflespawn)
            self.__write_boolean(f, self.unlockedarmsdealerspawn)
            self.__write_boolean(f, self.unlockednursespawn)
            self.__write_boolean(f, self.unlockedprincessspawn)
        
        if self.version >= 259:
            self.__write_boolean(f, self.combatbookvolumetwowasused)
        
        if self.version >= 260:
            self.__write_boolean(f, self.peddlerssatchelwasused)
        
        if self.version >= 261:
            self.__write_boolean(f, self.unlockedslimegreenspawn)
            self.__write_boolean(f, self.unlockedslimeoldspawn)
            self.__write_boolean(f, self.unlockedslimepurplespawn)
            self.__write_boolean(f, self.unlockedslimerainbowspawn)
            self.__write_boolean(f, self.unlockedslimeredspawn)
            self.__write_boolean(f, self.unlockedslimeyellowspawn)
            self.__write_boolean(f, self.unlockedslimecopperspawn)
        
        if self.version >= 264:
            self.__write_boolean(f, self.fastforwardtimetodusk)
            self.__write_uint8(f, self.moondialcooldown)
        
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
                while (remainingy > 0 and all(tile == self.tiles.tileinfos[x, nexty]) and int(tile[Channel.TILETYPE]) != 520 and int(tile[Channel.TILETYPE]) != 423):
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
                        self.__write_uint8(f, tiledata[idx])
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

        TYPE = int(tile[Channel.TILETYPE])
        ISACTIVE = (TYPE != -1)
        U = int(tile[Channel.FRAMEX])
        V = int(tile[Channel.FRAMEY])
        TILECOLOR = int(tile[Channel.TILECOLOR])
        FULLBRIGHTBLOCK = bool(tile[Channel.FULLBRIGHTBLOCK])
        WALL = int(tile[Channel.WALL])
        WALLCOLOR = int(tile[Channel.WALLCOLOR])
        FULLBRIGHTWALL = bool(tile[Channel.FULLBRIGHTWALL])
        LIQUIDAMOUNT = int(tile[Channel.LIQUIDAMOUNT])
        LIQUIDTYPE = int(tile[Channel.LIQUIDTYPE])
        WIRERED = bool(tile[Channel.WIRERED])
        WIREBLUE = bool(tile[Channel.WIREBLUE])
        WIREGREEN = bool(tile[Channel.WIREGREEN])
        BRICKSTYLE = int(tile[Channel.BRICKSTYLE])
        ACTUATER = bool(tile[Channel.ACTUACTOR])
        INACTIVE = bool(tile[Channel.INACTIVE])
        WIREYELLOW = bool(tile[Channel.WIREYELLOW])
        INVISIBLEBLOCK = bool(tile[Channel.INVISIBLEBLOCK])
        INVISIBLEWALL = bool(tile[Channel.INVISIBLEWALL])

        if ISACTIVE:
            header1 |= 0b0000_0010

            tiledata[dataindex] = TYPE%256
            dataindex += 1

            if tile[Channel.TILETYPE] > 255:
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
                if int(tile[Channel.TILECOLOR] != 0) and TILECOLOR != 31:
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

    def __SaveChests(self, f:io.BufferedWriter) -> int:
        count = len(self.chests)
        self.__write_int16(f, count)
        MAXITEMS = 40
        self.__write_int16(f, MAXITEMS)

        for chest in self.chests:
            self.__write_int32(f, chest.X)
            self.__write_int32(f, chest.Y)
            self.__write_string(f, chest.name)
            for slot in range(MAXITEMS):
                item:Item = chest.items[slot]
                stacksize = item.stacksize
                self.__write_int16(f, stacksize)

                if stacksize > 0:
                    item_id = item.netid
                    prefix = item.prefix
                    self.__write_int32(f, item_id)
                    self.__write_uint8(f, prefix)
        
        return f.tell()
    
    def __SaveSigns(self, f:io.BufferedWriter) -> int:
        count = len(self.signs)
        self.__write_int16(f, count)
        for sign in self.signs:
            text = sign.text
            x = sign.x
            y = sign.y
            self.__write_string(f, text)
            self.__write_int32(f, x)
            self.__write_int32(f, y)
        
        return f.tell()

    def __SaveTileEntity(self, f:io.BufferedWriter) -> int:
        count = len(self.tile_entities)
        self.__write_int32(f, count)
        for counter in range(count):
            entity = self.tile_entities[counter]
            entity_type = entity.type
            self.__write_uint8(f, entity_type)
            entity_id = entity.entity_id
            self.__write_int32(f, entity_id)
            posX = entity.posX
            self.__write_int16(f, posX)
            posY = entity.posY
            self.__write_int16(f, posY)
            attribute = entity.attribute

            if entity_type == TileEntityType.TrainingDummy:
                self.__write_int16(f, attribute["npc"])
            elif entity_type in [TileEntityType.ItemFrame,
                                 TileEntityType.WeaponRack,
                                 TileEntityType.FoodPlatter]:
                self.__SaveItem4TileEntity(f, attribute["item"])
            elif entity_type == TileEntityType.LogicSensor:
                self.__write_uint8(f, attribute["logiccheck"])
                self.__write_boolean(f, attribute["on"])
            elif entity_type == TileEntityType.DisplayDoll:
                item_bitmask = 0
                dye_bitmask = 0
                items:list[Item] = attribute["items"]
                dyes:list[Item] = attribute["dyes"]
                for idx in range(8):
                    if not items[idx].is_empty():
                        item_bitmask |= (1 << idx)
                for idx in range(8):
                    if not dyes[idx].is_empty():
                        dye_bitmask |= (1 << idx)
                self.__write_uint8(f, item_bitmask)
                self.__write_uint8(f, dye_bitmask)
                for idx in range(8):
                    if item_bitmask & (1 << idx):
                        self.__SaveItem4TileEntity(f, items[idx])
                for idx in range(8):
                    if dye_bitmask & (1 << idx):
                        self.__SaveItem4TileEntity(f, dyes[idx])
            elif entity_type == TileEntityType.HatRack:
                slots_bitmask = 0
                items:list[Item] = attribute["items"]
                dyes:list[Item] = attribute["dyes"]
                for idx in range(2):
                    if not items[idx].is_empty():
                        slots_bitmask |= (1 << idx)
                for idx in range(2):
                    if not dyes[idx].is_empty():
                        slots_bitmask |= (1 << (idx + 2))
                self.__write_uint8(f, slots_bitmask)
                for idx in range(2):
                    if slots_bitmask & (1 << idx):
                        self.__SaveItem4TileEntity(f, items[idx])
                for idx in range(2):
                    if slots_bitmask & (1 << (idx + 2)):
                        self.__SaveItem4TileEntity(f, dyes[idx])
            elif entity_type == TileEntityType.TeleportationPylon:
                pass
            else:
                raise WorldFileSaveError("Unknown TileEntity Type.")

        return f.tell()

    def __SaveItem4TileEntity(self, f:io.BufferedWriter, item:Item):
        self.__write_int16(f, item.netid)
        self.__write_uint8(f, item.prefix)
        self.__write_int16(f, item.stacksize)

    def __SavePressurePlate(self, f:io.BufferedWriter) -> int:
        count = len(self.pressure_plates)
        self.__write_int32(f, count)
        for plate in self.pressure_plates:
            self.__write_int32(f, plate.posX)
            self.__write_int32(f, plate.posY)
        
        return f.tell()

    def __SaveFooter(self, f:io.BufferedWriter):
        self.__write_boolean(f, True)
        self.__write_string(f, self.title)
        self.__write_int32(f, self.worldid)

    def __UpdateSectionPointers(self, f:io.BufferedWriter, sectionpointers:list[int]):
        f.seek(0)
        self.__write_int32(f, self.version)
        seeking_pos = 0x18 if self.version >= 140 else 0x04
        f.seek(seeking_pos)
        self.__write_int16(f, len(sectionpointers))
        for i in range(len(sectionpointers)):
            self.__write_int32(f, sectionpointers[i])