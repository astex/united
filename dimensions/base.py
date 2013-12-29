from united.util import BaseMetaClass, BaseClass

class DimensionMetaClass( BaseMetaClass ):

    @property
    def d( cls ):

        from . import d
        return d

class Dimension( BaseClass ):

    __metaclass__ = DimensionMetaClass
