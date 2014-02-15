"""Module for loading a user config."""

import os

try:
    import htdconf
except ImportError:
    htdconf = None


def get(attr, default):
    result = os.getenv('HTD_' + attr.upper())
    if result is None:
        result = getattr(htdconf, attr, None)
    if result is None:
        result = default
    return result


docfiles_dir = get('docfiles_dir', os.path.join(os.getcwd(), 'static', 'docfiles'))
#assert os.path.isdir(docfiles_dir), 'Must exist: %s' % docfiles_dir
docfiles_link_root = get('docfiles_link_root', 'static/docfiles')

# If defined, is placed in the footer.
# if not defined, don't display copyright.
# Probably you want to use something
# like 'Copyright &copy; My Company 2014'
copyright = get('copyright', '')

# Title of the homepage.
title = get('title', 'Host the Docs Home')

# Message in jumbotron.
welcome = get('welcome', 'Welcome to Host the Docs!')
# Message below jumbotron
intro = get('intro', """
Browse all available documentation below.
To add your docs, see
<a href="https://github.com/rgalanakis/hostthedocs#uploading-your-docs">these instructions</a>.""")

server = get('server', '127.0.0.1')
port = get('port', 5000)
debug = get('debug', None)

all = dict((k, v) for (k, v) in globals().items() if isinstance(v, basestring))
