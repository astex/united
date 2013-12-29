from united.util import make_num_denom_dict

from .basic import Length, Time, Mass
from .complicated import Area, Velocity, Frequency

d = make_num_denom_dict( [ Length, Time, Mass, Area, Velocity, Frequency ] )
