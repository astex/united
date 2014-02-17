from united.dimensions import Length

from .base import Unit

class Meter( Unit ):

    string      = 'm'
    Dimension   = Length

class Mile( Unit ):

    string      = 'mile'
    Dimension   = Length
    prefixed    = False

class Foot( Unit ):

    string      = 'ft'
    Dimension   = Length
    prefixed    = False

    Mile        = 5280

class Inch( Unit ):

    string      = 'in.'
    Dimension   = Length
    prefixed    = False

    Meter       = 39.3701
    Foot        = 12

unit_set = set( [ Meter, Mile, Foot, Inch ] )
