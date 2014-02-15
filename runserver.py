import os
os.environ['HTD_COPYRIGHT'] = 'Copyright &copy; Rob Galanakis'
os.environ['HTD_DOCFILES_DIR'] = 'hostthedocs/static/docfiles'
os.environ['HTD_DOCFILES_LINK_ROOT'] = 'static/docfiles'
os.environ['HTD_DEBUG'] = 'True'

from hostthedocs import app, getconfig

if __name__ == '__main__':
    getconfig.serve(app)
