# PyTerraMapManipulator

---

Generating & Manipulating terraria world file(.wld) with python

---

1. Loading World

```python
from terrariaworld import TerrariaWorld

world = TerrariaWorld()
world.load_world() #After this TERMINAL will ask you the path of the wanted .wld file.
```