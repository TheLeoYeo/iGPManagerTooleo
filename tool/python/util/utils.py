from enum import Enum
from os import path


def join(*dirs, uplevel:int=1):
    new_path = path.join(par_dir(uplevel=uplevel), *dirs)
    return new_path


def par_dir(dir:str=__file__, uplevel:int=1):
    if uplevel <= 1:
        return path.dirname(dir)
    
    else:
        return path.dirname(par_dir(dir, uplevel - 1))


class Tyres(Enum):
    SUPERSOFT = "SS"
    SOFT = "S"
    MEDIUM = "M"
    HARD = "H"
    INTERS = "I"
    WETS = "W"
    
    
class StintNumbers(Enum):
    TWO = 0
    THREE = 1
    FOUR = 2
    FIVE = 3
    
    
ALL_TYRE_TYPES = [Tyres.SUPERSOFT, Tyres.SOFT, Tyres.MEDIUM, Tyres.HARD, Tyres.INTERS, Tyres.WETS]
ALL_STINT_NUMBERS = [StintNumbers.TWO, StintNumbers.THREE, StintNumbers.FOUR, StintNumbers.FIVE]
DEFAULT_LENGTH = 3
