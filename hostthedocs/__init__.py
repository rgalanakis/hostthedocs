from flask import abort, Flask, jsonify, render_template, request

from .filekeeper import delete_files, parse_docfiles, unpack_project
from . import getconfig

app = Flask(__name__)

@app.route('/hmfd', methods=['POST', 'DELETE'])
def hmfd():
    if getconfig.readonly:
        return abort(403)
    if request.method == 'POST':
        unpack_project(request.files.values()[0].stream, request.form, getconfig.docfiles_dir)
    else:
        assert request.method == 'DELETE'
        delete_files(
            request.args['name'],
            request.args.get('version'),
            getconfig.docfiles_dir,
            request.args.get('entire_project'))
    return jsonify({'success': True})


@app.route('/')
def home():
    projects = parse_docfiles(getconfig.docfiles_dir, getconfig.docfiles_link_root)
    return render_template('index.html', projects=projects, **getconfig.renderables)
