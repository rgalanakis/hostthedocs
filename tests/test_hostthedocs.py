import mock
import unittest
import urlparse

import hostthedocs
from tests import DOCFILESDIR


class Base(unittest.TestCase):
    def setUp(self):
        hostthedocs.app.config['TESTING'] = True
        self.app = hostthedocs.app.test_client()


class HMFDTests(Base):

    def test_readonly(self):
        with mock.patch('hostthedocs.getconfig.readonly', True):
            for meth in [self.app.post, self.app.delete]:
                self.assertEqual(meth('/hmfd').status_code, 403)

    def test_missing_zip(self):
        resp = self.app.post('/hmfd')
        self.assertEqual(400, resp.status_code)


@mock.patch('hostthedocs.getconfig.docfiles_dir', DOCFILESDIR)
@mock.patch('hostthedocs.getconfig.docfiles_link_root', 'linkroot')
class LatestTests(Base):

    def assert_redirect(self, path, code, location):
        resp = self.app.get(path)
        self.assertEqual(resp.status_code, code)
        gotloc = urlparse.urlsplit(dict(resp.headers)['Location']).path
        self.assertEqual(gotloc, location)

    def test_latest_noslash(self):
        self.assert_redirect('/foo/latest', 301, '/foo/latest/')

    def test_latest_root(self):
            self.assert_redirect('/Project2/latest/', 302, '/linkroot/Project2/2.0.3/index.html')

    def test_latest_certainfile(self):
            self.assert_redirect('/Project2/latest/somefile.html', 302, '/linkroot/Project2/2.0.3/somefile.html')


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
