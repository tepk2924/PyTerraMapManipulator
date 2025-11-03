import numpy as np

class Tiles:
    '''
    tileinfos: np.ndarray((maxX, maxY, 20), np.int32)
    =============================================
    - bool : 0 - 1, ushort : 0 - 65535, byte : 0 - 255
    - channel 0 (bool) : actuactor info
    - channel 1 (0: full, 1: halfbrick, 2: slope TR, 3: slope TL, 4: slope BR, 5: slope BL) : brickstyle
    - channel 2 (bool) : inactive
    - channel 3 (bool) : is active
    - channel 4 (byte) : liquid amount
    - channel 5 (0: none, 1: water, 2: lava, 3: honey, 8: shimmer) : liquid type
    - channel 6 (byte) : tule color
    - channel 7 (ushort) : tile type
    - channel 8 (int16) : U value
    - channel 9 (int16) : V value
    - channel 10 (ushort) : wall type
    - channel 11 (byte) : wall color
    - channel 12 (bool) : wire blue
    - channel 13 (bool) : wire green
    - channel 14 (bool) : wire red
    - channel 15 (bool) : wire yellow
    - channel 16 (bool) : full bright block
    - chaneel 17 (bool) : full bright wall
    - channel 18 (bool) : invisible block
    - channel 19 (bool) : invisible wall
    '''
    def __init__(self, maxX, maxY):
        self.tileinfos = np.zeros((maxX, maxY, 20), np.int32)
        self.__editmode = False
    
    #These just transposes tile information.
    #Editing is easy when tile information is stored as 2400*8400 (large), but saved as 8400*2400.
    #So, when starting editing and finishing editing, the tile information should be transposed.
    def enter_editmode(self):
        if not self.__editmode:
            self.__editmode = True
            self.tileinfos = self.tileinfos.transpose(1, 0, 2)
    
    def exit_editmode(self):
        if self.__editmode:
            self.__editmode = False
            self.tileinfos = self.tileinfos.transpose(1, 0, 2)