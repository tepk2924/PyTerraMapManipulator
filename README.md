# PyTerraMapManipulator

---

Generating & Manipulating terraria world file(.wld) with python

---

1. Loading World
```python
from terrariaworld import TerrariaWorld

world = TerrariaWorld(world_size="large") #This will initialize as a empty world with large size with classic difficulty.
world.load_world()
'''
After this terminal will ask you the path of the wanted .wld file.
'''
```

2. Manipulating World Properties & Tile
```python
from enumeration import GameMode, Channel, TileID, Liquid, Paint, WallID

world.gamemode = GameMode.EXPERT #Setting World Difficulty to Expert
world.title = "MyWorld" #Setting World Title (In Game)
'''
you can find other world properties in the class source code (terrariaworld.py).
there are too many of them to explain them all here.
'''

world.tiles.enter_editmode() #Transposes tile information
'''
world.tiles.tileinfos : np.ndarray (world.tileshigh, world.tileswide, 19) when enter_editmode()
'''

#Filling Entire Left Side of the World with stone block
world.tiles.tileinfos[:, :world.tileswide//2, Channel.TILETYPE] = TileID.Stone

#Remove tile at rectangular area from (0, 600) to (499, 799)
world.tiles.tileinfos[600:800, :500] = -1

#Filling Entire Upper Right Side of the World with lava
world.tiles.tileinfos[:world.tileshigh//2, world.tileswide//2:, Channel.LIQUIDTYPE] = Liquid.LAVA

#Setting lava amount as full(255)
world.tiles.tileinfos[:world.tileshigh//2, world.tileswide//2:, Channel.LIQUIDAMOUNT] = 255

#Actuate Out Entire Lower Left
world.tiles.tileinfos[world.tileshigh//2:, :world.tileswide//2, Channel.INACTIVE] = 1

#Color block at X=2500, Y=1500 with red color
world.tiles.tileinfos[1500, 2500, Channel.TILECOLOR] = Paint.RED

#Fill rectangular area from (5000, 1200) to (5049, 1299) with dirt wall
world.tiles.tileinfos[1200:1300, 5000:5050, Channel.WALL] = WallID.Dirt

#Paint that dirt wall with skyblue color
world.tiles.tileinfos[1200:1300, 5000:5050, Channel.WALLCOLOR] = Paint.SKYBLUE

#Place Red Wire at line segment from (4000, 1000) to (4999, 1000)
world.tiles.tileinfos[1000, 4000:5000, Channel.WIRERED] = 1

world.tiles.exit_editmode() #Transposes back
```

3. Saving World
```python
world.save_world()
'''
After this terminal will ask you the path of the save file path.
If the file path does not ends with ".wld" (which is extension for terraria world file), it will automatically append it.
'''
```

Browse example_script/ to find more usage examples.