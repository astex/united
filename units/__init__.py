from copy import copy

from united.lib.util import make_num_denom_dict
from united.dimensions.exceptions import DimError

from .base import Unitless
from .length import *
from .time import *
from .mass import *
from .complicated import Hertz, SquareMeter
from .exceptions import ConversionError

d = make_num_denom_dict( [ Unitless, Gram, Hertz, SquareMeter ] )

def get_conversion_factor( unit_from, unit_to, unit_set=None, _try_reverse=True ):

    '''Gets a conversion factor from `unit_from` to `unit_to`.
    
        Args:
            unit_from (`UnitMetaClass`) - The unit class being converted from.
            unit_to (`UnitMetaClass`)   - The unit class being converted to.
            unit_set (`set`)            - The set of unit classes on which to try conversion.
            _try_reverse (`bool`)       - Whether or not to try conversion in the alternate direction.
    '''

    if not unit_to.Dimension is unit_from.Dimension: raise DimError

    factor = getattr( unit_to, unit_from.__name__, None )
    if factor:
    
        print( unit_from, unit_to, factor )
        return factor

    if unit_set is None: unit_set = unit_to.Dimension.unit_set
    unit_set = copy( unit_set )
    unit_set = filter( lambda u: hasattr( u, unit_from.__name__ ), unit_set )
    for unit in unit_set:
        try:
            unit_set_without_this_unit = copy( unit_set )
            unit_set_without_this_unit.remove( unit )
            print( unit_set_without_this_unit )
            factor = get_conversion_factor( unit, unit_to, unit_set = unit_set_without_this_unit )
            print( unit_from, unit_to, factor * getattr( unit, unit_from.__name__ ) )
            return factor * getattr( unit, unit_from.__name__ )
        except ConversionError:
            continue

    if _try_reverse: return 1./get_conversion_factor( unit_to, unit_from, _try_reverse=False )

    raise ConversionError( 'Could not find conversion factor between {0} and {1}.'.format( unit_from, unit_to ) )
