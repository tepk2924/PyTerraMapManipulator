from dataclasses import dataclass
from enumeration import ItemID, PrefixID

class Chest:
    def __init__(self, X, Y, name):
        self.X:int = X
        self.Y:int = Y
        self.name:str = name
        self.items:list[Item] = [Item() for _ in range(40)]
        self.maxitems = 40
    
    def __repr__(self):
        return f"Chest Object ax X = {self.X} and Y = {self.Y} with name : {self.name} and items: \n {self.items}"

class Item:
    def __init__(self,
                 stacksize=0,
                 netid=ItemID.NoItem,
                 prefix=PrefixID.NoPrefix):
        self.stacksize:int = stacksize
        self.netid:int = netid
        self.prefix:int = prefix
    
    def is_empty(self):
        if self.stacksize == 0:
            return True
        if self.netid == ItemID.NoItem:
            return True
        return False

    def __repr__(self):
        if self.is_empty(): return "()"

        if self.prefix in PrefixID._value2member_map_:
            prefix = PrefixID._value2member_map_[self.prefix].name
        else:
            prefix = "Unknown Prefix"
        
        if self.netid in ItemID._value2member_map_:
            netid = ItemID._value2member_map_[self.netid].name
        else:
            netid = "Unknown Item"
        
        return f"({prefix} {netid}*{self.stacksize})"