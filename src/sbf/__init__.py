__version__ = '0.1'

try:
    __SBF_SETUP__
except NameError:
    __SBF_SETUP__ = False

if not __SBF_SETUP__:
    from .masking import elliptical_mask, make_mask
    from .measure import measure
    from . import masking
    from . import utils

