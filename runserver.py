import os
os.environ['HTD_COPYRIGHT'] = 'Copyright &copy; Rob Galanakis'
os.environ['HTD_DEBUG'] = 'True'

from hostthedocs import app, getconfig

if __name__ == '__main__':
    getconfig.serve(app)
