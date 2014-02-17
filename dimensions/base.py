from united.lib.base import BaseMetaClass, BaseClass
from united.lib.util import classproperty

class DimensionMetaClass( BaseMetaClass ):

    def __getattr__( cls, name ):

        matching_units = filter( lambda u: u.__name__ == name, cls.unit_set )
        if not matching_units: raise AttributeError

        return list( matching_units )[0]

    def __eq__( cls, other ):
        return cls.numerator_dict == other.numerator_dict and cls.denominator_dict == other.denominator_dict

class Dimension( BaseClass ):

    __metaclass__ = DimensionMetaClass

    def __init__( self, value ):
    
        from united.units.base import Unit

        if not isinstance( value, Unit ): raise TypeError( 'Dimensions must be initialized with units.' )
        self.value = value

    def __getattr__( self, name ):

        from united.units import get_conversion_factor

        matching_units = filter( lambda u: u.__name__ == name, self.unit_set )
        if not matching_units: raise AttributeError

        old_unit = self.value.__class__
        new_unit = list( matching_units )[0]

        return new_unit( get_conversion_factor( old_unit, new_unit ) * self.value.value )

    def __repr__( self ): return '<{0} \'{1}\'>'.format( self.__class__.__name__, self.value )

    @classmethod
    def register( cls, unit_cls ): cls.unit_set.add( unit_cls )

    @classproperty
    def unit_set( cls ):

        if not hasattr( cls, '_unit_set' ):

            if cls is Dimension: raise TypeError( 'Do not initialize unit_set on the Dimension base class.' )
            cls._unit_set = set()

        return cls._unit_set
