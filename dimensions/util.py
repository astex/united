from collections import Counter

from .base import Dimension

def multiply_dims( dim1, dim2 ):

    numerator   = getattr( dim1, 'numerator', (dim1,) ) + getattr( dim2, 'numerator', (dim2,) )
    denominator = getattr( dim1, 'denominator', () ) + getattr( dim2, 'denominator', () )

    numerator, denominator = cancel_numerator_and_denominator( numerator, denominator )

    return find_or_make_dimension( numerator, denominator )

def divide_dims( dim1, dim2 ):

    numerator   = getattr( dim1, 'numerator', (dim1,) ) + getattr( dim2, 'denominator', () )
    denominator = getattr( dim1, 'denominator', () ) + getattr( dim2, 'numerator', (dim2,) )

    numerator, denominator = cancel_numerator_and_denominator( numerator, denominator )

    return find_or_make_dimension( numerator, denominator )

def cancel_numerator_and_denominator( numerator, denominator ):

    numerator   = list( numerator )
    denominator = list( denominator )

    for i, n in enumerate( numerator ):
        for j, d in enumerate( denominator ):
            if d == n:
                numerator[i]    = None
                denominator[j]  = None
                break

    numerator   = tuple(filter( None, numerator ))
    denominator = tuple(filter( None, denominator ))

    return numerator, denominator

def find_or_make_dimension( numerator, denominator ):

    '''Looks for a dimension in complicated and basic.  If none is found, one is created.'''

    import basic, complicated

    for dim in basic.__all__ + complicated.__all__:
        
        dim_numerator   = getattr( dim, 'numerator', (dim,) )
        dim_denominator = getattr( dim, 'denominator', () )

        if Counter( dim_numerator ) == Counter( numerator ) and Counter( dim_denominator ) == Counter( denominator ):
            return dim

    return type( dim1.__name__ + dim2.__name__, (Dimension,), {} )
