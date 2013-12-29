from united.dimensions import Length, Time, Mass

from .base import Unit

class Meter( Unit ):

    string  = 'm'
    dim     = Length

class Second( Unit ):

    string  = 's'
    dim     = Time

class Gram( Unit ):

    string  = 'g'
    dim     = Mass
