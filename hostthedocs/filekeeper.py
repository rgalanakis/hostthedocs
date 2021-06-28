import os
import shutil
import zipfile
import tarfile
import natsort
import tempfile

from codecs import open
from . import util


DEFAULT_PROJECT_DESCRIPTION = 'No project description'


def sort_by_version(x):
    # See http://natsort.readthedocs.io/en/stable/examples.html
    return x['version'].replace('.', '~') + 'z'


def _is_valid_doc_version(folder):
    """
    Test if a version folder contains valid documentation.

    A vaersion folder contains documentation if:
    - is a directory
    - contains an `index.html` file
    """
    if not os.path.isdir(folder):
        return False
    if not os.path.exists(os.path.join(folder, 'index.html')):
        return False

    return True


def _get_proj_dict(docfiles_dir, proj_dir, link_root):
    """
    Lookup for the configuration of a project.

    The project configuration is a :class:`dict` with the following data:
    - "name": the name of the project
    - "description": the description of the project
    - "versions": the list of the versions of the documentation. For each
      version, there is a :class:`dict` with:
      - "version": name of the version
      - "link": the relative url of the version

    If no valid versions have been found, returns ``None``.
    """
    def join_with_default_path(*a):
        return os.path.join(docfiles_dir, proj_dir, *a)

    allpaths = os.listdir(join_with_default_path())
    versions = [
        dict(version=p, link='%s/%s/%s/index.html' % (link_root, proj_dir, p))
        for p in allpaths if _is_valid_doc_version(join_with_default_path(p))
    ]
    if len(versions) == 0:
        return None

    versions = natsort.natsorted(versions, key=sort_by_version)
    descr = DEFAULT_PROJECT_DESCRIPTION
    if 'description.txt' in allpaths:
        dpath = join_with_default_path('description.txt')
        with open(dpath, 'r', encoding='utf-8') as f:
            descr = f.read().strip()
    return {'name': proj_dir, 'versions': versions, 'description': descr}


def parse_docfiles(docfiles_dir, link_root):
    """
    Create the list of the projects.

    The list of projects is computed by walking the `docfiles_dir` and
    searching for project paths (<project-name>/<version>/index.html)
    """
    if not os.path.exists(docfiles_dir):
        return {}

    projects = list()
    for folder in natsort.natsorted(os.listdir(docfiles_dir), key=str.lower):
        if not os.path.isdir(os.path.join(docfiles_dir, folder)):
            continue
        project = _get_proj_dict(docfiles_dir, folder, link_root)
        if project is not None:
            projects.append(project)

    return projects


def find_root_dir(compressed_file, file_ext = ".html"):
    """
    Determines the documentation root directory by searching the top-level index file.
    """
    
    if isinstance(compressed_file, zipfile.ZipFile):
        index_files = [member.filename for member in compressed_file.infolist()
                       if not member.is_dir() and os.path.basename(member.filename) == f"index{file_ext}"]
    elif isinstance(compressed_file, tarfile.TarFile):
        index_files = [member.name for member in compressed_file.getmembers()
                       if member.isfile() and os.path.basename(member.name) == f"index{file_ext}"]
    else:
        raise TypeError(f"Invalid archive file type: {type(compressed_file)}")

    if not index_files:
        raise FileNotFoundError("Failed to find root index file!")

    root_index_file = sorted(index_files, key = lambda filename: len(filename.split(os.sep)))[0]

    return os.path.dirname(root_index_file)


def unpack_project(uploaded_file, proj_metadata, docfiles_dir):
    projdir = os.path.join(docfiles_dir, proj_metadata['name'])
    verdir = os.path.join(projdir, proj_metadata['version'])

    if not os.path.isdir(verdir):
        os.makedirs(verdir)

    # Overwrite project description only if a (non empty) new one has been
    # provided
    descr = proj_metadata.get('description', '')
    if len(descr) > 0:
        descrpath = os.path.join(projdir, 'description.txt')
        with open(descrpath, 'w', encoding='utf-8') as f:
            f.write(descr)

    # This is insecure, we are only accepting things from trusted sources.
    with util.FileExpander(uploaded_file) as compressed_file:
        # Determine documentation root dir by finding top-level index file
        root_dir = find_root_dir(compressed_file)

        # Extract full archive to temporary directory
        temp_dir = tempfile.mkdtemp()
        compressed_file.extractall(temp_dir)

        # Then, only move root directory to target dir
        shutil.rmtree(verdir)                                  # clear possibly existing target dir
        shutil.move(os.path.join(temp_dir, root_dir), verdir)  # only move documentation root dir

        if os.path.isdir(temp_dir):  # cleanup temporary directory (if it still exists)
            shutil.rmtree(temp_dir)


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
