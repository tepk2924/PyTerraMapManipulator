class Tile:
    __slots__ = ('actuator', 'brickstyle', 'inactive', 'isactive', 'v0_lit', 'liquidamount', 'liquidtype', 'tilecolor', 'type', 'U', 'V', 'wall', 'wallcolor', 'wireblue', 'wiregreen', 'wirered', 'wireyellow', 'invisibleblock', 'invisiblewall', 'fullbrightblock', 'fullbrightwall', 'uvtilecache', 'uvwallcache', 'lazymergeid', 'haslazychecked')
    def __init__(self):
        self.actuator:bool = None
        self.brickstyle:int = None
        self.inactive:bool = None
        self.isactive:bool = None
        self.v0_lit:bool = None
        self.liquidamount:int = None
        self.liquidtype:int = None
        self.tilecolor:int = None
        self.type:int = None
        self.U:int = None
        self.V:int = None
        self.wall:int = None
        self.wallcolor:int = None
        self.wireblue:bool = None
        self.wiregreen:bool = None
        self.wirered:bool = None
        self.wireyellow:bool = None
        self.invisibleblock:bool = None
        self.invisiblewall:bool = None
        self.fullbrightblock:bool = None
        self.fullbrightwall:bool = None
        self.uvtilecache:int = 0xFFFF
        self.uvwallcache:int = 0xFFFF
        self.lazymergeid:int = 0xFF
        self.haslazychecked:bool = False

    def isempty(self):
        return (not self.isactive) and (self.wall == 0) and (not self.hasliquid()) and (not self.haswire()) and (not self.actuator)
    
    def haswire(self):
        return self.wireblue or self.wirered or self.wiregreen or self.wireyellow
    
    def hasliquid(self):
        return (self.liquidamount > 0) and (self.liquidtype != self.NONE)
    
    def hasmultiplewires(self):
        return self.wirered + self.wireblue + self.wiregreen + self.wireyellow > 1
    
    def reset(self):
        self.actuator = False
        self.brickstyle = 0x0 #FULL BLOCK
        self.inactive = False
        self.isactive = False
        self.liquidamount = 0
        self.liquidtype = 0x0 #NONE
        self.tilecolor = 0
        self.type = 0
        self.U = 0
        self.V = 0
        self.wall = 0
        self.wallcolor = 0
        self.wireblue = False
        self.wiregreen = False
        self.wirered = False
        self.wireyellow = False
        self.fullbrightblock = False
        self.fullbrightwall = False
        self.invisibleblock = False
        self.invisiblewall = False