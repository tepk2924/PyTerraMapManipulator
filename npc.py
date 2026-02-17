from dataclasses import dataclass

@dataclass
class NPC:
    homeX:int = None
    homeY:int = None
    ishomeless:bool = None
    homelessdespawn:bool = None
    name:str = None
    positionX:float = None
    positionY:float = None
    spriteid:int = None
    displayname:str = None
    townnpcvariationindex:int = None