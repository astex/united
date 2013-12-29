from united.util import classproperty, BaseMetaClass, BaseClass
from united.dimensions.exceptions import DimError

class UnitMetaClass( BaseMetaClass ):

    @property
    def d( cls ):

        from . import d
        return d

    def make_cls_mul( cls, other, *args, **kargs ):

        new_cls     = super( UnitMetaClass, cls ).make_cls_mul( other, *args, **kargs )
        new_cls.dim = cls.dim * other.dim
        return new_cls

    def make_cls_div( cls, other, *args, **kargs ):

        new_cls     = super( UnitMetaClass, cls ).make_cls_div( other, *args, **kargs )
        new_cls.dim = cls.dim / other.dim
        return new_cls

    def make_cls_rdiv( cls, *args, **kargs ):

        new_cls     = super( UnitMetaClass, cls ).make_cls_rdiv( *args, **kargs )
        new_cls.dim = 1/cls.dim
        return new_cls

    def __rmul__( cls, other ): return cls( other )

    def __rdiv__( cls, other ):

        new_cls = super( UnitMetaClass, cls ).__rdiv__( other )
        return new_cls( other )

class Unit( BaseClass ):

    '''The base unit class.'''

    __metaclass__ = UnitMetaClass

    def __init__( self, value ):

        if isinstance( value, Unit ): value = value.convert_to( self.__class__ ).value
        self.value = value

    def __repr__( self ): return '{0} {1}'.format( self.value, self.string )
    def __str__( self ): return self.__repr__()

    def __add__( self, other ):

        if not isinstance( other, Unit ):   raise TypeError( 'Unit-ed objects may only be added to other Unit-ed objects.' )
        if not self.dim == other.dim:       raise DimError( 'Dimensions don\'t match: {0}, {1}'.format( self.dim, other.dim ) )

        if not self.__class__ == other.__class__: other = other.convert_to( self.__class__ )

        return self.__class__( self.value + other.value )

    def __mul__( self, other ):

        if isinstance( other, UnitMetaClass ):  return ( self.__class__ * other )( self.value )
        if not isinstance( other, Unit ):       return self.__class__( self.value * other )

        if self.dim == other.dim and not self.__class__ == other.__class__:
            other = other.convert_to( self.__class__ )

        new_cls = self.__class__ * other.__class__
        value   = self.value * other.value

        if not new_cls.numerator and not new_cls.denominator:   return value
        else:                                                   return new_cls( value )

    def __rmul__( self, other ): return self.__class__( self.value * other )

    def __div__( self, other ):

        if isinstance( other, UnitMetaClass ):  return ( self.__class__ / other )( self.value )
        if not isinstance( other, Unit ):       return self.__class__( self.value/other )

        if self.dim == other.dim and not self.__class__ == other.__class__:
            other = other.convert_to( self.__class__ )

        new_cls = self.__class__ / other.__class__
        value   = self.value / other.value

        if not new_cls.numerator and not new_cls.denominator:   return value
        else:                                                   return new_cls( value )

    def __rdiv__( self, other ): return (other/self.value) / self.__class__

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
