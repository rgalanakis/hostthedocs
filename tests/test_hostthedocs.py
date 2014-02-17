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


class ConfigTests(unittest.TestCase):

    def setUp(self):
        self.gev = hostthedocs.getconfig.serve_gevent
        self.flsk = hostthedocs.getconfig.serve_flask

    def assertCalc(
            self,
            shouldbe,
            serve_from_conf=None,
            gevent_module=None,
            debug_from_conf=None,
            wsgi_server_from_conf=None):
        self.assertIs(
            shouldbe,
            hostthedocs.getconfig.calc_serve(
                serve_from_conf, gevent_module,
                debug_from_conf, wsgi_server_from_conf))

    def test_uses_flask_if_gevent_none(self):
        self.assertCalc(self.flsk)

    def test_uses_gevent_if_gevent_available(self):
        self.assertCalc(self.gev, gevent_module=1)

    def test_uses_flask_if_flask(self):
        self.assertCalc(self.flsk, wsgi_server_from_conf='flask')

    def test_uses_gevent_if_gevent(self):
        self.assertCalc(self.gev, wsgi_server_from_conf='gevent')

    def test_uses_serve_if_provided(self):
        serve = lambda: None
        self.assertCalc(serve, serve)

    def test_uses_flask_if_debug(self):
        self.assertCalc(self.flsk, debug_from_conf=True)
