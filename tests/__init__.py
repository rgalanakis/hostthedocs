import os
import sys

import unittest
if not hasattr(unittest.TestCase, 'assertIs'):
    import unittest2
    sys.modules['unittest'] = unittest2


THISDIR = os.path.dirname(__file__)
DOCFILESDIR = os.path.join(THISDIR, 'docfiles')
