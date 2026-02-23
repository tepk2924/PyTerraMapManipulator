import sys
import os
import numpy as np
import multiprocessing
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

class WorldSaveError(Exception):
    pass

def save_world(wld:"TerrariaWorld",
               save_file_path:str=None,
               process_units:int=1):
    if save_file_path is None:
        save_file_path = input("Saving File Path : ")
    if not save_file_path.endswith(".wld"):
        save_file_path = save_file_path + ".wld"

    if wld.title is None:
        wld.title = os.path.splitext(os.path.basename(save_file_path))[0]

    sectionpointers = [None]*__getsectioncount(wld)

    with open(save_file_path, "wb") as f:
        sectionpointers[0] = __SaveSectionHeader(wld, f, wld.tileframeimportant)
        sectionpointers[1] = __SaveHeaderFlags(wld, f)
        if process_units == 1:
            sectionpointers[2] = __SaveTiles(wld, f, wld.tileswide, wld.tileshigh)
        else:
            sectionpointers[2] = __SaveTiles_Multiprocess(wld, f, wld.tileswide, wld.tileshigh, process_units)
        sectionpointers[3] = __SaveChests(wld, f)
        sectionpointers[4] = __SaveSigns(wld, f)
        sectionpointers[5] = __SaveNPCs(wld, f)

        if wld.version >= 140:
            sectionpointers[6] = __SaveTileEntity(wld, f)
        
        if wld.version >= 170:
            sectionpointers[7] = __SavePressurePlate(wld, f)
        
        if wld.version >= 189:
            f.write(wld.town_manager_data)
            sectionpointers[8] = f.tell()
        
        if wld.version >= 210:
            f.write(wld.bestiary_data)
            sectionpointers[9] = f.tell()
        
        if wld.version >= 220:
            f.write(wld.creative_power_data)
            sectionpointers[10] = f.tell()
        
        __SaveFooter(wld, f)
        __UpdateSectionPointers(wld, f, sectionpointers)

def __getsectioncount(wld:"TerrariaWorld"):
    return 11 if wld.version >= 220 else 10

def __SaveSectionHeader(wld:"TerrariaWorld", f:io.BufferedWriter, tileframeimportant) -> int:
    write_uint32(f, wld.version)

    if wld.version >= 140:
        if wld.ischinese:
            f.write('xindong'.encode('ascii'))
        else:
            f.write('relogic'.encode('ascii'))
        
        write_uint8(f, 2)

        write_uint32(f, wld.filerevision)

        worldheaderflags = 0
        if wld.isfavorite:
            worldheaderflags |= 1
        write_uint64(f, worldheaderflags)

    sectioncount = __getsectioncount(wld)
    write_int16(f, sectioncount)

    for _ in range(sectioncount):
        write_int32(f, 0)
    
    __WriteBitArray(f, tileframeimportant)
    return f.tell()

def __WriteBitArray(f:io.BufferedWriter, tileframeimportant):
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
def __SaveHeaderFlags(wld:"TerrariaWorld", f:io.BufferedWriter) -> int:
    write_string(f, wld.title)

    if wld.version >= 179:
        if wld.version == 179:
            seed = int(wld.seed)
            write_int32(f, seed)
        else:
            write_string(f, wld.seed)
        write_uint64(f, wld.worldgenversion)
    
    if wld.version >= 181:
        f.write(wld.worldguid.bytes)
    
    write_int32(f, wld.worldid)
    write_int32(f, int(wld.leftworld))
    write_int32(f, int(wld.rightworld))
    write_int32(f, int(wld.topworld))
    write_int32(f, int(wld.bottomworld))
    write_int32(f, wld.tileshigh)
    write_int32(f, wld.tileswide)

    if wld.version >= 209:
        write_int32(f, wld.gamemode)
        
        if wld.version >= 222: write_boolean(f, wld.drunkworld)
        if wld.version >= 227: write_boolean(f, wld.goodworld)
        if wld.version >= 238: write_boolean(f, wld.tenthanniversaryworld)
        if wld.version >= 239: write_boolean(f, wld.dontstarveworld)
        if wld.version >= 241: write_boolean(f, wld.notthebeesworld)
        if wld.version >= 249: write_boolean(f, wld.remixworld)
        if wld.version >= 266: write_boolean(f, wld.notrapworld)
        if wld.version >= 266: write_boolean(f, wld.zenithworld)
        if wld.version >= 302: write_boolean(f, wld.skyblockworld)
    elif wld.version == 208:
        write_boolean(f, wld.gamemode == 2)
    elif wld.version == 112:
        write_boolean(f, wld.gamemode == 1)
    else:
        pass

    if wld.version >= 141:
        write_int64(f, wld.creationtime)
    if wld.version >= 284:
        write_int64(f, wld.lastplayed)
    
    write_uint8(f, wld.moontype)
    write_int32(f, wld.treeX0)
    write_int32(f, wld.treeX1)
    write_int32(f, wld.treeX2)
    write_int32(f, wld.treestyle0)
    write_int32(f, wld.treestyle1)
    write_int32(f, wld.treestyle2)
    write_int32(f, wld.treestyle3)
    write_int32(f, wld.cavebackX0)
    write_int32(f, wld.cavebackX1)
    write_int32(f, wld.cavebackX2)
    write_int32(f, wld.cavebackstyle0)
    write_int32(f, wld.cavebackstyle1)
    write_int32(f, wld.cavebackstyle2)
    write_int32(f, wld.cavebackstyle3)
    write_int32(f, wld.icebackstyle)
    write_int32(f, wld.junglebackstyle)
    write_int32(f, wld.hellbackstyle)

    write_int32(f, wld.spawnX)
    write_int32(f, wld.spawnY)
    write_double(f, wld.groundlevel)
    write_double(f, wld.rocklevel)
    write_double(f, wld.time)
    write_boolean(f, wld.daytime)
    write_int32(f, wld.moonphase)
    write_boolean(f, wld.bloodmoon)
    write_boolean(f, wld.iseclipse)
    write_int32(f, wld.dungeonX)
    write_int32(f, wld.dungeonY)

    write_boolean(f, wld.iscrimson)

    write_boolean(f, wld.downedboss1eyeofcthulhu)
    write_boolean(f, wld.downedboss2eaterofworlds)
    write_boolean(f, wld.downedboss3skeletron)
    write_boolean(f, wld.downedqueenbee)
    write_boolean(f, wld.downedmechboss1thedestroyer)
    write_boolean(f, wld.downedmechboss2thetwins)
    write_boolean(f, wld.downedmechboss3skeletronprime)
    write_boolean(f, wld.downedmechbossany)
    write_boolean(f, wld.downedplantboss)
    write_boolean(f, wld.downedgolemboss)

    if wld.version >= 118: write_boolean(f, wld.downedslimekingboss)

    write_boolean(f, wld.savedgoblin)
    write_boolean(f, wld.savedwizard)
    write_boolean(f, wld.savedmech)
    write_boolean(f, wld.downedgoblins)
    write_boolean(f, wld.downedclown)
    write_boolean(f, wld.downedfrost)
    write_boolean(f, wld.downedpirates)

    write_boolean(f, wld.shadoworbsmashed)
    write_boolean(f, wld.spawnmeteor)
    write_uint8(f, wld.shadoworbcount)
    write_int32(f, wld.altarcount)
    write_boolean(f, wld.hardmode)
    if wld.version >= 257: write_boolean(f, wld.partyofdoom)
    write_int32(f, wld.invasiondelay)
    write_int32(f, wld.invasionsize)
    write_int32(f, wld.invasiontype)
    write_double(f, wld.invasionX)
    if wld.version >= 118: write_double(f, wld.slimeraintime)
    if wld.version >= 113: write_uint8(f, wld.sundialcooldown)

    write_boolean(f, wld.israining)
    write_int32(f, wld.tempraintime)
    write_single(f, wld.tempmaxrain)
    write_int32(f, wld.savedoretierscobalt)
    write_int32(f, wld.savedoretiersmythril)
    write_int32(f, wld.savedoretiersadamantitie)
    write_uint8(f, wld.bgtree)
    write_uint8(f, wld.bgcorruption)
    write_uint8(f, wld.bgjungle)
    write_uint8(f, wld.bgsnow)
    write_uint8(f, wld.bghallow)
    write_uint8(f, wld.bgcrimson)
    write_uint8(f, wld.bgdesert)
    write_uint8(f, wld.bgocean)
    write_int32(f, int(wld.cloudbgactive))
    write_int16(f, wld.numclouds)
    write_single(f, wld.windspeedset)

    if wld.version < 95: return f.tell()

    write_int32(f, len(wld.anglers))

    for angler in wld.anglers:
        write_string(f, angler)
    
    if wld.version < 99: return f.tell()

    write_boolean(f, wld.savedangler)

    if wld.version < 101: return f.tell()

    write_int32(f, wld.anglerquest)

    if wld.version < 104: return f.tell()

    write_boolean(f, wld.savedstylist)

    if wld.version >= 129:
        write_boolean(f, wld.savedtaxcollector)
    if wld.version >= 201:
        write_boolean(f, wld.savedgolfer)
    if wld.version >= 107:
        write_int32(f, wld.invasionsizestart)
    if wld.version >= 108:
        write_int32(f, wld.cultistdelay)
    
    if wld.version < 109: return f.tell()

    number_of_mobs = len(wld.killedmobs)
    write_int16(f, number_of_mobs)
    for i in range(number_of_mobs):
        write_int32(f, wld.killedmobs[i])
    
    if wld.version >= 289:
        claimablebannercount = len(wld.claimablebanners)
        write_int16(f, claimablebannercount)
        for banner in wld.claimablebanners:
            write_int16(f, banner)

    if wld.version < 128: return f.tell()

    if wld.version >= 140:
        write_boolean(f, wld.fastforwardtime)
    
    if wld.version < 131: return f.tell()

    write_boolean(f, wld.downedfishron)

    if wld.version >= 140:
        write_boolean(f, wld.downedmartians)
        write_boolean(f, wld.downedlunaticcultist)
        write_boolean(f, wld.downedmoonlord)

    write_boolean(f, wld.downedhalloweenking)
    write_boolean(f, wld.downedhalloweentree)
    write_boolean(f, wld.downedchristmasqueen)
    write_boolean(f, wld.downedsanta)
    write_boolean(f, wld.downedchristmastree)

    if wld.version < 140: return f.tell()

    write_boolean(f, wld.downedcelestialsolar)
    write_boolean(f, wld.downedcelestialvortex)
    write_boolean(f, wld.downedcelestialnebula)
    write_boolean(f, wld.downedcelestialstardust)
    write_boolean(f, wld.celestialsolaractive)
    write_boolean(f, wld.celestialvortexactive)
    write_boolean(f, wld.celestialnebulaactive)
    write_boolean(f, wld.celestialstardustactive)
    write_boolean(f, wld.apocalypse)

    if wld.version >= 170:
        write_boolean(f, wld.partymanual)
        write_boolean(f, wld.partygenuine)
        write_int32(f, wld.partycooldown)
        numparty = len(wld.partyingnpcs)
        write_int32(f, numparty)
        for i in range(numparty):
            write_int32(f, numparty[i])
    
    if wld.version >= 174:
        write_boolean(f, wld.sandstormhappening)
        write_int32(f, wld.sandstormtimeleft)
        write_single(f, wld.sandstormseverity)
        write_single(f, wld.sandstormintendedseverity)

    if wld.version >= 178:
        write_boolean(f, wld.savedbartender)
        write_boolean(f, wld.downeddd2invasiont1)
        write_boolean(f, wld.downeddd2invasiont2)
        write_boolean(f, wld.downeddd2invasiont3)

    if wld.version > 194:
        write_uint8(f, wld.mushroombg)

    if wld.version >= 215:
        write_uint8(f, wld.underworldbg)
    
    if wld.version >= 195:
        write_uint8(f, wld.bgtree2)
        write_uint8(f, wld.bgtree3)
        write_uint8(f, wld.bgtree4)

    if wld.version >= 204:
        write_boolean(f, wld.combatbookused)
    
    if wld.version >= 207:
        write_int32(f, wld.lanternnightcooldown)
        write_boolean(f, wld.lanternnightgenuine)
        write_boolean(f, wld.lanternnightmanual)
        write_boolean(f, wld.lanternnightnextnightisgenuine)

    if wld.version >= 211:
        numtrees = len(wld.treetopvariations)
        write_int32(f, numtrees)
        for i in range(numtrees):
            write_int32(f, wld.treetopvariations[i])

    if wld.version >= 212:
        write_boolean(f, wld.forcehalloweenfortoday)
        write_boolean(f, wld.forcexmasfortoday)

    if wld.version >= 216:
        write_int32(f, wld.savedoretierscopper)
        write_int32(f, wld.savedoretiersiron)
        write_int32(f, wld.savedoretierssilver)
        write_int32(f, wld.savedoretiersgold)
    
    if wld.version >= 217:
        write_boolean(f, wld.boughtcat)
        write_boolean(f, wld.boughtdog)
        write_boolean(f, wld.boughtbunny)

    if wld.version >= 223:
        write_boolean(f, wld.downedempressoflight)
        write_boolean(f, wld.downedqueenslime)
    
    if wld.version >= 240:
        write_boolean(f, wld.downeddeerclops)
    
    if wld.version >= 250:
        write_boolean(f, wld.unlockedslimebluespawn)
    
    if wld.version >= 251:
        write_boolean(f, wld.unlockedmerchantspawn)
        write_boolean(f, wld.unlockeddemolitionistspawn)
        write_boolean(f, wld.unlockedpartygirlspawn)
        write_boolean(f, wld.unlockeddyetraderspawn)
        write_boolean(f, wld.unlockedtrufflespawn)
        write_boolean(f, wld.unlockedarmsdealerspawn)
        write_boolean(f, wld.unlockednursespawn)
        write_boolean(f, wld.unlockedprincessspawn)
    
    if wld.version >= 259:
        write_boolean(f, wld.combatbookvolumetwowasused)
    
    if wld.version >= 260:
        write_boolean(f, wld.peddlerssatchelwasused)
    
    if wld.version >= 261:
        write_boolean(f, wld.unlockedslimegreenspawn)
        write_boolean(f, wld.unlockedslimeoldspawn)
        write_boolean(f, wld.unlockedslimepurplespawn)
        write_boolean(f, wld.unlockedslimerainbowspawn)
        write_boolean(f, wld.unlockedslimeredspawn)
        write_boolean(f, wld.unlockedslimeyellowspawn)
        write_boolean(f, wld.unlockedslimecopperspawn)
    
    if wld.version >= 264:
        write_boolean(f, wld.fastforwardtimetodusk)
        write_uint8(f, wld.moondialcooldown)

    if wld.version >= 287:
        write_boolean(f, wld.forcehalloweenforever)
        write_boolean(f, wld.forcexmasforever)
    
    if wld.version >= 288:
        write_boolean(f, wld.vampireseed)
    
    if wld.version >= 296:
        write_boolean(f, wld.infectedseed)
    
    if wld.version >= 291:
        write_int32(f, wld.tempmeteorshowercount)
        write_int32(f, wld.tempcoinrain)
    
    if wld.version >= 297:
        write_boolean(f, wld.teambasedspawnseed)
        write_uint8(f, len(wld.teamspawns))
        for (x, y) in wld.teamspawns:
            write_int16(f, x)
            write_int16(f, y)
    
    if wld.version >= 304:
        write_boolean(f, wld.dualdungeonseed)
    
    if 299 <= wld.version < 313:
        write_boolean(f, False)
    
    if wld.version >= 299:
        write_string(f, wld.worldmanifestdata)
    
    return f.tell()

def __SaveTiles(wld:"TerrariaWorld",
                f:io.BufferedWriter,
                maxX:int,
                maxY:int) -> int:
    wld.tiles.exit_editmode()
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
            tile = wld.tiles.tileinfos[x, y]
            tiledata, dataindex, headerindex = __serializeTilaData(wld.version, wld.tileframeimportant, tile)

            header1 = tiledata[headerindex]

            rle = 0
            nexty = y + 1
            remainingy = maxY - y - 1
            while (remainingy > 0 and all(tile == wld.tiles.tileinfos[x, nexty]) and int(tile[Channel.TILETYPE]) != 520 and int(tile[Channel.TILETYPE]) != 423):
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
            except struct.error as e:
                print(e)
                print(tiledata)
                exit(1)
            y += 1
    sys.stdout.write(f'\x1b[{backspace}D')
    sys.stdout.write(f"saving tile {total_tiles}/{total_tiles} done... [{"="*barlen}]\n")
    return f.tell()

def __SaveTiles_Multiprocess(wld:"TerrariaWorld",
                             f:io.BufferedWriter,
                             maxX:int,
                             maxY:int,
                             process_units:int):
    assert isinstance(process_units, int)
    assert process_units >= 2
    wld.tiles.exit_editmode()
    pool = multiprocessing.Pool(processes=process_units)
    results = pool.starmap(__Multiprocess_Sub, [(wld.version, wld.tileframeimportant, wld.tiles.
                                                 tileinfos[int(maxX*idx/process_units):int(maxX*(idx + 1)/process_units), :, :].copy(), idx) for idx in range(process_units)])
    pool.close()
    pool.join()
    for arr in results:
        for data in arr:
            write_uint8(f, data)
    return f.tell()

def __Multiprocess_Sub(version:int,
                       tileframeimportant:list[bool],
                       sub_tiles:np.ndarray,
                       idx:int) -> list[int]:
    maxX, maxY, _ = sub_tiles.shape
    total_tiles = maxX*maxY
    digits = len(str(total_tiles))
    barlen = 30
    ret = []
    for x in range(maxX):
        progess = int(barlen*x/maxX)
        print(f"multiprocess unit {idx}: {x*maxY:>{digits}d}/{total_tiles} done... [{"="*progess}{" "*(barlen - progess)}]")
        y = 0
        while y < maxY:
            tile = sub_tiles[x, y]
            tiledata, dataindex, headerindex = __serializeTilaData(version, tileframeimportant, tile)

            header1 = tiledata[headerindex]

            rle = 0
            nexty = y + 1
            remainingy = maxY - y - 1
            while (remainingy > 0 and all(tile == sub_tiles[x, nexty]) and int(tile[Channel.TILETYPE]) != 520 and int(tile[Channel.TILETYPE]) != 423):
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
            ret.extend(tiledata[headerindex:dataindex])
            y += 1
    return ret

def __serializeTilaData(version:int,
                        tileframeimportant:list[int],
                        tile:np.ndarray) -> tuple[list[int], int, int]:
    size = 16 if version >= 269 else 15 if version > 22 else 13

    dataindex = 4 if version >= 269 else 3

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

        if tileframeimportant[TYPE]:
            tiledata[dataindex] = U & 0xFF
            dataindex += 1
            tiledata[dataindex] = (U & 0xFF00) >> 8
            dataindex += 1
            tiledata[dataindex] = V & 0xFF
            dataindex += 1
            tiledata[dataindex] = (V & 0xFF00) >> 8
            dataindex += 1
        
        if version < 269:
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

        if version < 269:
            if WALLCOLOR != 0 or FULLBRIGHTWALL:
                color = WALLCOLOR

                if color == 0 and version < 269 and FULLBRIGHTWALL:
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
        if version >= 269 and LIQUIDTYPE == Liquid.SHIMMER:
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
    
    if WALL > 255 and version >= 222:
        header3 |= 0b0100_0000
        tiledata[dataindex] = WALL >> 8
        dataindex += 1
    
    if version >= 269:
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

def __SaveChests(wld:"TerrariaWorld", f:io.BufferedWriter) -> int:
    count = len(wld.chests)
    write_int16(f, count)
    MAXITEMS_LAGACY = 40
    if wld.version < 294:
        write_int16(f, MAXITEMS_LAGACY)

    for chest in wld.chests:
        item_count = chest.maxitems if wld.version >= 294 else MAXITEMS_LAGACY
        write_int32(f, chest.X)
        write_int32(f, chest.Y)
        write_string(f, chest.name)
        if wld.version >= 294:
            write_int32(f, chest.maxitems) #always 40
        for slot in range(item_count):
            item:Item = chest.items[slot]
            stacksize = item.stacksize
            write_int16(f, stacksize)

            if stacksize > 0:
                item_id = item.netid
                prefix = item.prefix
                write_int32(f, item_id)
                write_uint8(f, prefix)
    
    return f.tell()

def __SaveSigns(wld:"TerrariaWorld", f:io.BufferedWriter) -> int:
    count = len(wld.signs)
    write_int16(f, count)
    for sign in wld.signs:
        text = sign.text
        x = sign.x
        y = sign.y
        write_string(f, text)
        write_int32(f, x)
        write_int32(f, y)
    
    return f.tell()

def __SaveNPCs(wld:"TerrariaWorld", f:io.BufferedWriter) -> int:
    if wld.version >= 268:
        write_int32(f, len(wld.shimmeredtownnpcs))
        for shimtownnpc in wld.shimmeredtownnpcs:
            write_int32(f, shimtownnpc)
    for npc in wld.npcs:
        write_boolean(f, True)
        if wld.version >= 190:
            if npc.spriteid is None:
                raise WorldSaveError("NPC save failure")
            write_int32(f, npc.spriteid)
        else:
            if npc.name is None:
                raise WorldSaveError("NPC save failure")
            write_string(f, npc.name)
        write_string(f, npc.displayname)
        write_single(f, npc.positionX)
        write_single(f, npc.positionY)
        write_boolean(f, npc.ishomless)
        write_int32(f, npc.homeX)
        write_int32(f, npc.homeY)
        if wld.version >= 213:
            bitmask = 1
            write_uint8(f, bitmask)
            if bitmask & (1 << 0):
                write_int32(f, npc.townnpcvariationindex)
        if wld.version >= 315:
            write_boolean(f, npc.homelessdespawn)
    write_boolean(f, False)
    if wld.version >= 140:
        for mob in wld.mobs:
            write_boolean(f, True)
            if wld.version >= 190:
                if mob.spriteid is None:
                    raise WorldSaveError("NPC save failure")
                write_int32(f, mob.spriteid)
            else:
                if mob.name is None:
                    raise WorldSaveError("NPC save failure")
                write_string(f, mob.name)
            write_single(f, mob.positionX)
            write_single(f, mob.positionY)
        write_boolean(f, False)
    return f.tell()

def __SaveTileEntity(wld:"TerrariaWorld", f:io.BufferedWriter) -> int:
    count = len(wld.tile_entities)
    write_int32(f, count)
    for counter in range(count):
        entity = wld.tile_entities[counter]
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
                             TileEntityType.FoodPlatter,
                             TileEntityType.DeadCellsDisplayJar]:
            __SaveItem4TileEntity(f, attribute["item"])
        elif entity_type == TileEntityType.LogicSensor:
            write_uint8(f, attribute["logiccheck"])
            write_boolean(f, attribute["on"])
        elif entity_type == TileEntityType.DisplayDoll:
            item_bitmask = 0
            dye_bitmask = 0
            extraslots_bitmask = 0
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

            if wld.version >= 307:
                write_uint8(f, attribute["pose"])
            if wld.version >= 308:
                hand_item:Item = attribute["hand"]
                if not hand_item.is_empty():
                    extraslots_bitmask |= (1 << 0)
                if not items[8].is_empty():
                    extraslots_bitmask |= (1 << 1)
                if not dyes[8].is_empty():
                    extraslots_bitmask |= (1 << 2)
                write_uint8(f, extraslots_bitmask)
            
            maxslots = 9 if wld.version >= 308 else 8

            for idx in range(maxslots):
                if not items[idx].is_empty():
                    __SaveItem4TileEntity(f, items[idx])
            for idx in range(maxslots):
                if not dyes[idx].is_empty():
                    __SaveItem4TileEntity(f, dyes[idx])
            
            if wld.version >= 308 and not hand_item.is_empty():
                __SaveItem4TileEntity(f, hand_item)
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
                    __SaveItem4TileEntity(f, items[idx])
            for idx in range(2):
                if slots_bitmask & (1 << (idx + 2)):
                    __SaveItem4TileEntity(f, dyes[idx])
        elif entity_type == TileEntityType.TeleportationPylon:
            pass
        elif entity_type in [TileEntityType.CritterAnchor,
                             TileEntityType.KiteAnchor]:
            write_int16(f, attribute["netid"])
        else:
            raise WorldSaveError("Unknown TileEntity Type.")

    return f.tell()

def __SaveItem4TileEntity(f:io.BufferedWriter, item:Item):
    write_int16(f, item.netid)
    write_uint8(f, item.prefix)
    write_int16(f, item.stacksize)

def __SavePressurePlate(wld:"TerrariaWorld", f:io.BufferedWriter) -> int:
    count = len(wld.weighted_pressure_plates)
    write_int32(f, count)
    for plate in wld.weighted_pressure_plates:
        write_int32(f, plate.posX)
        write_int32(f, plate.posY)
    
    return f.tell()

def __SaveFooter(wld:"TerrariaWorld", f:io.BufferedWriter):
    write_boolean(f, True)
    write_string(f, wld.title)
    write_int32(f, wld.worldid)

def __UpdateSectionPointers(wld:"TerrariaWorld", f:io.BufferedWriter, sectionpointers:list[int]):
    f.seek(0)
    write_int32(f, wld.version)
    seeking_pos = 0x18 if wld.version >= 140 else 0x04
    f.seek(seeking_pos)
    write_int16(f, len(sectionpointers))
    for i in range(len(sectionpointers)):
        write_int32(f, sectionpointers[i])
