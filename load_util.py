import uuid
import datetime
import sys
from fileIOutils import *
from tiles import Tiles
from chest import Chest, Item
from sign import Sign
from pressureplate import PressurePlate
from tileentity import TileEntity
from enumeration import BrickStyle, Liquid, Channel, GameMode, TileID, TileEntityType, ItemID
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from terrariaworld import TerrariaWorld

class WorldLoadError(Exception):
    pass

#TODO: maybe this should be updated upon 1.4.5?
def load_world(wld:"TerrariaWorld",
               file_path=None,
               chest_verbose=False,
               sign_verbose=False,
               tile_entity_verbose=False,
               skip_header_flags=False,
               skip_tile_data=False,
               skip_chest_data=False,
               skip_sign_data=False,
               skip_tile_entity_data=False,
               ):
    if file_path is None:
        file_path = input("Map file path : ")
    with open(file_path, "rb") as f:
        wld.version = read_uint32(f)

        tileframeimportant, section_ptrs = __LoadSectionHeader(wld, f)
        wld.tileframeimportant = tileframeimportant

        if f.tell() != section_ptrs[0]:
            raise WorldLoadError("Unexpected Position: Invalid File Format Section")
        
        if skip_header_flags:
            f.seek(section_ptrs[1])
        else:
            #World Informations
            __LoadHeaderFlags(wld, f)
            if f.tell() != section_ptrs[1]:
                raise WorldLoadError("Unexpected Position: Invalid Header Flags")

        if skip_tile_data:
            f.seek(section_ptrs[2])
        else:
            #World Tile Datas
            wld.tiles = __LoadTileData(f, wld.tileswide, wld.tileshigh, wld.version, tileframeimportant)
            if f.tell() != section_ptrs[2]:
                print("Correcting Position Error")
                f.seek(section_ptrs[2])

        if skip_chest_data:
            f.seek(section_ptrs[3])
        else:
            wld.chests = __LoadChestData(wld, f, chest_verbose)
            if f.tell() != section_ptrs[3]:
                raise WorldLoadError("Unexpected Position: Invalid Chest Data")
        
        if skip_sign_data:
            f.seek(section_ptrs[4])
        else:
            wld.signs = __LoadSignData(f, sign_verbose)
            #여기 즈음에 sign 데이터의 tile type이 진짜 표지판의 종류인지 검사하는 코드가 원래 있었음
            if f.tell() != section_ptrs[4]:
                raise WorldLoadError("Unexpected Position: Invalid Sign Data")
        
        if wld.version >= 140:
            NPCMobs_data_len = section_ptrs[5] - section_ptrs[4]
            wld.NPCMobs_data = f.read(NPCMobs_data_len)
            if f.tell() != section_ptrs[5]:
                raise WorldLoadError("Unexpected Position: Invalid Mob and NPC Data")
            if skip_tile_entity_data:
                f.seek(section_ptrs[6])
            else:
                wld.tile_entities = __LoadTileEntity(wld, f, tile_entity_verbose)
                if f.tell() != section_ptrs[6]:
                    raise WorldLoadError("Unexpected Position: Invalid Tile Entities Section")
        else:
            NPCMobs_data_len = section_ptrs[5] - section_ptrs[4]
            wld.NPCMobs_data = f.read(NPCMobs_data_len)
            if f.tell() != section_ptrs[5]:
                raise WorldLoadError("Unexpected Position: Invalid NPC Data")
        
        if wld.version >= 170:
            #.wld file saves weighted pressure plates that were being stepped on while player exiting the world. Interesting.
            wld.pressure_plates = __LoadPressurePlate(f)
            if f.tell() != section_ptrs[7]:
                raise WorldLoadError("Unexpected Position: Invalid Weighted Pressure Plate Section")
        
        if wld.version >= 189:
            town_manager_data_len = section_ptrs[8] - section_ptrs[7]
            wld.town_manager_data = f.read(town_manager_data_len)
            if f.tell() != section_ptrs[8]:
                raise WorldLoadError("Unexpected Position: Invalid Town Manager Section")
        
        if wld.version >= 210:
            besitary_data_len = section_ptrs[9] - section_ptrs[8]
            wld.bestiary_data = f.read(besitary_data_len)
            if f.tell() != section_ptrs[9]:
                raise WorldLoadError("Unexpected Position: Invalid Bestiary Section")
        
        if wld.version >= 220:
            creative_power_len = section_ptrs[10] - section_ptrs[9]
            wld.creative_power_data = f.read(creative_power_len)
            if f.tell() != section_ptrs[10]:
                raise WorldLoadError("Unexpected Position: Invalid Bestiary Section")
        
        __LoadFooter(wld, f)            

def __LoadSectionHeader(wld:"TerrariaWorld", f:io.BufferedReader):
    #loading section header
    if wld.version >= 140:
        tmp = f.tell()
        wld.ischinese = (f.read(1).decode('ascii') == 'x')
        f.seek(tmp)
        headerformat = f.read(7).decode('ascii')
        filetype = f.read(1)
        wld.filerevision = read_uint32(f)
        flags = read_uint64(f)
        wld.isfavorite = ((flags & 1) == 1)
    sectioncount = read_int16(f)
    section_ptrs = []
    for _ in range(sectioncount):
        section_ptrs.append(read_int32(f))
    
    tileframeimportant = __ReadBitArray(f)
    return tileframeimportant, section_ptrs

def __ReadBitArray(f:io.BufferedReader):
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
def __LoadHeaderFlags(wld:"TerrariaWorld", f:io.BufferedReader):
    wld.title = read_string(f)

    if wld.version >= 179:
        if wld.version == 179:
            wld.seed = str(read_int32(f))
        else:
            wld.seed = read_string(f)
        wld.worldgenversion = read_uint64(f)
    else:
        wld.seed = ""
    if wld.version >= 181:
        wld.worldguid = uuid.UUID(bytes_le=f.read(16))
    else:
        wld.worldguid = uuid.uuid1()

    wld.worldid = read_int32(f)
    wld.leftworld = float(read_int32(f))
    wld.rightworld = float(read_int32(f))
    wld.topworld = float(read_int32(f))
    wld.bottomworld = float(read_int32(f))
    wld.tileshigh = read_int32(f)
    wld.tileswide = read_int32(f)

    if wld.version >= 209:
        wld.gamemode = read_int32(f)

        if wld.version >= 222: wld.drunkworld = read_boolean(f)
        if wld.version >= 227: wld.goodworld = read_boolean(f)
        if wld.version >= 238: wld.tenthanniversaryworld = read_boolean(f)
        if wld.version >= 239: wld.dontstarveworld = read_boolean(f)
        if wld.version >= 241: wld.notthebeesworld = read_boolean(f)
        if wld.version >= 249: wld.remixworld = read_boolean(f)
        if wld.version >= 266: wld.notrapworld = read_boolean(f)
        wld.zenithworld = (wld.remixworld and wld.drunkworld) if wld.version < 267 else read_boolean(f)
        if wld.version >= 302: wld.skyblockworld = read_boolean(f)
    elif wld.version == 208:
        wld.gamemode = 2 if read_boolean(f) else 0
    elif wld.version == 112:
        wld.gamemode = 1 if read_boolean(f) else 0
    else:
        wld.gamemode = 0

    wld.creationtime = read_int64(f) if wld.version >= 141 else int(datetime.datetime.now().timestamp())
    wld.lastplayed = read_int64(f) if wld.version >= 284 else int(datetime.datetime.now())

    wld.moontype = read_uint8(f)
    wld.treeX[0] = read_int32(f)
    wld.treeX[1] = read_int32(f)
    wld.treeX[2] = read_int32(f)
    wld.treeX0 = wld.treeX[0]
    wld.treeX1 = wld.treeX[1]
    wld.treeX2 = wld.treeX[2]
    wld.treestyle0 = read_int32(f)
    wld.treestyle1 = read_int32(f)
    wld.treestyle2 = read_int32(f)
    wld.treestyle3 = read_int32(f)
    wld.cavebackX[0] = read_int32(f)
    wld.cavebackX[1] = read_int32(f)
    wld.cavebackX[2] = read_int32(f)
    wld.cavebackX0 = wld.cavebackX[0]
    wld.cavebackX1 = wld.cavebackX[1]
    wld.cavebackX2 = wld.cavebackX[2]
    wld.cavebackstyle0 = read_int32(f)
    wld.cavebackstyle1 = read_int32(f)
    wld.cavebackstyle2 = read_int32(f)
    wld.cavebackstyle3 = read_int32(f)
    wld.icebackstyle = read_int32(f)
    wld.junglebackstyle = read_int32(f)
    wld.hellbackstyle = read_int32(f)

    wld.spawnX = read_int32(f)
    wld.spawnY = read_int32(f)
    wld.groundlevel = read_double(f)
    wld.rocklevel = read_double(f)
    wld.time = read_double(f)
    wld.daytime = read_boolean(f)
    wld.moonphase = read_int32(f)
    wld.bloodmoon = read_boolean(f)
    wld.iseclipse = read_boolean(f)
    wld.dungeonX = read_int32(f)
    wld.dungeonY = read_int32(f)

    wld.iscrimson = read_boolean(f)

    wld.downedboss1eyeofcthulhu = read_boolean(f)
    wld.downedboss2eaterofworlds = read_boolean(f)
    wld.downedboss3skeletron = read_boolean(f)
    wld.downedqueenbee = read_boolean(f)
    wld.downedmechboss1thedestroyer = read_boolean(f)
    wld.downedmechboss2thetwins = read_boolean(f)
    wld.downedmechboss3skeletronprime = read_boolean(f)
    wld.downedmechbossany = read_boolean(f)
    wld.downedplantboss = read_boolean(f)
    wld.downedgolemboss = read_boolean(f)

    if wld.version >= 118: wld.downedslimekingboss = read_boolean(f)

    wld.savedgoblin = read_boolean(f)
    wld.savedwizard = read_boolean(f)
    wld.savedmech = read_boolean(f)
    wld.downedgoblins = read_boolean(f)
    wld.downedclown = read_boolean(f)
    wld.downedfrost = read_boolean(f)
    wld.downedpirates = read_boolean(f)

    wld.shadoworbsmashed = read_boolean(f)
    wld.spawnmeteor = read_boolean(f)
    wld.shadoworbcount = read_uint8(f)
    wld.altarcount = read_int32(f)
    wld.hardmode = read_boolean(f)
    if wld.version >= 257: wld.partyofdoom = read_boolean(f)
    wld.invasiondelay = read_int32(f)
    wld.invasionsize = read_int32(f)
    wld.invasiontype = read_int32(f)
    wld.invasionX = read_double(f)
    if wld.version >= 118: wld.slimeraintime = read_double(f)
    if wld.version >= 113: wld.sundialcooldown = read_uint8(f)
    
    wld.israining = read_boolean(f)
    wld.tempraintime = read_int32(f)
    wld.tempmaxrain = read_single(f)
    wld.savedoretierscobalt = read_int32(f)
    wld.savedoretiersmythril = read_int32(f)
    wld.savedoretiersadamantitie = read_int32(f)
    wld.bgtree = read_uint8(f)
    wld.bgcorruption = read_uint8(f)
    wld.bgjungle = read_uint8(f)
    wld.bgsnow = read_uint8(f)
    wld.bghallow = read_uint8(f)
    wld.bgcrimson = read_uint8(f)
    wld.bgdesert = read_uint8(f)
    wld.bgocean = read_uint8(f)
    wld.cloudbgactive = float(read_int32(f))
    wld.numclouds = read_int16(f)
    wld.windspeedset = read_single(f)
    
    if wld.version < 95: return

    for _ in range(read_int32(f)):
        wld.anglers.append(read_string(f))
    
    if wld.version < 99: return

    wld.savedangler = read_boolean(f)

    if wld.version < 101: return

    wld.anglerquest = read_int32(f)

    if wld.version < 104: return

    wld.savedstylist = read_boolean(f)

    if wld.version >= 140:
        wld.savedtaxcollector = read_boolean(f)
    if wld.version >= 201:
        wld.savedgolfer = read_boolean(f)
    if wld.version >= 107:
        wld.invasionsizestart = read_int32(f)
    wld.cultistdelay = read_int32(f) if wld.version >= 108 else 86400

    if wld.version < 109: return

    __LoadBanners(wld, f)
    
    if wld.version < 128: return

    if wld.version >= 140:
        wld.fastforwardtime = read_boolean(f)
    
    if wld.version < 131: return

    wld.downedfishron = read_boolean(f)
    
    if wld.version >= 140:
        wld.downedmartians = read_boolean(f)
        wld.downedlunaticcultist = read_boolean(f)
        wld.downedmoonlord = read_boolean(f)
    
    wld.downedhalloweenking = read_boolean(f)
    wld.downedhalloweentree = read_boolean(f)
    wld.downedchristmasqueen = read_boolean(f)
    wld.downedsanta = read_boolean(f)
    wld.downedchristmastree = read_boolean(f)

    if wld.version < 140: return

    wld.downedcelestialsolar = read_boolean(f)
    wld.downedcelestialvortex = read_boolean(f)
    wld.downedcelestialnebula = read_boolean(f)
    wld.downedcelestialstardust = read_boolean(f)
    wld.celestialsolaractive = read_boolean(f)
    wld.celestialvortexactive = read_boolean(f)
    wld.celestialnebulaactive = read_boolean(f)
    wld.celestialstardustactive = read_boolean(f)
    wld.apocalypse = read_boolean(f)

    if wld.version >= 170:
        wld.partymanual = read_boolean(f)
        wld.partygenuine = read_boolean(f)
        wld.partycooldown = read_int32(f)
        numparty = read_int32(f)
        for _ in range(numparty):
            wld.partyingnpcs.append(read_int32(f))
    
    if wld.version >= 174:
        wld.sandstormhappening = read_boolean(f)
        wld.sandstormtimeleft = read_int32(f)
        wld.sandstormseverity = read_single(f)
        wld.sandstormintendedseverity = read_single(f)
    
    if wld.version >= 178:
        wld.savedbartender = read_boolean(f)
        wld.downeddd2invasiont1 = read_boolean(f)
        wld.downeddd2invasiont2 = read_boolean(f)
        wld.downeddd2invasiont3 = read_boolean(f)
    
    if wld.version > 194:
        wld.mushroombg = read_uint8(f)
    
    if wld.version >= 215:
        wld.underworldbg = read_uint8(f)
    
    if wld.version >= 195:
        wld.bgtree2 = read_uint8(f)
        wld.bgtree3 = read_uint8(f)
        wld.bgtree4 = read_uint8(f)
    else:
        wld.bgtree2 = wld.bgtree
        wld.bgtree3 = wld.bgtree
        wld.bgtree4 = wld.bgtree

    if wld.version >= 204:
        wld.combatbookused = read_boolean(f)
    
    if wld.version >= 207:
        wld.lanternnightcooldown = read_int32(f)
        wld.lanternnightgenuine = read_boolean(f)
        wld.lanternnightmanual = read_boolean(f)
        wld.lanternnightnextnightisgenuine = read_boolean(f)
    
    if wld.version >= 211:
        numtrees = read_int32(f)
        wld.treetopvariations = [0]*max([13, numtrees])
        for i in range(numtrees):
            wld.treetopvariations[i] = read_int32(f)
    else:
        wld.treetopvariations[0] = wld.treestyle0
        wld.treetopvariations[1] = wld.treestyle1
        wld.treetopvariations[2] = wld.treestyle2
        wld.treetopvariations[3] = wld.treestyle3
        wld.treetopvariations[4] = wld.bgcorruption
        wld.treetopvariations[5] = wld.junglebackstyle
        wld.treetopvariations[6] = wld.bgsnow
        wld.treetopvariations[7] = wld.bghallow
        wld.treetopvariations[8] = wld.bgcrimson
        wld.treetopvariations[9] = wld.bgdesert
        wld.treetopvariations[10] = wld.bgocean
        wld.treetopvariations[11] = wld.mushroombg
        wld.treetopvariations[12] = wld.underworldbg

    if wld.version >= 212:
        wld.forcehalloweenfortoday = read_boolean(f)
        wld.forcexmasfortoday = read_boolean(f)
    
    if wld.version >= 216:
        wld.savedoretierscopper = read_int32(f)
        wld.savedoretiersiron = read_int32(f)
        wld.savedoretierssilver = read_int32(f)
        wld.savedoretiersgold = read_int32(f)
    else:
        wld.savedoretierscopper = -1
        wld.savedoretiersiron = -1
        wld.savedoretierssilver = -1
        wld.savedoretiersgold = -1
    
    if wld.version >= 217:
        wld.boughtcat = read_boolean(f)
        wld.boughtdog = read_boolean(f)
        wld.boughtbunny = read_boolean(f)
    
    if wld.version >= 223:
        wld.downedempressoflight = read_boolean(f)
        wld.downedqueenslime = read_boolean(f)
    
    if wld.version >= 240:
        wld.downeddeerclops = read_boolean(f)
    
    if wld.version >= 250:
        wld.unlockedslimebluespawn = read_boolean(f)
    
    if wld.version >= 251:
        wld.unlockedmerchantspawn = read_boolean(f)
        wld.unlockeddemolitionistspawn = read_boolean(f)
        wld.unlockedpartygirlspawn = read_boolean(f)
        wld.unlockeddyetraderspawn = read_boolean(f)
        wld.unlockedtrufflespawn = read_boolean(f)
        wld.unlockedarmsdealerspawn = read_boolean(f)
        wld.unlockednursespawn = read_boolean(f)
        wld.unlockedprincessspawn = read_boolean(f)
    
    if wld.version >= 259:
        wld.combatbookvolumetwowasused = read_boolean(f)
    
    if wld.version >= 260:
        wld.peddlerssatchelwasused = read_boolean(f)
    
    if wld.version >= 261:
        wld.unlockedslimegreenspawn = read_boolean(f)
        wld.unlockedslimeoldspawn = read_boolean(f)
        wld.unlockedslimepurplespawn = read_boolean(f)
        wld.unlockedslimerainbowspawn = read_boolean(f)
        wld.unlockedslimeredspawn = read_boolean(f)
        wld.unlockedslimeyellowspawn = read_boolean(f)
        wld.unlockedslimecopperspawn = read_boolean(f)
    
    if wld.version >= 264:
        wld.fastforwardtimetodusk = read_boolean(f)
        wld.moondialcooldown = read_uint8(f)
    
    if wld.version >= 287:
        wld.forcehalloweenforever = read_boolean(f)
        wld.forcexmasforever = read_boolean(f)
    else:
        wld.forcehalloweenforever = False
        wld.forcexmasforever = False
    if wld.version >= 288:
        wld.vampireseed = read_boolean(f)
    if wld.version >= 296:
        wld.infectedseed = read_boolean(f)
    if wld.version >= 291:
        wld.tempmeteorshowercount = read_int32(f)
        wld.tempcoinrain = read_int32(f)
    else:
        wld.tempmeteorshowercount = 0
        wld.tempcoinrain = 0
    if wld.version >= 297:
        wld.teambasedspawnseed = read_boolean(f)
        __LoadTeamSpawns(wld, f)
    else:
        wld.teambasedspawnseed = False
        wld.teamspawns.clear()
    
    wld.dualdungeonseed = wld.version >= 304 and read_boolean(f)

    if 299 <= wld.version < 313:
        read_uint32(f)
    if wld.version >= 299:
        wld.worldmanifestdata = read_string(f)

    return

def __LoadBanners(wld:"TerrariaWorld",
                  f:io.BufferedReader):
    wld.killedmobs.clear()
    number_of_mobs = read_int16(f)
    for _ in range(number_of_mobs):
        wld.killedmobs.append(read_int32(f))
    if wld.version < 289: return
    wld.claimablebanners.clear()
    claimablebannercount = read_int16(f)
    for _ in range(claimablebannercount):
        wld.claimablebanners.append(read_int16(f))

def __LoadTeamSpawns(wld:"TerrariaWorld",
                     f:io.BufferedReader):
    wld.teamspawns.clear()
    l = read_uint8(f)
    for _ in range(l):
        x = read_int16(f)
        y = read_int16(f)
        wld.teamspawns.append((x, y))

def __LoadTileData(f:io.BufferedReader,
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
            single_tile, rle = __deserializetiledata(f, tileframeimportant, version)
            tiles.tileinfos[x, y, :] = single_tile
            while rle > 0:
                y += 1
                tiles.tileinfos[x, y, :] = tiles.tileinfos[x, y - 1, :]
                rle -= 1
            y += 1
    sys.stdout.write(f'\x1b[{backspace}D')
    sys.stdout.write(f"loading tile {total_tiles}/{total_tiles} done... [{"="*barlen}]\n")
    return tiles

def __deserializetiledata(f, tileframeimportant, version) -> tuple[list, int]:
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

def __LoadChestData(wld:"TerrariaWorld", f:io.BufferedReader, chest_verbose) -> list[Chest]:
    total_chests = read_int16(f)
    if wld.version < 294:
        max_items = read_int16(f)
    else:
        max_items = 40
    # CHEST_MAX = 40

    # if max_items > CHEST_MAX:
    #     items_per_chest = CHEST_MAX
    #     overflowitems = max_items - CHEST_MAX
    # else:
    #     items_per_chest = max_items
    #     overflowitems = 0

    ret_chests = []

    for i in range(total_chests):
        X = read_int32(f)
        Y = read_int32(f)
        name = read_string(f)
        chest = Chest(X, Y, name)

        if wld.version >= 294:
            chest.maxitems = read_int32(f) #always 40
        for slot in range(chest.maxitems):
            stacksize = read_int16(f)
            chest.items[slot].stacksize = stacksize

            if stacksize > 0:
                item_id = read_int32(f)
                prefix = read_uint8(f)

                chest.items[slot].netid = item_id
                chest.items[slot].stacksize = stacksize
                chest.items[slot].prefix = prefix
    
        # for overflow in range(overflowitems):
        #     stacksize = read_int16(f)
        #     if stacksize > 0:
        #         read_int32(f)
        #         read_uint8(f)
        
        ret_chests.append(chest)
    
    if chest_verbose:
        for chest in ret_chests:
            print(chest)

    return ret_chests

def __LoadSignData(f:io.BufferedReader, sign_verbose) -> list[Sign]:
    totalsigns = read_int16(f)

    ret_signs = []

    for i in range(totalsigns):
        text = read_string(f)
        x = read_int32(f)
        y = read_int32(f)
        sign = Sign(text, x, y)

        ret_signs.append(sign)
    
    if sign_verbose:
        for sign in ret_signs:
            print(sign)        

    return ret_signs

#TODO: maybe this should be updated upon 1.4.5?
def __LoadTileEntity(wld: "TerrariaWorld", f:io.BufferedReader, tile_entity_verbose) -> list[TileEntity]:
    count = read_int32(f)
    ret_entities = []
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
                             TileEntityType.FoodPlatter,
                             TileEntityType.DeadCellsDisplayJar]:
            entity.attribute["item"] = __LoadItem4TileEntity(f)
        elif entity_type == TileEntityType.LogicSensor:
            entity.attribute["logiccheck"] = read_uint8(f)
            entity.attribute["on"] = read_boolean(f)
        elif entity_type == TileEntityType.DisplayDoll:
            item_bitmask = read_uint8(f)
            dye_bitmask = read_uint8(f)

            if wld.version >= 307:
                pose = read_uint8(f)
            
            extraslots_bitmask = read_uint8(f) if wld.version >= 308 else 0

            v311:bool = False
            if wld.version == 311:
                v311 = bool(extraslots_bitmask & (1 << 1))
                extraslots_bitmask &= 0b11111101
            
            maxslots = 9 if wld.version >= 308 else 8

            items:list[Item] = [Item() for _ in range(9)]
            dyes:list[Item] = [Item() for _ in range(9)]
            hand:Item = Item()
            for idx in range(maxslots):
                hasitem = bool(item_bitmask & (1 << idx)) if idx < 8 else bool(extraslots_bitmask & (1 << 1))
                if hasitem:
                    items[idx] = __LoadItem4TileEntity(f)
            for idx in range(maxslots):
                hasdye = bool(dye_bitmask & (1 << idx)) if idx < 8 else bool(extraslots_bitmask & (1 << 2))
                if hasdye:
                    dyes[idx] = __LoadItem4TileEntity(f)
            if extraslots_bitmask & (1 << 0):
                hand = __LoadItem4TileEntity(f)
            entity.attribute["items"] = items
            entity.attribute["dyes"] = dyes
            entity.attribute["hand"] = hand
            entity.attribute["pose"] = pose
            if v311: #WTF
                items[8] = __LoadItem4TileEntity(f)
        elif entity_type == TileEntityType.HatRack:
            slots_bitmask = read_uint8(f)
            items:list[Item] = [Item() for _ in range(2)]
            dyes:list[Item] = [Item() for _ in range(2)]
            for idx in range(2):
                if slots_bitmask & (1 << idx):
                    items[idx] = __LoadItem4TileEntity(f)
            for idx in range(2):
                if slots_bitmask & (1 << (idx + 2)):
                    dyes[idx] = __LoadItem4TileEntity(f)
            entity.attribute["items"] = items
            entity.attribute["dyes"] = dyes
        elif entity_type == TileEntityType.TeleportationPylon:
            pass
        elif entity_type in [TileEntityType.CritterAnchor,
                             TileEntityType.KiteAnchor]:
            entity.attribute["netid"] = read_int16(f)
        else:
            raise WorldLoadError("Unknown TileEntity Type.")
        ret_entities.append(entity)
    
    if tile_entity_verbose:
        for entity in ret_entities:
            print(entity)
    return ret_entities

def __LoadItem4TileEntity(f) -> Item:
    netid = read_int16(f)
    prefix = read_uint8(f)
    stacksize = read_int16(f)
    return Item(netid=netid, prefix=prefix, stacksize=stacksize)

def __LoadPressurePlate(f) -> list[PressurePlate]:
    count = read_int32(f)
    ret = []
    for counter in range(count):
        posX = read_int32(f)
        posY = read_int32(f)
        ret.append(PressurePlate(posX, posY))
    return ret

def __LoadFooter(wld, f):
    boolean_footer = read_boolean(f)
    # print(f"{boolean_footer = }")
    if not boolean_footer:
        raise WorldLoadError("Invalid Boolean Footer")
    
    title_footer = read_string(f)
    # print(f"{title_footer = }")
    if title_footer != wld.title:
        raise WorldLoadError("Invalid World Title Footer")
    
    world_id_footer = read_int32(f)
    # print(f"{world_id_footer = }")
    if world_id_footer != wld.worldid:
        raise WorldLoadError("Invalid World ID Footer")
