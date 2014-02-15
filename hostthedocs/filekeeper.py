import os
import zipfile

DEFAULT_PROJECT_DESCRIPTION = '<No project description>'


def _get_proj_dict(root, proj):
    join = lambda *a: os.path.join(root, proj, *a)
    allpaths = os.listdir(join())
    dirs = [p for p in allpaths if os.path.isdir(join(p))]
    descr = DEFAULT_PROJECT_DESCRIPTION
    if 'description.txt' in allpaths:
        dpath = join('description.txt')
        with open(dpath) as f:
            descr = f.read().strip()
    return {'versions': dirs, 'description': descr}


def parse_docfiles(docfiles_dir):
    result = dict(
        (f, _get_proj_dict(docfiles_dir, f))
        for f in os.listdir(docfiles_dir))

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
