import mock
import unittest

import hostthedocs


class HostTheDocsTests(unittest.TestCase):

    def setUp(self):
        hostthedocs.app.config['TESTING'] = True
        self.app = hostthedocs.app.test_client()

    def test_readonly(self):
        with mock.patch('hostthedocs.getconfig.readonly', True):
            for meth in [self.app.post, self.app.delete]:
                self.assertEqual(meth('/hmfd').status_code, 403)
