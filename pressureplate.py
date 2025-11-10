class PressurePlate:
    def __init__(self, posX, posY):
        self.posX = posX
        self.posY = posY
    
    def __repr__(self):
        return f"(Pressure Plate Object at X = {self.posX}, Y = {self.posY})"