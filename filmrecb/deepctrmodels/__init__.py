# __all__ = ["Deepfm"]

from . import layers
from . import models
from .utils import check_version
# from .deepfm import Deepfm

__version__ = '0.2.9'
check_version(__version__)