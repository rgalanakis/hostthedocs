import os
import shutil
import zipfile

DEFAULT_PROJECT_DESCRIPTION = '<No project description>'


def _tryint(s):
    try:
        return int(s)
    except ValueError:
        return s


def sort_by_version(d):
    v = d['version']
    intparts = [_tryint(s) for s in v.split('.')]
    return intparts


def _get_proj_dict(docfiles_dir, proj_dir, link_root):
    join = lambda *a: os.path.join(docfiles_dir, proj_dir, *a)
    allpaths = os.listdir(join())
    versions = [
        dict(version=p, link='%s/%s/%s/index.html' % (link_root, proj_dir, p))
        for p in allpaths if os.path.isdir(join(p))
    ]
    versions.sort(key=sort_by_version)
    descr = DEFAULT_PROJECT_DESCRIPTION
    if 'description.txt' in allpaths:
        dpath = join('description.txt')
        with open(dpath) as f:
            descr = f.read().strip()
    return {'name': proj_dir, 'versions': versions, 'description': descr}


def parse_docfiles(docfiles_dir, link_root):
    if not os.path.exists(docfiles_dir):
        return {}

    result = [_get_proj_dict(docfiles_dir, f, link_root)
              for f in sorted(os.listdir(docfiles_dir), key=str.lower)]

    return result


def unpack_project(zippath, proj_metadata, docfiles_dir):
    projdir = os.path.join(docfiles_dir, proj_metadata['name'])
    verdir = os.path.join(projdir, proj_metadata['version'])

    if not os.path.isdir(verdir):
        os.makedirs(verdir)

    descrpath = os.path.join(projdir, 'description.txt')
    with open(descrpath, 'w') as f:
        f.write(proj_metadata.get('description', DEFAULT_PROJECT_DESCRIPTION))

    zf = zipfile.ZipFile(zippath)
    # This is insecure, we are only accepting things from trusted sources.
    zf.extractall(verdir)


def valid_name(s):
    """See readme for what's valid.

    :type s: str
    """
    for c in s:
        if not (c.isalnum() or c in ' -_'):
            return False
    return True


def valid_version(s):
    """See readme for what's valid.

    :type s: str
    """
    for c in s:
        if not (c.isalnum() or c == '.'):
            return False
    return True


def delete_files(name, version, docfiles_dir, entire_project=False):
    remove = os.path.join(docfiles_dir, name)
    if not entire_project:
        remove = os.path.join(remove, version)
    if os.path.exists(remove):
        shutil.rmtree(remove)


def _has_latest(versions):
    return any(v['version'] == 'latest' for v in versions)


def insert_link_to_latest(projects, template):
    """For each project in ``projects``,
    will append a "latest" version that links to a certain location
    (should not be to static files).
    Will not add a "latest" version if it already exists.

    :param projects: Project dicts to mutate.
    :param template: String to turn into a link.
      Should have a ``%(project)s`` that will be replaced with the project name.
    """
    for p in projects:
        if _has_latest(p['versions']):
            continue
        link = template % dict(project=p['name'])
        p['versions'].append(dict(version='latest', link=link))
