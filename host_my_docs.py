"""Run this script to test your Host the Docs server.
It will POST a zip file.
You can also pass in your own settings to test more.
Requires the requests library.

Used also to generate and upload Host the Docs documentation for its demo page.
"""

import argparse
import logging
import os
import requests
import sys
import time
import zipfile

from tests.test_filekeeper import ZIPFILE
from hostthedocs import getconfig as cfg

L = logging.getLogger('host_my_docs')

def parse():
    p = argparse.ArgumentParser()
    p.add_argument('-n', '--name', default='Test Project')
    p.add_argument('-d', '--description', default='Project description.')
    p.add_argument('-v', '--version', default='7.8.9')
    p.add_argument('-z', '--zippath', default=ZIPFILE)
    p.add_argument(
        '--hostthedocs', action='store_true',
        help='Generates docs for Host the Docs. Ignore all other options if used.')
    p.add_argument(
        '-H', '--host',
        default='%s:%s' % (cfg.host, cfg.port),
        help='Host to use.')
    p.add_argument('-D', '--delete', action='store_true')
    p.add_argument('-A', '--deleteall', action='store_true')
    return p.parse_args()


def _makeaddr(host):
    return 'http://%s/hmfd' % host.rstrip('/')


def _unlink(path):
    try:
        os.unlink(path)
    except WindowsError:
        time.sleep(.5)
        os.unlink(path)


def post(host, metadata, zippath):
    address = _makeaddr(host)
    L.info('POSTing to %s\n  metadata: %s\n  zippath: %s', address, metadata, zippath)
    got = requests.post(
        address,
        data=metadata,
        files={"archive": ("test.zip", open(zippath, 'rb'))})
    return got


def delete(host, metadata, deleteall=False):
    address = _makeaddr(host)
    address += '?name=%s&version=%s' % (
        metadata['name'], metadata['version'])
    if deleteall:
        address += '&entire_project=True'
    L.info('DELETING to %s', address)
    got = requests.delete(address)
    return got


def generate_htd_docs():
    from docutils.core import publish_string
    with open('README.rst') as f:
        html = publish_string(f.read(),writer_name='html')
    with open('index.html', 'w') as f:
        f.write(html)
    zippath = 'docstemp.zip'
    z = zipfile.ZipFile(zippath, 'w')
    z.write('index.html')
    z.close()
    _unlink('index.html')

    metadata = {
        'name': 'Host the Docs',
        'version': 'latest',
        'description': 'Makes documentation hosting easy.'}
    host = 'tech-artists.org:5003'

    try:
        resp = post(host, metadata, zippath)
    finally:
        _unlink(zippath)

    if resp.status_code != 200:
        raise RuntimeError(repr(resp))


def main():
    opts = parse()
    if opts.hostthedocs:
        generate_htd_docs()
        sys.exit(0)

    metadata = {
        'name': opts.name,
        'version': opts.version,
        'description': opts.description}
    if opts.delete or opts.deleteall:
        got = delete(opts.host, metadata, opts.deleteall)
    else:
        got = post(opts.host, metadata, opts.zippath)
    L.info('Recieved: %s: %s', got.status_code, got.content.replace('\n', ''))
    sys.exit(0 if got.status_code == 200 else got.status_code)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
