class BlockState:
    Solid = 0
    SolidGravity = 1
    Liquid = 2
    Gas = 3

class Block:
    #Name
    #State - Solid, Liquid, Gas
    def __init__(self, _name, _color, _state, _flamable, _causeFire):
        self.name = _name
        self.color = _color
        self.state = _state
        self.flamable = _flamable
        self.causeFire = _causeFire

blocksList = [
    Block('Water', [100, 120, 250], BlockState.Liquid, False, False),
    Block('Sand', [255, 220, 120], BlockState.SolidGravity, False, False),
    Block('Stone', [80, 80, 80], BlockState.Solid, False, False),
    Block('Wood', [180, 100, 0], BlockState.Solid, True, False),
    Block('Gas', [172, 250, 162], BlockState.Gas, False, False),
    Block('Flamable Gas', [200, 250, 100], BlockState.Gas, True, False),
    Block('Oil', [0, 20, 72], BlockState.Liquid, True, False),
    Block('Fire', [255, 128, 0], BlockState.SolidGravity, False, True),
    Block('Lava', [255, 142, 0], BlockState.Liquid, False, True)
]

def getBlock(_color):
    for x in blocksList:
        if(x.color == _color):
            return x
    return Block('', [0, 0, 0], BlockState.Solid, False, False)