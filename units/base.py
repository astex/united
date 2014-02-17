import pdb

from united.lib.util import classproperty
from united.lib.base import BaseMetaClass, BaseClass
from united.dimensions import Dimensionless
from united.dimensions.exceptions import DimError

prefixes = set( (
    ( 'Kilo', 'k', 1000 ),
    ( 'Centa', 'C', 100 ),
    ( 'Deca', 'D', 10 ),
    ( 'Deci', 'd', .1 ),
    ( 'Centi', 'c', .01 ),
    ( 'Milli', 'm', .001 )
) )

def prefixed_string( prefix, string ): return prefix[0] + string[0].lower() + string[1:]

class UnitMetaClass( BaseMetaClass ):

    def __init__( cls, name, bases, attrs ):

        '''Registers a new unit class with its Dimension in addition to creating it.
        
            This will also create any prefixed classes and assign them to the Unit's Dimension.
        '''

        if not cls.is_virtual:

            cls.Dimension.register( cls )

            if cls.prefixed:

                d = dict( cls.__dict__ )
                d['prefixed'] = False

                for prefix in prefixes:

                    prefix_unit_cls = cls.__metaclass__( prefixed_string( prefix, cls.__name__ ), cls.__bases__, d )

                    # @note: Prefixed classes just append a prefixed Unitless to the end of their numerators.  Unitless items are
                    #   left alone.

                    if cls.__name__ != 'Unitless':

                        # If the unit is simple, then the auto-generated numerator must be overridden.
                        if prefix_unit_cls.numerator == (prefix_unit_cls,): prefix_unit_cls.numerator = (cls,)

                        prefix_unit_cls.numerator = tuple(
                            list( prefix_unit_cls.numerator ) + [ getattr( Dimensionless, prefixed_string( prefix, 'Unitless' ) ) ]
                        )

                    prefix_unit_cls.prefixed    = False
                    prefix_unit_cls.string      = prefix[1] + prefix_unit_cls.string

                    setattr( cls, prefix_unit_cls.__name__, prefix[2] )
                    cls.Dimension.register( prefix_unit_cls )

    @property
    def d( cls ):

        from . import d
        return d

    def make_cls_mul( cls, other, *args, **kargs ):

        new_cls             = super( UnitMetaClass, cls ).make_cls_mul( other, *args, **kargs )
        new_cls.Dimension   = cls.Dimension * other.Dimension
        return new_cls

    def make_cls_div( cls, other, *args, **kargs ):

        new_cls             = super( UnitMetaClass, cls ).make_cls_div( other, *args, **kargs )
        new_cls.Dimension   = cls.Dimension / other.Dimension
        return new_cls

    def make_cls_rdiv( cls, *args, **kargs ):

        new_cls             = super( UnitMetaClass, cls ).make_cls_rdiv( *args, **kargs )
        new_cls.Dimension   = 1/cls.Dimension
        return new_cls

    def __rmul__( cls, other ): return cls( other )

    def __rdiv__( cls, other ):

        new_cls = super( UnitMetaClass, cls ).__rdiv__( other )
        return new_cls( other )

    def __getattr__( cls, name ):

        '''Return the prefixed conversion factors.'''

        if name == cls.__name__: return 1
        raise AttributeError

class Unit( BaseClass ):

    '''The base unit class.'''

    __metaclass__ = UnitMetaClass

    def __init__( self, value ):

        if isinstance( value, Unit ):
            if not self.Dimension == value.Dimension:
                raise DimError( 'Cannot convert between dimensions {0} and {1}.'.format( self.Dimension, value.Dimension ) )
            value = getattr( value.dimension, self.__class__.__name__ ).value
        self.value = value

    def __repr__( self ): return '{0} {1}'.format( self.value, self.string )
    def __str__( self ): return self.__repr__()

    def __neg__( self ): return self.__class__( -self.value )
    def __pos__( self ): return self
    def __abs__( self ): return self.__class__( abs( self.value ) )

    def __add__( self, other ):

        if not isinstance( other, Unit ): raise TypeError( 'Unit-ed objects may only be added to other Unit-ed objects.' )
        if not self.__class__ == other.__class__: other = self.__class__( other )
        return self.__class__( self.value + other.value )

    def __sub__( self, other ):

        if not isinstance( other, Unit ): raise TypeError( 'Unit-ed objects may only be added to other Unit-ed objects.' )
        if not self.__class__ == other.__class__: other = self.__class__( other )
        return self.__class__( self.value - other.value )

    def __mul__( self, other ):

        if isinstance( other, UnitMetaClass ):  return ( self.__class__ * other )( self.value )
        if not isinstance( other, Unit ):       return self.__class__( self.value * other )

        if not self.__class__ == other.__class__: other = self.__class__( other )

        new_cls = self.__class__ * other.__class__
        value   = self.value * other.value

        return new_cls( value )

    def __rmul__( self, other ): return self.__class__( self.value * other )

    def __div__( self, other ):

        if isinstance( other, UnitMetaClass ):  return ( self.__class__ / other )( self.value )
        if not isinstance( other, Unit ):       return self.__class__( self.value/other )

        if not self.__class__ == other.__class__: other = self.__class__( other )

        new_cls = self.__class__ / other.__class__
        value   = self.value / other.value

        return new_cls( value )

    def __rdiv__( self, other ): return (other/self.value) / self.__class__

    def __complex__( self ):    return complex( self.value )
    def __int__( self ):        return int( self.value )
    def __long__( self ):       return long( self.value )
    def __float__( self ):      return float( self.value )

    def __cmp__( self, other ):

        if not isinstance( other, Unit ):           raise TypeError( 'Cannot compare unit and non-unit.' )

        if not self.__class__ == other.__class__:   other = self.__class__( other )

        if self.value < other.value:    return -1
        elif self.value == other.value: return 0
        elif self.value > other.value:  return 1

    Dimension   = Dimensionless
    prefixed    = True

    @classproperty
    def string( cls ):

        s = ''
        if cls.numerator:
            s += ' * '.join( map( lambda n: n.string, cls.numerator ) )
            if cls.denominator: s += ' '
        if cls.denominator:
            s += '/'
            if len( cls.denominator ) > 1: s += '('
            s += ' ' + ' * '.join( map( lambda d: d.string, cls.denominator ) ) + ' '
            if len( cls.denominator ) > 1: s += ')'

        return s

    @property
    def dimension( self ): return self.Dimension( self )

    @classproperty
    def is_virtual( cls ):

        if cls.__name__ == 'Unit':  return True
        else:                       return False

class Unitless( Unit ): string = 'unit'
