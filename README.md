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
from enumeration import GameMode, Ch, TileID

world.gamemode = GameMode.EXPERT #Setting World Difficulty to Expert
world.title = "MyWorld" #Setting World Title (In Game)

world.tiles.enter_editmode()
world.tiles.tileinfos[:, :, Ch.TILETYPE] = TileID.Stone #Filling Entire World with stone block
world.tiles.exit_editmode()
```

3. Saving World
```python
world.save_world()
'''
After this terminal will ask you the path of the save file path.
If the file path does not ends with ".wld" (which is extension for terraria world file), it will automatically append it.
'''
```