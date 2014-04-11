import mock
import unittest
import six.moves.urllib.parse as urlparse

import hostthedocs
from tests import DOCFILESDIR


class Base(unittest.TestCase):
    def setUp(self):
        hostthedocs.app.config['TESTING'] = True
        self.app = hostthedocs.app.test_client()


class HomeTests(Base):
    def test_finds_all(self):
        pass

    def test_inserts_latest(self):
        pass


class HMFDTests(Base):

    def test_readonly(self):
        with mock.patch('hostthedocs.getconfig.readonly', True):
            for meth in [self.app.post, self.app.delete]:
                self.assertEqual(meth('/hmfd').status_code, 403)

    def test_missing_zip(self):
        resp = self.app.post('/hmfd')
        self.assertEqual(400, resp.status_code)

    def test_delete(self):
        pass

    def test_add_new(self):
        pass


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

    def test_missing_returns_404(self):
        pass


class ConfigTests(unittest.TestCase):

    def setUp(self):
        self.gev = hostthedocs.getconfig.serve_gevent
        self.flsk = hostthedocs.getconfig.serve_flask

    def assert_wsgiserver_calc(
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
        self.assert_wsgiserver_calc(self.flsk)

    def test_uses_gevent_if_gevent_available(self):
        self.assert_wsgiserver_calc(self.gev, gevent_module=1)

    def test_uses_flask_if_flask(self):
        self.assert_wsgiserver_calc(self.flsk, wsgi_server_from_conf='flask')

    def test_uses_gevent_if_gevent(self):
        self.assert_wsgiserver_calc(self.gev, wsgi_server_from_conf='gevent')

    def test_uses_serve_if_provided(self):
        serve = lambda: None
        self.assert_wsgiserver_calc(serve, serve)

    def test_uses_flask_if_debug(self):
        self.assert_wsgiserver_calc(self.flsk, debug_from_conf=True)
