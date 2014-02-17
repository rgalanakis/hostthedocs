# You must use None for default values!
# All string values can be set using environment variables (prefixed with 'HTD_'),
# such as 'HTD_DOCFILES_DIR' corresponds to the `docfiles_dir` attribute.

# The directory that will contain the docfiles (stored user documentaiton).
# If you're letting Host the Docs care care of serving, just leave it default
# and let it serve from hostthedocs/static/docfiles.
# Otherwise, point it to a place where your webserver is configured to serve
# static content from.
docfiles_dir = None

# Will be pre-pended to the links of the project files.
# For example, if docfiles_dir is '~/htd/hostthedocs/static/docfiles'
# then docfiles_link_root should be 'static/docfiles'
docfiles_link_root = None

# If defined, is placed in the footer.
# if not defined, don't display copyright.
# Probably you want to use something
# like 'Copyright &copy; My Company 2014'
# Supports HTML.
copyright = None

# Title of the homepage.
title = None

# Message in jumbotron.
welcome = None
# Message below jumbotron.
# Supports HTML.
intro = None

# Host to serve.
host = None
# Port to serve.
port = None
# Whether to serve in debug mode. Only used by Flask.
debug = None

# If True, do not allow anything to be done via /hmfd
readonly = False

# Max upload size in MB (float or int)
# Default to 8, may need to be much larger if you have big docs.
max_content_mb = None

# Name of the WSGI server to use.
# Choose 'flask' or 'gevent'.
# Default is to use 'flask' if debug == True,
#   otherwise 'gevent' if the module is importable,
#   otherwise 'flask'.
# Or use your own webserver by defining a serve funciton (see below).
wsgi_server = None

# If you want to use your own WSGI server,
# provide your own serve function.
# It will be passed the Flask app instance.
serve = None
