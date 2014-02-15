from flask import Flask, render_template

from .filekeeper import parse_docfiles, unpack_project
from . import getconfig

app = Flask(__name__)

@app.route('/hmfd')
def hmfd():
    pass


@app.route('/')
def home():
    projects = parse_docfiles(getconfig.docfiles_dir, getconfig.docfiles_link_root)
    print projects
    return render_template('index.html', projects=projects, **getconfig.all)
