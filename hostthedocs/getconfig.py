"""Module for loading a user config.
See conf.py for more info.
"""

import os

try:
    import conf
except ImportError:
    conf = None


def get(attr, default):
    result = os.getenv('HTD_' + attr.upper())
    if result is None:
        result = getattr(conf, attr, None)
    if result is None:
        result = default
    return result


docfiles_dir = get('docfiles_dir', 'hostthedocs/static/docfiles')
#assert os.path.isdir(docfiles_dir), 'Must exist: %s' % docfiles_dir
docfiles_link_root = get('docfiles_link_root', 'static/docfiles')

copyright = get('copyright', '')

title = get('title', 'Host the Docs Home')

welcome = get('welcome', 'Welcome to Host the Docs!')

intro = get('intro', """
Browse all available documentation below.
To add your docs, see
<a href="https://github.com/rgalanakis/hostthedocs#uploading-your-docs">these instructions</a>.""")

server = get('server', '127.0.0.1')
port = get('port', 5000)
debug = bool(get('debug', None))

# CSS theme options


renderables = dict((k, v) for (k, v) in globals().items() if isinstance(v, basestring))


def serve_gevent(app):
    from gevent.wsgi import WSGIServer

    http_server = WSGIServer((server, port), app)
    http_server.serve_forever()


def serve_flask(app):
    app.run(server, port, debug)


wsgi_server = get('wsgi_server', None)

serve = None
if wsgi_server:
    serve = {'gevent': serve_gevent,
             'flask': serve_flask}[wsgi_server]
if serve is None:
    serve = get('serve', None)
if serve is None:
    serve = serve_flask
