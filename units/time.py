from united.dimensions import Time

from .base import Unit

class Millenium( Unit ):

    string      = 'millenium'
    Dimension   = Time
    prefixed    = False

class Century( Unit ):

    string      = 'century'
    Dimension   = Time
    prefixed    = False

    Millenium   = 10

class Decade( Unit ):

    string      = 'decade'
    Dimension   = Time
    prefixed    = False

    Century     = 10

class LeapYear( Unit ):

    string      = 'leap yr'
    Dimension   = Time
    prefixed    = False

class JulianYear( Unit ):

    string      = 'jyr'
    Dimension   = Time
    prefixed    = False

    Decade      = 10

class Year( Unit ):

    string      = 'yr'
    Dimension   = Time
    prefixed    = False

class Day( Unit ):

    string      = 'days'
    Dimension   = Time
    prefixed    = False

    Year        = 365
    JulianYear  = 365.25
    LeapYear    = 366

class Hour( Unit ):

    string      = 'hr'
    Dimension   = Time
    prefixed    = False

    Day         = 24

class Minute( Unit ):

    string      = 'min.'
    Dimension   = Time
    prefixed    = False

    Hour        = 60

class Second( Unit ):

    string      = 's'
    Dimension   = Time

    Minute      = 60

unit_set = set( [Millenium,Century,Decade,LeapYear,JulianYear,Year,Day,Hour,Minute,Second] )
