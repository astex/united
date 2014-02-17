from .base import Dimension
from .basic import Length, Time

class Area( Dimension ):

    numerator   = (Length, Length)
    denominator = ()

class Velocity( Dimension ):

    numerator   = (Length,)
    denominator = (Time,)

class Frequency( Dimension ):

    numerator   = ()
    denominator = (Time,)
