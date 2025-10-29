class Chest:
    def __init__(self, X, Y, name):
        self.X:int = X
        self.Y:int = Y
        self.name:str = name
        self.items:list[Item] = [Item() for _ in range(40)]

class Item:
    def __init__(self):
        self.stacksize:int = 0
        self.netid:int = 0
        self.prefix:int = 0