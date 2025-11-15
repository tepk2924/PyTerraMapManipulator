import struct
import io
import uuid
import datetime
import numpy as np
import sys
import os
import random
from IOutils import *
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
                 world_size:str | tuple = "large"):
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

    #TODO: SHOULE BE UPDATED UPON 1.4.5 ARRIVES
    def __initializetileframeimportant(self):
        '''
        This decides whether tile type is block or sprite.
        self.tileframeimportant[tiletype] == True means tile of #tiletype is sprite.
        THIS SHOULE BE UPDATED UPON 1.4.5 ARRIVES AS WELL
        '''
        self.tileframeimportant:list[bool] = [False, False, False, True, True, True, False, False, False, False, True, True, True, True, True, True, True, True, True, True, True, True, False, False, True, False, True, True, True, True, False, True, False, True, True, True, True, False, False, False, False, False, True, False, False, False, False, False, False, True, True, False, False, False, False, True, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, True, True, True, True, False, False, True, True, True, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, False, False, True, False, False, True, True, False, False, False, False, False, False, False, False, False, False, True, True, False, True, True, False, False, True, True, True, True, True, True, True, True, False, True, True, True, True, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, True, True, True, True, False, False, False, True, False, False, False, False, False, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, True, False, True, True, False, True, False, False, True, True, True, True, True, True, False, False, False, False, False, False, True, True, False, False, True, False, True, False, True, True, True, True, True, True, True, True, True, True, True, True, True, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True, False, False, False, True, True, True, True, True, True, True, True, True, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, False, False, True, False, True, True, True, True, True, False, False, True, True, False, False, False, False, False, False, False, False, False, True, True, False, True, True, True, False, False, False, False, False, False, False, False, False, True, False, False, False, False, True, True, True, False, True, True, True, True, True, True, True, False, False, False, False, False, False, False, True, True, True, True, True, True, True, False, True, False, False, False, False, False, True, True, True, True, True, True, True, True, True, True, False, False, False, False, False, False, False, False, False, True, True, False, False, False, True, True, True, True, True, False, False, False, False, True, True, False, False, True, True, True, False, True, True, True, False, False, False, False, False, True, True, True, True, True, True, True, True, True, True, True, False, False, False, False, False, False, True, True, True, True, True, True, False, False, False, True, True, True, True, True, True, True, True, True, True, True, False, False, False, True, True, False, False, False, True, False, False, False, True, True, True, True, True, True, True, True, False, True, True, False, False, True, False, True, False, False, False, False, False, True, True, False, False, True, True, True, False, False, False, False, False, False, True, True, True, True, True, True, True, True, True, True, False, True, True, True, True, True, False, False, False, False, True, False, False, False, True, True, True, True, False, True, True, True, True, True, True, True, True, True, True, False, True, True, True, False, False, False, True, True, False, True, True, True, True, True, True, True, False, False, False, False, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, True, True, True, True, True, True, False, False, False, False, True, True, True, True, False, True, False, False, True, False, True, True, False, True, True, True, True, True, True, True, True, True, True, True, True, True, False, True, True, True, False, True, False, False, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]

    def __initializeotherdata(self):
        self.NPCMobs_data = b'\x00\x00\x00\x00\x01%\x00\x00\x00\x00\x00\x97\xe3G\x00\xa0\x16F\x00s\x1c\x00\x00]\x02\x00\x00\x01\x00\x00\x00\x00\x00\x00'
        self.town_manager_data = b'\x00\x00\x00\x00'
        self.bestiary_data = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        self.creative_power_data = b'\x01\x00\x00\x00\x01\x08\x00\x00\x00\x00\x00\x01\t\x00\x00\x01\n\x00\x00\x01\x0c\x00\x00\x00\x00\x00\x01\r\x00\x00\x00'

    #TODO: SHOULE BE UPDATED UPON 1.4.5 ARRIVES
    def __HeaderFlags_init(self,
                           world_size:str):
        self.title:str = None
        self.seed:str = str(random.randint(0, (1 << 31) - 1)) #random
        self.worldgenversion:int = 1198295875585 #taken
        self.worldguid:uuid.UUID = uuid.uuid1()
        self.worldid:int = random.randint(0, (1 << 31) - 1) #random
        self.leftworld:float = 0.0 #always float 0.0?
        self.topworld:float = 0.0 #always float 0.0?
        if isinstance(world_size, str):
            world_size = world_size.lower()
            if world_size not in ["small", "medium", "large"]:
                print("World size unknown. Set to large.")
                world_size = "large"
            if world_size == "small":
                self.tileshigh:int = 1200
                self.tileswide:int = 4200
            elif world_size == "medium":
                self.tileshigh:int = 1800
                self.tileswide:int = 6400
            else: #large
                self.tileshigh:int = 2400
                self.tileswide:int = 8400
        elif isinstance(world_size, tuple):
            rows, cols = world_size
            self.tileshigh = rows
            self.tileswide = cols
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
        self.treeX:list[int] = [0, 0, 0]
        self.treeX0:int = self.treeX[0]
        self.treeX1:int = self.treeX[1]
        self.treeX2:int = self.treeX[2]
        self.treestyle0:int = 0
        self.treestyle1:int = 0
        self.treestyle2:int = 0
        self.treestyle3:int = 0
        self.cavebackX:list[int] = [0, 0, 0]
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
        self.spawnX = self.tileswide//2
        self.spawnY = self.tileshigh//6
        self.groundlevel = float(self.tileshigh/4)
        self.rocklevel = float(self.tileshigh/3)
        self.time:float = 27000.0
        self.daytime:bool = False
        self.moonphase:int = 0
        self.bloodmoon:bool = False
        self.iseclipse:bool = False
        self.dungeonX:int = 0
        self.dungeonY:int = 0
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

    #TODO: maybe this should be updated upon 1.4.5?
    def __getsectioncount(self):
        return 11 if self.version >= 220 else 10

    #TODO: maybe this should be updated upon 1.4.5?
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
            self.version = read_uint32(f)

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

    #TODO: maybe this should be updated upon 1.4.5?
    def __LoadSectionHeader(self, f:io.BufferedReader):
        #loading section header
        if self.version >= 140:
            tmp = f.tell()
            self.ischinese = (f.read(1).decode('ascii') == 'x')
            f.seek(tmp)
            headerformat = f.read(7).decode('ascii')
            filetype = f.read(1)
            self.filerevision = read_uint32(f)
            flags = read_uint64(f)
            self.isfavorite = ((flags & 1) == 1)
        sectioncount = read_int16(f)
        section_ptrs = []
        for _ in range(sectioncount):
            section_ptrs.append(read_int32(f))
        
        tileframeimportant = self.__ReadBitArray(f)
        return tileframeimportant, section_ptrs
    
    def __ReadBitArray(self, f:io.BufferedReader):
        #read bit array
        bitarraylength = read_int16(f)
        data = 0
        bitmask = 128
        booleans = [False]*bitarraylength
        for idx in range(bitarraylength):
            if bitmask != 128:
                bitmask = bitmask << 1
            else:
                data = read_uint8(f)
                bitmask = 1
            if data & bitmask == bitmask:
                booleans[idx] = True
        return booleans
    
    #TODO: SHOULE BE UPDATED UPON 1.4.5 ARRIVES
    def __LoadHeaderFlags(self, f:io.BufferedReader):
        self.title = read_string(f)

        if self.version >= 179:
            if self.version == 179:
                #TODO: ???
                self.seed = str(read_int32(f))
            else:
                self.seed = read_string(f)
            self.worldgenversion = read_uint64(f)
        else:
            self.seed = ""
        if self.version >= 181:
            self.worldguid = uuid.UUID(bytes_le=f.read(16))
        else:
            self.worldguid = uuid.uuid1()

        self.worldid = read_int32(f)
        self.leftworld = float(read_int32(f))
        self.rightworld = float(read_int32(f))
        self.topworld = float(read_int32(f))
        self.bottomworld = float(read_int32(f))
        self.tileshigh = read_int32(f)
        self.tileswide = read_int32(f)

        if self.version >= 209:
            self.gamemode = read_int32(f)

            if self.version >= 222: self.drunkworld = read_boolean(f)
            if self.version >= 227: self.goodworld = read_boolean(f)
            if self.version >= 238: self.tenthanniversaryworld = read_boolean(f)
            if self.version >= 239: self.dontstarveworld = read_boolean(f)
            if self.version >= 241: self.notthebeesworld = read_boolean(f)
            if self.version >= 249: self.remixworld = read_boolean(f)
            if self.version >= 266: self.notrapworld = read_boolean(f)
            self.zenithworld = (self.remixworld and self.drunkworld) if self.version < 267 else read_boolean(f)
        elif self.version == 208:
            self.gamemode = 2 if read_boolean(f) else 0
        elif self.version == 112:
            self.gamemode = 1 if read_boolean(f) else 0
        else:
            self.gamemode = 0

        self.creationtime = read_int64(f) if self.version >= 141 else int(datetime.datetime.now().timestamp())

        self.moontype = read_uint8(f)
        self.treeX[0] = read_int32(f)
        self.treeX[1] = read_int32(f)
        self.treeX[2] = read_int32(f)
        self.treeX0 = self.treeX[0]
        self.treeX1 = self.treeX[1]
        self.treeX2 = self.treeX[2]
        self.treestyle0 = read_int32(f)
        self.treestyle1 = read_int32(f)
        self.treestyle2 = read_int32(f)
        self.treestyle3 = read_int32(f)
        self.cavebackX[0] = read_int32(f)
        self.cavebackX[1] = read_int32(f)
        self.cavebackX[2] = read_int32(f)
        self.cavebackX0 = self.cavebackX[0]
        self.cavebackX1 = self.cavebackX[1]
        self.cavebackX2 = self.cavebackX[2]
        self.cavebackstyle0 = read_int32(f)
        self.cavebackstyle1 = read_int32(f)
        self.cavebackstyle2 = read_int32(f)
        self.cavebackstyle3 = read_int32(f)
        self.icebackstyle = read_int32(f)
        self.junglebackstyle = read_int32(f)
        self.hellbackstyle = read_int32(f)

        self.spawnX = read_int32(f)
        self.spawnY = read_int32(f)
        self.groundlevel = read_double(f)
        self.rocklevel = read_double(f)
        self.time = read_double(f)
        self.daytime = read_boolean(f)
        self.moonphase = read_int32(f)
        self.bloodmoon = read_boolean(f)
        self.iseclipse = read_boolean(f)
        self.dungeonX = read_int32(f)
        self.dungeonY = read_int32(f)

        self.iscrimson = read_boolean(f)

        self.downedboss1eyeofcthulhu = read_boolean(f)
        self.downedboss2eaterofworlds = read_boolean(f)
        self.downedboss3skeletron = read_boolean(f)
        self.downedqueenbee = read_boolean(f)
        self.downedmechboss1thedestroyer = read_boolean(f)
        self.downedmechboss2thetwins = read_boolean(f)
        self.downedmechboss3skeletronprime = read_boolean(f)
        self.downedmechbossany = read_boolean(f)
        self.downedplantboss = read_boolean(f)
        self.downedgolemboss = read_boolean(f)

        if self.version >= 118: self.downedslimekingboss = read_boolean(f)

        self.savedgoblin = read_boolean(f)
        self.savedwizard = read_boolean(f)
        self.savedmech = read_boolean(f)
        self.downedgoblins = read_boolean(f)
        self.downedclown = read_boolean(f)
        self.downedfrost = read_boolean(f)
        self.downedpirates = read_boolean(f)

        self.shadoworbsmashed = read_boolean(f)
        self.spawnmeteor = read_boolean(f)
        self.shadoworbcount = read_uint8(f)
        self.altarcount = read_int32(f)
        self.hardmode = read_boolean(f)
        if self.version >= 257: self.partyofdoom = read_boolean(f)
        self.invasiondelay = read_int32(f)
        self.invasionsize = read_int32(f)
        self.invasiontype = read_int32(f)
        self.invasionX = read_double(f)
        if self.version >= 118: self.slimeraintime = read_double(f)
        if self.version >= 113: self.sundialcooldown = read_uint8(f)
        
        self.israining = read_boolean(f)
        self.tempraintime = read_int32(f)
        self.tempmaxrain = read_single(f)
        self.savedoretierscobalt = read_int32(f)
        self.savedoretiersmythril = read_int32(f)
        self.savedoretiersadamantitie = read_int32(f)
        self.bgtree = read_uint8(f)
        self.bgcorruption = read_uint8(f)
        self.bgjungle = read_uint8(f)
        self.bgsnow = read_uint8(f)
        self.bghallow = read_uint8(f)
        self.bgcrimson = read_uint8(f)
        self.bgdesert = read_uint8(f)
        self.bgocean = read_uint8(f)
        self.cloudbgactive = float(read_int32(f))
        self.numclouds = read_int16(f)
        self.windspeedset = read_single(f)
        
        if self.version < 95: return

        for _ in range(read_int32(f)):
            self.anglers.append(read_string(f))
        
        if self.version < 99: return

        self.savedangler = read_boolean(f)

        if self.version < 101: return

        self.anglerquest = read_int32(f)

        if self.version < 104: return

        self.savedstylist = read_boolean(f)

        if self.version >= 140:
            self.savedtaxcollector = read_boolean(f)
        if self.version >= 201:
            self.savedgolfer = read_boolean(f)
        if self.version >= 107:
            self.invasionsizestart = read_int32(f)
        self.cultistdelay = read_int32(f) if self.version >= 108 else 86400

        if self.version < 109: return

        self.killedmobs.clear()
        number_of_mobs = read_int16(f)
        for _ in range(number_of_mobs):
            self.killedmobs.append(read_int32(f))
        
        if self.version < 128: return

        if self.version >= 140:
            self.fastforwardtime = read_boolean(f)
        
        if self.version < 131: return

        self.downedfishron = read_boolean(f)
        
        if self.version >= 140:
            self.downedmartians = read_boolean(f)
            self.downedlunaticcultist = read_boolean(f)
            self.downedmoonlord = read_boolean(f)
        
        self.downedhalloweenking = read_boolean(f)
        self.downedhalloweentree = read_boolean(f)
        self.downedchristmasqueen = read_boolean(f)
        self.downedsanta = read_boolean(f)
        self.downedchristmastree = read_boolean(f)

        if self.version < 140: return

        self.downedcelestialsolar = read_boolean(f)
        self.downedcelestialvortex = read_boolean(f)
        self.downedcelestialnebula = read_boolean(f)
        self.downedcelestialstardust = read_boolean(f)
        self.celestialsolaractive = read_boolean(f)
        self.celestialvortexactive = read_boolean(f)
        self.celestialnebulaactive = read_boolean(f)
        self.celestialstardustactive = read_boolean(f)
        self.apocalypse = read_boolean(f)

        if self.version >= 170:
            self.partymanual = read_boolean(f)
            self.partygenuine = read_boolean(f)
            self.partycooldown = read_int32(f)
            numparty = read_int32(f)
            for _ in range(numparty):
                self.partyingnpcs.append(read_int32(f))
        
        if self.version >= 174:
            self.sandstormhappening = read_boolean(f)
            self.sandstormtimeleft = read_int32(f)
            self.sandstormseverity = read_single(f)
            self.sandstormintendedseverity = read_single(f)
        
        if self.version >= 178:
            self.savedbartender = read_boolean(f)
            self.downeddd2invasiont1 = read_boolean(f)
            self.downeddd2invasiont2 = read_boolean(f)
            self.downeddd2invasiont3 = read_boolean(f)
        
        if self.version > 194:
            self.mushroombg = read_uint8(f)
        
        if self.version >= 215:
            self.underworldbg = read_uint8(f)
        
        if self.version >= 195:
            self.bgtree2 = read_uint8(f)
            self.bgtree3 = read_uint8(f)
            self.bgtree4 = read_uint8(f)
        else:
            self.bgtree2 = self.bgtree
            self.bgtree3 = self.bgtree
            self.bgtree4 = self.bgtree

        if self.version >= 204:
            self.combatbookused = read_boolean(f)
        
        if self.version >= 207:
            self.lanternnightcooldown = read_int32(f)
            self.lanternnightgenuine = read_boolean(f)
            self.lanternnightmanual = read_boolean(f)
            self.lanternnightnextnightisgenuine = read_boolean(f)
        
        if self.version >= 211:
            numtrees = read_int32(f)
            self.treetopvariations = [0]*max([13, numtrees])
            for i in range(numtrees):
                self.treetopvariations[i] = read_int32(f)
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
            self.forcehalloweenfortoday = read_boolean(f)
            self.forcexmasfortoday = read_boolean(f)
        
        if self.version >= 216:
            self.savedoretierscopper = read_int32(f)
            self.savedoretiersiron = read_int32(f)
            self.savedoretierssilver = read_int32(f)
            self.savedoretiersgold = read_int32(f)
        else:
            self.savedoretierscopper = -1
            self.savedoretiersiron = -1
            self.savedoretierssilver = -1
            self.savedoretiersgold = -1
        
        if self.version >= 217:
            self.boughtcat = read_boolean(f)
            self.boughtdog = read_boolean(f)
            self.boughtbunny = read_boolean(f)
        
        if self.version >= 223:
            self.downedempressoflight = read_boolean(f)
            self.downedqueenslime = read_boolean(f)
        
        if self.version >= 240:
            self.downeddeerclops = read_boolean(f)
        
        if self.version >= 250:
            self.unlockedslimebluespawn = read_boolean(f)
        
        if self.version >= 251:
            self.unlockedmerchantspawn = read_boolean(f)
            self.unlockeddemolitionistspawn = read_boolean(f)
            self.unlockedpartygirlspawn = read_boolean(f)
            self.unlockeddyetraderspawn = read_boolean(f)
            self.unlockedtrufflespawn = read_boolean(f)
            self.unlockedarmsdealerspawn = read_boolean(f)
            self.unlockednursespawn = read_boolean(f)
            self.unlockedprincessspawn = read_boolean(f)
        
        if self.version >= 259:
            self.combatbookvolumetwowasused = read_boolean(f)
        
        if self.version >= 260:
            self.peddlerssatchelwasused = read_boolean(f)
        
        if self.version >= 261:
            self.unlockedslimegreenspawn = read_boolean(f)
            self.unlockedslimeoldspawn = read_boolean(f)
            self.unlockedslimepurplespawn = read_boolean(f)
            self.unlockedslimerainbowspawn = read_boolean(f)
            self.unlockedslimeredspawn = read_boolean(f)
            self.unlockedslimeyellowspawn = read_boolean(f)
            self.unlockedslimecopperspawn = read_boolean(f)
        
        if self.version >= 264:
            self.fastforwardtimetodusk = read_boolean(f)
            self.moondialcooldown = read_uint8(f)
        
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

    #TODO: maybe this should be updated upon 1.4.5?
    def __deserializetiledata(self, f, tileframeimportant, version) -> tuple[list, int]:
        single_tile = [0]*19
        tiletype = -1
        header4 = 0
        header3 = 0
        header2 = 0
        header1 = read_uint8(f)

        hasheader2 = False
        hasheader3 = False
        hasheader4 = False

        if header1 & 0b0000_0001:
            hasheader2 = True
            header2 = read_uint8(f)
        
        if hasheader2 and (header2 & 0b0000_0001):
            hasheader3 = True
            header3 = read_uint8(f)
        
        if version >= 269:
            if hasheader3 and (header3 & 0b0000_0001):
                hasheader4 = True
                header4 = read_uint8(f)
        
        isactive:bool = (header1 & 0b0000_0010) == 0b0000_0010

        if isactive:
            if not (header1 & 0b0010_0000):
                tiletype = read_uint8(f)
            else:
                lowerbyte = read_uint8(f)
                tiletype = read_uint8(f)
                tiletype = (tiletype << 8) | lowerbyte
            single_tile[Channel.TILETYPE] = tiletype

            if not tileframeimportant[tiletype]:
                single_tile[Channel.FRAMEX] = 0
                single_tile[Channel.FRAMEY] = 0
            else:
                single_tile[Channel.FRAMEX] = read_int16(f)
                single_tile[Channel.FRAMEY] = read_int16(f)

                if single_tile[Channel.TILETYPE] == 144: #reset timers
                    single_tile[Channel.FRAMEY] = 0
            
            if header3 & 0b0000_1000:
                single_tile[Channel.TILECOLOR] = read_uint8(f)
        else:
            single_tile[Channel.TILETYPE] = -1


        if header1 & 0b0000_0100:
            single_tile[Channel.WALL] = read_uint8(f)
            if ((header3 & 0b0001_0000) == 0b0001_0000):
                single_tile[Channel.WALLCOLOR] = read_uint8(f)
        
        liquidtype = (header1 & 0b0001_1000) >> 3
        if liquidtype != 0:
            single_tile[Channel.LIQUIDAMOUNT] = read_uint8(f)
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
                    single_tile[Channel.WALL] = (read_uint8(f) << 8) | single_tile[Channel.WALL]
        
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
            rle = read_uint8(f)
        else:
            rle = read_int16(f)
        
        return single_tile, rle

    def __LoadChestData(self, f, chest_verbose) -> list[Chest]:
        total_chests = read_int16(f)
        max_items = read_int16(f)
        CHEST_MAX = 40

        if max_items > CHEST_MAX:
            items_per_chest = CHEST_MAX
            overflowitems = max_items - CHEST_MAX
        else:
            items_per_chest = max_items
            overflowitems = 0

        chests = []

        for i in range(total_chests):
            X = read_int32(f)
            Y = read_int32(f)
            name = read_string(f)
            chest = Chest(X, Y, name)

            for slot in range(items_per_chest):
                stacksize = read_int16(f)
                chest.items[slot].stacksize = stacksize

                if stacksize > 0:
                    item_id = read_int32(f)
                    prefix = read_uint8(f)

                    chest.items[slot].netid = item_id
                    chest.items[slot].stacksize = stacksize
                    chest.items[slot].prefix = prefix
        
            for overflow in range(overflowitems):
                stacksize = read_int16(f)
                if stacksize > 0:
                    read_int32(f)
                    read_uint8(f)
            
            chests.append(chest)
        
        if chest_verbose:
            for chest in chests:
                print(chest)

        return chests

    def __LoadSignData(self, f, sign_verbose) -> list[Sign]:
        totalsigns = read_int16(f)

        signs = []

        for i in range(totalsigns):
            text = read_string(f)
            x = read_int32(f)
            y = read_int32(f)
            sign = Sign(text, x, y)

            signs.append(sign)
        
        if sign_verbose:
            for sign in signs:
                print(sign)        

        return signs

    def __LoadTileEntity(self, f:io.BufferedReader) -> list[TileEntity]:
        count = read_int32(f)
        ret = []
        for counter in range(count):
            entity_type = read_uint8(f)
            entity_id = read_int32(f)
            posX = read_int16(f)
            posY = read_int16(f)
            entity = TileEntity(type=entity_type,
                                entity_id=entity_id,
                                posX=posX,
                                posY=posY)
            
            if entity_type == TileEntityType.TrainingDummy:
                entity.attribute["npc"] = read_int16(f)
            elif entity_type in [TileEntityType.ItemFrame,
                                 TileEntityType.WeaponRack,
                                 TileEntityType.FoodPlatter]:
                entity.attribute["item"] = self.__LoadItem4TileEntity(f)
            elif entity_type == TileEntityType.LogicSensor:
                entity.attribute["logiccheck"] = read_uint8(f)
                entity.attribute["on"] = read_boolean(f)
            elif entity_type == TileEntityType.DisplayDoll:
                item_bitmask = read_uint8(f)
                dye_bitmask = read_uint8(f)
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
                slots_bitmask = read_uint8(f)
                items:list[Item] = [Item() for _ in range(2)]
                dyes:list[Item] = [Item() for _ in range(2)]
                for idx in range(2):
                    if slots_bitmask & (1 << idx):
                        items[idx] = self.__LoadItem4TileEntity(f)
                for idx in range(2):
                    if slots_bitmask & (1 << (idx + 2)):
                        dyes[idx] = self.__LoadItem4TileEntity(f)
                entity.attribute["items"] = items
                entity.attribute["dyes"] = dyes
            elif entity_type == TileEntityType.TeleportationPylon:
                pass
            else:
                raise WorldFileFormatException("Unknown TileEntity Type.")
            ret.append(entity)
        return ret

    def __LoadItem4TileEntity(self, f) -> Item:
        netid = read_int16(f)
        prefix = read_uint8(f)
        stacksize = read_int16(f)
        return Item(netid=netid, prefix=prefix, stacksize=stacksize)

    def __LoadPressurePlate(self, f) -> list[PressurePlate]:
        count = read_int32(f)
        ret = []
        for counter in range(count):
            posX = read_int32(f)
            posY = read_int32(f)
            ret.append(PressurePlate(posX, posY))
        return ret

    def __LoadFooter(self, f):
        boolean_footer = read_boolean(f)
        # print(f"{boolean_footer = }")
        if not boolean_footer:
            raise WorldFileFormatException("Invalid Boolean Footer")
        
        title_footer = read_string(f)
        # print(f"{title_footer = }")
        if title_footer != self.title:
            raise WorldFileFormatException("Invalid World Title Footer")
        
        world_id_footer = read_int32(f)
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
        self.tiles.enter_editmode()
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

    def place_item_frame(self,
                         row:int,
                         col:int,
                         item:Item):
        self.place_sprite(row, col, TileID.ItemFrame, 2, 2)
        item_frame_entity = TileEntity(type=TileEntityType.ItemFrame,
                                       entity_id=len(self.tile_entities),
                                       posX=col,
                                       posY=row)
        item_frame_entity.attribute["item"] = item
        self.tile_entities.append(item_frame_entity)

    #TODO: maybe this should be updated upon 1.4.5?
    def save_world(self,
                   save_file_path:str=None):
        if save_file_path is None:
            save_file_path = input("Saving File Path : ")
        if not save_file_path.endswith(".wld"):
            save_file_path = save_file_path + ".wld"

        if self.title is None:
            self.title = os.path.splitext(os.path.basename(save_file_path))[0]

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

    #TODO: maybe this should be updated upon 1.4.5?
    def __SaveSectionHeader(self, f:io.BufferedWriter, tileframeimportant) -> int:
        write_uint32(f, self.version)

        if self.version >= 140:
            if self.ischinese:
                f.write('xindong'.encode('ascii'))
            else:
                f.write('relogic'.encode('ascii'))
            
            write_uint8(f, 2)

            write_uint32(f, self.filerevision)

            worldheaderflags = 0
            if self.isfavorite:
                worldheaderflags |= 1
            write_uint64(f, worldheaderflags)

        sectioncount = self.__getsectioncount()
        write_int16(f, sectioncount)

        for _ in range(sectioncount):
            write_int32(f, 0)
        
        self.__WriteBitArray(f, tileframeimportant)
        return f.tell()
    
    def __WriteBitArray(self, f, tileframeimportant):
        write_int16(f, len(tileframeimportant))

        data = 0
        bitmask = 1
        for i in range(len(tileframeimportant)):
            if tileframeimportant[i]:
                data = data | bitmask
            if bitmask != 128:
                bitmask = bitmask << 1
            else:
                write_uint8(f, data)
                data = 0
                bitmask = 1
        
        if bitmask != 1:
            write_uint8(f, data)
    
    #TODO: SHOULE BE UPDATED UPON 1.4.5 ARRIVES
    def __SaveHeaderFlags(self, f:io.BufferedWriter) -> int:
        write_string(f, self.title)

        if self.version >= 179:
            if self.version == 179:
                seed = int(self.seed)
                write_int32(f, seed)
            else:
                seed = int(self.seed)
                write_string(f, str(seed))
            write_uint64(f, self.worldgenversion)
        
        if self.version >= 181:
            f.write(self.worldguid.bytes)
        
        write_int32(f, self.worldid)
        write_int32(f, int(self.leftworld))
        write_int32(f, int(self.rightworld))
        write_int32(f, int(self.topworld))
        write_int32(f, int(self.bottomworld))
        write_int32(f, self.tileshigh)
        write_int32(f, self.tileswide)

        if self.version >= 209:
            write_int32(f, self.gamemode)
            
            if self.version >= 222: write_boolean(f, self.drunkworld)
            if self.version >= 227: write_boolean(f, self.goodworld)
            if self.version >= 238: write_boolean(f, self.tenthanniversaryworld)
            if self.version >= 239: write_boolean(f, self.dontstarveworld)
            if self.version >= 241: write_boolean(f, self.notthebeesworld)
            if self.version >= 249: write_boolean(f, self.remixworld)
            if self.version >= 266: write_boolean(f, self.notrapworld)
            if self.version >= 266: write_boolean(f, self.zenithworld)
        elif self.version == 208:
            write_boolean(f, self.gamemode == 2)
        elif self.version == 112:
            write_boolean(f, self.gamemode == 1)
        else:
            pass

        if self.version >= 141:
            write_int64(f, self.creationtime)
        
        write_uint8(f, self.moontype)
        write_int32(f, self.treeX0)
        write_int32(f, self.treeX1)
        write_int32(f, self.treeX2)
        write_int32(f, self.treestyle0)
        write_int32(f, self.treestyle1)
        write_int32(f, self.treestyle2)
        write_int32(f, self.treestyle3)
        write_int32(f, self.cavebackX0)
        write_int32(f, self.cavebackX1)
        write_int32(f, self.cavebackX2)
        write_int32(f, self.cavebackstyle0)
        write_int32(f, self.cavebackstyle1)
        write_int32(f, self.cavebackstyle2)
        write_int32(f, self.cavebackstyle3)
        write_int32(f, self.icebackstyle)
        write_int32(f, self.junglebackstyle)
        write_int32(f, self.hellbackstyle)

        write_int32(f, self.spawnX)
        write_int32(f, self.spawnY)
        write_double(f, self.groundlevel)
        write_double(f, self.rocklevel)
        write_double(f, self.time)
        write_boolean(f, self.daytime)
        write_int32(f, self.moonphase)
        write_boolean(f, self.bloodmoon)
        write_boolean(f, self.iseclipse)
        write_int32(f, self.dungeonX)
        write_int32(f, self.dungeonY)

        write_boolean(f, self.iscrimson)

        write_boolean(f, self.downedboss1eyeofcthulhu)
        write_boolean(f, self.downedboss2eaterofworlds)
        write_boolean(f, self.downedboss3skeletron)
        write_boolean(f, self.downedqueenbee)
        write_boolean(f, self.downedmechboss1thedestroyer)
        write_boolean(f, self.downedmechboss2thetwins)
        write_boolean(f, self.downedmechboss3skeletronprime)
        write_boolean(f, self.downedmechbossany)
        write_boolean(f, self.downedplantboss)
        write_boolean(f, self.downedgolemboss)

        if self.version >= 118: write_boolean(f, self.downedslimekingboss)

        write_boolean(f, self.savedgoblin)
        write_boolean(f, self.savedwizard)
        write_boolean(f, self.savedmech)
        write_boolean(f, self.downedgoblins)
        write_boolean(f, self.downedclown)
        write_boolean(f, self.downedfrost)
        write_boolean(f, self.downedpirates)

        write_boolean(f, self.shadoworbsmashed)
        write_boolean(f, self.spawnmeteor)
        write_uint8(f, self.shadoworbcount)
        write_int32(f, self.altarcount)
        write_boolean(f, self.hardmode)
        if self.version >= 257: write_boolean(f, self.partyofdoom)
        write_int32(f, self.invasiondelay)
        write_int32(f, self.invasionsize)
        write_int32(f, self.invasiontype)
        write_double(f, self.invasionX)
        if self.version >= 118: write_double(f, self.slimeraintime)
        if self.version >= 113: write_uint8(f, self.sundialcooldown)

        write_boolean(f, self.israining)
        write_int32(f, self.tempraintime)
        write_single(f, self.tempmaxrain)
        write_int32(f, self.savedoretierscobalt)
        write_int32(f, self.savedoretiersmythril)
        write_int32(f, self.savedoretiersadamantitie)
        write_uint8(f, self.bgtree)
        write_uint8(f, self.bgcorruption)
        write_uint8(f, self.bgjungle)
        write_uint8(f, self.bgsnow)
        write_uint8(f, self.bghallow)
        write_uint8(f, self.bgcrimson)
        write_uint8(f, self.bgdesert)
        write_uint8(f, self.bgocean)
        write_int32(f, int(self.cloudbgactive))
        write_int16(f, self.numclouds)
        write_single(f, self.windspeedset)

        if self.version < 95: return f.tell()

        write_int32(f, len(self.anglers))

        for angler in self.anglers:
            write_string(f, angler)
        
        if self.version < 99: return f.tell()

        write_boolean(f, self.savedangler)

        if self.version < 101: return f.tell()

        write_int32(f, self.anglerquest)

        if self.version < 104: return f.tell()

        write_boolean(f, self.savedstylist)

        if self.version >= 129:
            write_boolean(f, self.savedtaxcollector)
        if self.version >= 201:
            write_boolean(f, self.savedgolfer)
        if self.version >= 107:
            write_int32(f, self.invasionsizestart)
        if self.version >= 108:
            write_int32(f, self.cultistdelay)
        
        if self.version < 109: return f.tell()

        number_of_mobs = len(self.killedmobs)
        write_int16(f, number_of_mobs)
        for i in range(number_of_mobs):
            write_int32(f, self.killedmobs[i])
        
        if self.version < 128: return f.tell()

        if self.version >= 140:
            write_boolean(f, self.fastforwardtime)
        
        if self.version < 131: return f.tell()

        write_boolean(f, self.downedfishron)

        if self.version >= 140:
            write_boolean(f, self.downedmartians)
            write_boolean(f, self.downedlunaticcultist)
            write_boolean(f, self.downedmoonlord)

        write_boolean(f, self.downedhalloweenking)
        write_boolean(f, self.downedhalloweentree)
        write_boolean(f, self.downedchristmasqueen)
        write_boolean(f, self.downedsanta)
        write_boolean(f, self.downedchristmastree)

        if self.version < 140: return f.tell()

        write_boolean(f, self.downedcelestialsolar)
        write_boolean(f, self.downedcelestialvortex)
        write_boolean(f, self.downedcelestialnebula)
        write_boolean(f, self.downedcelestialstardust)
        write_boolean(f, self.celestialsolaractive)
        write_boolean(f, self.celestialvortexactive)
        write_boolean(f, self.celestialnebulaactive)
        write_boolean(f, self.celestialstardustactive)
        write_boolean(f, self.apocalypse)

        if self.version >= 170:
            write_boolean(f, self.partymanual)
            write_boolean(f, self.partygenuine)
            write_int32(f, self.partycooldown)
            numparty = len(self.partyingnpcs)
            write_int32(f, numparty)
            for i in range(numparty):
                write_int32(f, numparty[i])
        
        if self.version >= 174:
            write_boolean(f, self.sandstormhappening)
            write_int32(f, self.sandstormtimeleft)
            write_single(f, self.sandstormseverity)
            write_single(f, self.sandstormintendedseverity)

        if self.version >= 178:
            write_boolean(f, self.savedbartender)
            write_boolean(f, self.downeddd2invasiont1)
            write_boolean(f, self.downeddd2invasiont2)
            write_boolean(f, self.downeddd2invasiont3)

        if self.version > 194:
            write_uint8(f, self.mushroombg)

        if self.version >= 215:
            write_uint8(f, self.underworldbg)
        
        if self.version >= 195:
            write_uint8(f, self.bgtree2)
            write_uint8(f, self.bgtree3)
            write_uint8(f, self.bgtree4)

        if self.version >= 204:
            write_boolean(f, self.combatbookused)
        
        if self.version >= 207:
            write_int32(f, self.lanternnightcooldown)
            write_boolean(f, self.lanternnightgenuine)
            write_boolean(f, self.lanternnightmanual)
            write_boolean(f, self.lanternnightnextnightisgenuine)

        if self.version >= 211:
            numtrees = len(self.treetopvariations)
            write_int32(f, numtrees)
            for i in range(numtrees):
                write_int32(f, self.treetopvariations[i])

        if self.version >= 212:
            write_boolean(f, self.forcehalloweenfortoday)
            write_boolean(f, self.forcexmasfortoday)

        if self.version >= 216:
            write_int32(f, self.savedoretierscopper)
            write_int32(f, self.savedoretiersiron)
            write_int32(f, self.savedoretierssilver)
            write_int32(f, self.savedoretiersgold)
        
        if self.version >= 217:
            write_boolean(f, self.boughtcat)
            write_boolean(f, self.boughtdog)
            write_boolean(f, self.boughtbunny)

        if self.version >= 223:
            write_boolean(f, self.downedempressoflight)
            write_boolean(f, self.downedqueenslime)
        
        if self.version >= 240:
            write_boolean(f, self.downeddeerclops)
        
        if self.version >= 250:
            write_boolean(f, self.unlockedslimebluespawn)
        
        if self.version >= 251:
            write_boolean(f, self.unlockedmerchantspawn)
            write_boolean(f, self.unlockeddemolitionistspawn)
            write_boolean(f, self.unlockedpartygirlspawn)
            write_boolean(f, self.unlockeddyetraderspawn)
            write_boolean(f, self.unlockedtrufflespawn)
            write_boolean(f, self.unlockedarmsdealerspawn)
            write_boolean(f, self.unlockednursespawn)
            write_boolean(f, self.unlockedprincessspawn)
        
        if self.version >= 259:
            write_boolean(f, self.combatbookvolumetwowasused)
        
        if self.version >= 260:
            write_boolean(f, self.peddlerssatchelwasused)
        
        if self.version >= 261:
            write_boolean(f, self.unlockedslimegreenspawn)
            write_boolean(f, self.unlockedslimeoldspawn)
            write_boolean(f, self.unlockedslimepurplespawn)
            write_boolean(f, self.unlockedslimerainbowspawn)
            write_boolean(f, self.unlockedslimeredspawn)
            write_boolean(f, self.unlockedslimeyellowspawn)
            write_boolean(f, self.unlockedslimecopperspawn)
        
        if self.version >= 264:
            write_boolean(f, self.fastforwardtimetodusk)
            write_uint8(f, self.moondialcooldown)
        
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
                        write_uint8(f, tiledata[idx])
                except struct.error:
                    print(tiledata)
                    exit(1)
                y += 1
        sys.stdout.write(f'\x1b[{backspace}D')
        sys.stdout.write(f"saving tile {total_tiles}/{total_tiles} done... [{"="*barlen}]\n")
        return f.tell()
    
    #TODO: maybe this should be updated upon 1.4.5?
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
        write_int16(f, count)
        MAXITEMS = 40
        write_int16(f, MAXITEMS)

        for chest in self.chests:
            write_int32(f, chest.X)
            write_int32(f, chest.Y)
            write_string(f, chest.name)
            for slot in range(MAXITEMS):
                item:Item = chest.items[slot]
                stacksize = item.stacksize
                write_int16(f, stacksize)

                if stacksize > 0:
                    item_id = item.netid
                    prefix = item.prefix
                    write_int32(f, item_id)
                    write_uint8(f, prefix)
        
        return f.tell()
    
    def __SaveSigns(self, f:io.BufferedWriter) -> int:
        count = len(self.signs)
        write_int16(f, count)
        for sign in self.signs:
            text = sign.text
            x = sign.x
            y = sign.y
            write_string(f, text)
            write_int32(f, x)
            write_int32(f, y)
        
        return f.tell()

    def __SaveTileEntity(self, f:io.BufferedWriter) -> int:
        count = len(self.tile_entities)
        write_int32(f, count)
        for counter in range(count):
            entity = self.tile_entities[counter]
            entity_type = entity.type
            write_uint8(f, entity_type)
            entity_id = entity.entity_id
            write_int32(f, entity_id)
            posX = entity.posX
            write_int16(f, posX)
            posY = entity.posY
            write_int16(f, posY)
            attribute = entity.attribute

            if entity_type == TileEntityType.TrainingDummy:
                write_int16(f, attribute["npc"])
            elif entity_type in [TileEntityType.ItemFrame,
                                 TileEntityType.WeaponRack,
                                 TileEntityType.FoodPlatter]:
                self.__SaveItem4TileEntity(f, attribute["item"])
            elif entity_type == TileEntityType.LogicSensor:
                write_uint8(f, attribute["logiccheck"])
                write_boolean(f, attribute["on"])
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
                write_uint8(f, item_bitmask)
                write_uint8(f, dye_bitmask)
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
                write_uint8(f, slots_bitmask)
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
        write_int16(f, item.netid)
        write_uint8(f, item.prefix)
        write_int16(f, item.stacksize)

    def __SavePressurePlate(self, f:io.BufferedWriter) -> int:
        count = len(self.pressure_plates)
        write_int32(f, count)
        for plate in self.pressure_plates:
            write_int32(f, plate.posX)
            write_int32(f, plate.posY)
        
        return f.tell()

    def __SaveFooter(self, f:io.BufferedWriter):
        write_boolean(f, True)
        write_string(f, self.title)
        write_int32(f, self.worldid)

    def __UpdateSectionPointers(self, f:io.BufferedWriter, sectionpointers:list[int]):
        f.seek(0)
        write_int32(f, self.version)
        seeking_pos = 0x18 if self.version >= 140 else 0x04
        f.seek(seeking_pos)
        write_int16(f, len(sectionpointers))
        for i in range(len(sectionpointers)):
            write_int32(f, sectionpointers[i])