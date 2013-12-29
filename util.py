def make_num_denom_dict( l ):

    d = dict()

    for cls in l:
        if cls.numerator in d:
            d[cls.numerator][cls.denominator] = cls
        else:
            d[cls.numerator] = dict()
            d[cls.numerator][cls.denominator] = cls

    return d

class classproperty( object ):

    '''A decorator similar to properties, but for class methods.'''

    def __init__( self, getter ):           self.getter = getter
    def __get__( self, obj, cls ):          return self.getter( cls )

def cancel_out( numerator, denominator ):

    numerator   = list( numerator )
    denominator = list( denominator )

    for i,n in enumerate( numerator ):
        for j,d in enumerate( denominator ):
            if n == d:
                numerator[i] = None
                denominator[j] = None
                break

    numerator   = tuple(filter( None, numerator ))
    denominator = tuple(filter( None, denominator ))

    return numerator, denominator

class BaseMetaClass( type ):

    def __repr__( cls ): return '<class \'{0}\'>'.format( cls.__name__ )

    def __mul__( cls, other ):

        if not cls.__metaclass__ == getattr( other, '__metaclass__' ):
            raise TypeError( 'Multiplication of classes {0} and {1} not supported.'.format( cls, other ) )

        numerator   = cls.numerator + other.numerator
        denominator = cls.denominator + other.denominator

        numerator, denominator = cancel_out( numerator, denominator )

        try:
            return cls.find_cls( numerator, denominator )
        except:
            return cls.make_cls_mul( other, numerator, denominator )

    def __div__( cls, other ):

        if not cls.__metaclass__ == other.__metaclass__:
            raise TypeError( 'Division of classes {0} and {1} not supported.'.format( cls, other ) )

        numerator   = cls.numerator + other.denominator
        denominator = cls.denominator + other.numerator

        numerator, denominator = cancel_out( numerator, denominator )

        try:    return cls.find_cls( numerator, denominator )
        except: return cls.make_cls_div( other, numerator, denominator )

    def __rdiv__( cls, other ):

        '''Builds a "PerBaseClass" class.  This ignores the value of other leaving that up to any children that call this.'''

        numerator   = cls.denominator
        denominator = cls.numerator

        try:    return cls.find_cls( numerator, denominator )
        except: return cls.make_cls_rdiv( other, numerator, denominator )

    def find_cls( cls, numerator, denominator ): return cls.d[numerator][denominator]

    def make_cls( cls, other, numerator, denominator, separator='' ):

        new_cls = cls.__metaclass__(
            cls.__name__ + separator + other.__name__,
            tuple( set( cls.__bases__ ) & set( other.__bases__ ) ),
            {}
        )
        new_cls.numerator   = numerator
        new_cls.denominator = denominator

        return new_cls

    def make_cls_rdiv( cls, other, numerator, denominator ):

        new_cls = cls.__metaclass__( 'Per' + cls.__name__, cls.__bases__, {} )
        new_cls.numerator   = numerator
        new_cls.denominator = denominator

        return new_cls

    make_cls_mul = lambda c,o,n,d: c.make_cls( o,n,d )
    make_cls_div = lambda c,o,n,d: c.make_cls( o,n,d,'Per' )

class BaseClass( object ):

    __metaclass__ = BaseMetaClass

    @classproperty
    def numerator( cls ): return (cls,)

    denominator = ()
