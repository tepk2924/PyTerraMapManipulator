import numpy as np

class Tiles:
    '''
    tileinfos: np.ndarray((maxX, maxY, 20), np.int32)
    =============================================
    - bool : 0 - 1, ushort : 0 - 65535, byte : 0 - 255
    - channel 0 (bool) : actuactor info
    - channel 1 (0: full, 1: halfbrick, 2: slope TR, 3: slope TL, 4: slope BR, 5: slope BL) : brickstyle
    - channel 2 (bool) : inactive
    - channel 3 (byte) : liquid amount
    - channel 4 (0: none, 1: water, 2: lava, 3: honey, 8: shimmer) : liquid type
    - channel 5 (byte) : tile color
    - channel 6 (ushort | -1) : tile type, -1 for empty
    - channel 7 (int16) : U value
    - channel 8 (int16) : V value
    - channel 9 (ushort) : wall type
    - channel 10 (byte) : wall color
    - channel 11 (bool) : wire blue
    - channel 12 (bool) : wire green
    - channel 13 (bool) : wire red
    - channel 14 (bool) : wire yellow
    - channel 15 (bool) : full bright block
    - chaneel 16 (bool) : full bright wall
    - channel 17 (bool) : invisible block
    - channel 18 (bool) : invisible wall
    '''
    def __init__(self, maxX, maxY):
        self.tileinfos = np.zeros((maxX, maxY, 19), np.int32)
        self.tileinfos[:, :, 6] = -1 #Filling Air
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