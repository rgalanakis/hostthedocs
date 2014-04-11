import os
import sys

try:
    import unittest2
    sys.modules['unittest'] = unittest2
except ImportError:
    pass

THISDIR = os.path.dirname(__file__)
DOCFILESDIR = os.path.join(THISDIR, 'docfiles')
