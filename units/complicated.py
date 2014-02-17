from united.dimensions import Frequency, Area

from .base import Unit
from .time import Second
from .length import Meter

class Hertz( Unit ):

    numerator   = ()
    denominator = (Second,)

    Dimension   = Frequency
    string      = 'Hz'

class SquareMeter( Unit ):

    numerator   = (Meter,Meter)

    Dimension   = Area
    string      = 'm^2'
