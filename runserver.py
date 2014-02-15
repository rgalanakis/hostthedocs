import os
os.environ['HTD_COPYRIGHT'] = 'Copyright &copy; Rob Galanakis'
os.environ['HTD_DOCFILES_DIR'] = 'hostthedocs/static/docfiles'
os.environ['HTD_DOCFILES_LINK_ROOT'] = 'static/docfiles'

import hostthedocs


if __name__ == '__main__':
    hostthedocs.app.run(debug=True)
