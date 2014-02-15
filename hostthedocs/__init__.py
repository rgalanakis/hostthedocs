from flask import Flask, jsonify, render_template, request

from .filekeeper import delete_files, parse_docfiles, unpack_project
from . import getconfig

app = Flask(__name__)

@app.route('/hmfd', methods=['POST', 'DELETE'])
def hmfd():
    success = False
    if request.method == 'POST':
        unpack_project(request.files.values()[0].stream, request.form, getconfig.docfiles_dir)
        success = True
    else:
        assert request.method == 'DELETE'
        delete_files(
            request.form['name'],
            request.form['version'],
            getconfig.docfiles_dir,
            request.form.get('entire_project'))
    return jsonify({'success': success})


@app.route('/')
def home():
    projects = parse_docfiles(getconfig.docfiles_dir, getconfig.docfiles_link_root)
    return render_template('index.html', projects=projects, **getconfig.renderables)
