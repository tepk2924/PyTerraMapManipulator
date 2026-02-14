import uuid
import random

import load_util
import save_util
from tiles import Tiles
from chest import Chest, Item
from sign import Sign
from pressureplate import PressurePlate
from tileentity import TileEntity
from enumeration import BrickStyle, Liquid, Channel, GameMode, TileID, TileEntityType, ItemID

class TerrariaWorld:
    #At least making these works for 1.4.5.....
    def __init__(self,
                 world_size:str | tuple = "large"):
        '''
        world_size(optional, default = "large"):
            str: "small"(rows = 1200, cols = 4200) | "medium"(rows = 1800, cols = 6400) | "large"(rows = 1800, cols = 6400)
            tuple[int, int]: (rows, cols)
        '''
        self.version:int = 316 #1.4.5
        self.ischinese:bool = False
        self.filerevision:int = 0
        self.isfavorite:bool = False
        self.__initializetileframeimportant()
        self.__HeaderFlags_init(world_size)
        self.tiles:Tiles = Tiles(self.tileswide, self.tileshigh)
        self.chests:list[Chest] = []
        self.signs:list[Sign] = []
        self.weighted_pressure_plates:list[PressurePlate] = []
        self.tile_entities:list[TileEntity] = []
        self.__initializeotherdata()

    def set_world_version(self,
                          version:str | int):
        if isinstance(version, int):
            self.version = version
        elif isinstance(version, str):
            if version == "1.4.4":
                self.version = 279
            elif version == "1.4.5":
                self.version = 316
            else:
                raise ValueError("the version string must be 1.4.4 or 1.4.5")

    def __initializetileframeimportant(self):
        '''
        This decides whether tile type is block or sprite.
        self.tileframeimportant[tiletype] == True means tile of #tiletype is sprite.
        '''
        self.tileframeimportant:list[bool] = [False, False, False, True, True, True, False, False, False, False, True, True, True, True, True, True, True, True, True, True, True, True, False, False, True, False, True, True, True, True, False, True, False, True, True, True, True, False, False, False, False, False, True, False, False, False, False, False, False, True, True, False, False, False, False, True, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, True, True, True, True, False, False, True, True, True, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, False, False, True, False, False, True, True, False, False, False, False, False, False, False, False, False, False, True, True, False, True, True, False, False, True, True, True, True, True, True, True, True, False, True, True, True, True, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, True, True, True, True, False, False, False, True, False, False, False, False, False, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, True, False, True, True, False, True, False, False, True, True, True, True, True, True, False, False, False, False, False, False, True, True, False, False, True, False, True, False, True, True, True, True, True, True, True, True, True, True, True, True, True, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True, False, False, False, True, True, True, True, True, True, True, True, True, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, False, False, True, False, True, True, True, True, True, False, False, True, True, False, False, False, False, False, False, False, False, False, True, True, False, True, True, True, False, False, False, False, False, False, False, False, False, True, False, False, False, False, True, True, True, False, True, True, True, True, True, True, True, False, False, False, False, False, False, False, True, True, True, True, True, True, True, False, True, False, False, False, False, False, True, True, True, True, True, True, True, True, True, True, False, False, False, False, False, False, False, False, False, True, True, False, False, False, True, True, True, True, True, False, False, False, False, True, True, False, False, True, True, True, False, True, True, True, False, False, False, False, False, True, True, True, True, True, True, True, True, True, True, True, False, False, False, False, False, False, True, True, True, True, True, True, False, False, False, True, True, True, True, True, True, True, True, True, True, True, False, False, False, True, True, False, False, False, True, False, False, False, True, True, True, True, True, True, True, True, False, True, True, False, False, True, False, True, False, False, False, False, False, True, True, False, False, True, True, True, False, False, False, False, False, False, True, True, True, True, True, True, True, True, True, True, False, True, True, True, True, True, False, False, False, False, True, False, False, False, True, True, True, True, False, True, True, True, True, True, True, True, True, True, True, False, True, True, True, False, False, False, True, True, False, True, True, True, True, True, True, True, False, False, False, False, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, True, True, True, True, True, True, False, False, False, False, True, True, True, True, False, True, False, False, True, False, True, True, False, True, True, True, True, True, True, True, True, True, True, True, True, True, False, True, True, True, False, True, False, False, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True, True, False, True, True, True, True, True, True, True, True, True, True, False, True, True, True, True, True, True, True, True, False, False, False, True, True, False, True, True, True, True, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True]

    def __initializeotherdata(self):
        self.NPCMobs_data = b'\x00\x00\x00\x00\x01%\x00\x00\x00\x00\x00\x97\xe3G\x00\xa0\x16F\x00s\x1c\x00\x00]\x02\x00\x00\x01\x00\x00\x00\x00\x00\x00'
        self.town_manager_data = b'\x00\x00\x00\x00'
        self.bestiary_data = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        self.creative_power_data = b'\x01\x00\x00\x00\x01\x08\x00\x00\x00\x00\x00\x01\t\x00\x00\x01\n\x00\x00\x01\x0c\x00\x00\x00\x00\x00\x01\r\x00\x00\x00'

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
        self.skyblockworld:bool = False
        self.creationtime:int = -8584768520111393488
        self.lastplayed:int = -8584768520111393488
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
        #TODO: 1.4.5, Update the length.
        self.killedmobs:list[int] = [0]*688
        self.claimablebanners:list[int] = [0]*688
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
        self.forcehalloweenforever:bool = False
        self.forcexmasforever:bool = False
        self.vampireseed:bool = False
        self.infectedseed:bool = False
        self.tempmeteorshowercount:int = 0
        self.tempcoinrain:int = 0
        self.teambasedspawnseed:bool = False
        self.teamspawns:list[tuple[int, int]] = []
        self.dualdungeonseed:bool = False
        self.worldmanifestdata:str = '{"GenPassResults":[],"Version":null,"GitSHA":null,"FinalHash":null}' #This is FUCKING mandatory somehow
        
    def load_world(self, *args, **kwargs):
        load_util.load_world(self, *args, **kwargs)

    def save_world(self, save_file_path:str=None):
        save_util.save_world(self, save_file_path=save_file_path)

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

    def place_chest_group1(self,
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
    
    def place_logic_sensor(self,
                           row:int,
                           col:int,
                           type:str | int,
                           on:bool = False):
        if isinstance(type, str):
            if type == "day":
                type = 1
            elif type == "night":
                type = 2
            elif type == "player_above":
                type = 3
            else:
                raise ValueError("The type must be one of the following : day | night | player_above")
        elif isinstance(type, int):
            if type <= 0 or 4 <= type:
                raise ValueError("The type must be one of the following : 1 | 2 | 3")
        if type == 1:
            self.place_sprite(row, col, TileID.LogicSensor, 1, 1, 18, 0)
        elif type == 2:
            self.place_sprite(row, col, TileID.LogicSensor, 1, 1, 0, 18)
        else:
            self.place_sprite(row, col, TileID.LogicSensor, 1, 1, 0, 36)
        sensor_entity = TileEntity(type=TileEntityType.LogicSensor,
                                   entity_id=len(self.tile_entities),
                                   posX=col,
                                   posY=row)
        sensor_entity.attribute["logiccheck"] = type
        sensor_entity.attribute['on'] = on
        self.tile_entities.append(sensor_entity)