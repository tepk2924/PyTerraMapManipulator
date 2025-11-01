class Chest:
    def __init__(self, X, Y, name):
        self.X:int = X
        self.Y:int = Y
        self.name:str = name
        self.items:list[Item] = [Item() for _ in range(40)]
    
    def __repr__(self):
        return f"Chest Object ax X = {self.X} and Y = {self.Y} with name : {self.name} and items: \n {self.items}"

class Item:
    def __init__(self):
        self.stacksize:int = 0
        self.netid:int = 0
        self.prefix:int = 0
    
    def __repr__(self):
        return f"(stacksize = {self.stacksize}, id = {self.netid}, prefix = {self.prefix})"