class TileEntity:
    def __init__(self, type, entity_id, posX, posY):
        self.type:int = type
        self.entity_id:int = entity_id
        self.posX:int = posX
        self.posY:int = posY
        self.attribute:dict = {}
    
    def __repr__(self):
        return f"(type = {self.type}, entity_id = {self.entity_id}, posX = {self.posX}, posY = {self.posY}, attribute = {self.attribute})"