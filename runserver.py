import os

import hostthedocs

os.environ[hostthedocs.DOCFILES_ENVVAR] = '../docfiles'


if __name__ == '__main__':
    hostthedocs.app.run(debug=True)
