import os

from flask import abort, Flask, jsonify, redirect, render_template, request

from . import getconfig, util
from .filekeeper import delete_files, insert_link_to_latest, parse_docfiles, unpack_project

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = getconfig.max_content_mb * 1024 * 1024


@app.route('/hmfd', methods=['POST', 'DELETE'])
def hmfd():
    if getconfig.readonly:
        return abort(403)

    if request.method == 'POST':
        if not request.files:
            return abort(400, 'Request is missing a zip/tar file.')
        uploaded_file = util.file_from_request(request)
        unpack_project(
            uploaded_file,
            request.form,
            getconfig.docfiles_dir
        )
        uploaded_file.close()
    elif request.method == 'DELETE':
        if getconfig.disable_delete:
            return abort(403)

        delete_files(
            request.args['name'],
            request.args.get('version'),
            getconfig.docfiles_dir,
            request.args.get('entire_project'))
    else:
        abort(405)

    return jsonify({'success': True})


@app.route('/')
def home():
    projects = parse_docfiles(getconfig.docfiles_dir, getconfig.docfiles_link_root)
    insert_link_to_latest(projects, '%(project)s/latest')
    return render_template('index.html', projects=projects, **getconfig.renderables)


@app.route('/<project>/latest/')
def latest_root(project):
    return latest(project, '')


@app.route('/<project>/latest/<path:path>')
def latest(project, path):
    parsed_docfiles = parse_docfiles(getconfig.docfiles_dir, getconfig.docfiles_link_root)
    proj_for_name = dict((p['name'], p) for p in parsed_docfiles)
    if project not in proj_for_name:
        return 'Project %s not found' % project, 404
    latestindex = proj_for_name[project]['versions'][-1]['link']
    if path:
        latestlink = '%s/%s' % (os.path.dirname(latestindex), path)
    else:
        latestlink = latestindex
    return redirect('/' + latestlink)
