"""IDD Models and Data Analysis Package."""

__version__ = "0.1.0"
__author__ = "Bobby Reiner"
__email__ = "bcreiner@uw.edu"

# Import main modules for easy access
from . import models
from . import visualization
from . import ui
from . import utils
from . import apps

# Configure matplotlib defaults
from .visualization.colors import configure_matplotlib_defaults
configure_matplotlib_defaults()

__all__ = ['models', 'visualization', 'ui', 'utils', 'apps']