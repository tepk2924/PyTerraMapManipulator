class Sign:
    def __init__(self, text, x, y):
        self.text:str = text
        self.x:int = x
        self.y:int = y
    
    def __repr__(self):
        return f"(Sign Object at X = {self.y} and Y = {self.y} with content : {self.text})"