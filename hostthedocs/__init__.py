from flask import Flask, jsonify, render_template, request
import json

from .filekeeper import parse_docfiles, unpack_project
from . import getconfig

app = Flask(__name__)

@app.route('/hmfd', methods=['POST'])
def hmfd():
    unpack_project(request.files.values()[0].stream, request.form, getconfig.docfiles_dir)
    return jsonify({'success': True})


@app.route('/')
def home():
    projects = parse_docfiles(getconfig.docfiles_dir, getconfig.docfiles_link_root)
    print projects
    return render_template('index.html', projects=projects, **getconfig.all)
