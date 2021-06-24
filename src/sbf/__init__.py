__version__ = '0.1'

try:
    __SBF_SETUP__
except NameError:
    __SBF_SETUP__ = False

if not __ARTPOP_SETUP__:
    from .measure import measure
