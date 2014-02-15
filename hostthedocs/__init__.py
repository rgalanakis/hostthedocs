from flask import Flask, render_template
import os

from .filekeeper import parse_docfiles, unpack_project

DOCFILES_ENVVAR = 'HTD_DOCFILES_DIR'

app = Flask(__name__)


def docfiles_dir():
    try:
        return os.environ[DOCFILES_ENVVAR]
    except KeyError:
        raise RuntimeError(
            '%s needs to be set to the docfiles directory to use the server.' %
            DOCFILES_ENVVAR)


@app.route('/hmfd')
def hmfd():
    pass


@app.route('/')
def home():
    proj_data = parse_docfiles(docfiles_dir())
    return render_template(
        'index.html',
        title='Welcome to Host the Docs',
        proj_data=proj_data)
