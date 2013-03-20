from .paths import *
from .basic import *
from .apps import *
from .locale import *
from .auth import *
from .context import *
from .middleware import *
from .static import *
from .logging import *
from .contrib import *
from .custom import *


# Load localsettings, if they exist
try:
    from ..localsettings import *
except ImportError:
    pass
