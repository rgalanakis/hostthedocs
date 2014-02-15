"""Run this script to test your Host the Docs server.
It will POST a zip file.
You can also pass in your own settings to test more.
Requires the requests library.
"""

import argparse
import requests

from tests.test_filekeeper import ZIPFILE
from hostthedocs import getconfig as cfg


def parse():
    p = argparse.ArgumentParser()
    p.add_argument('-n', '--name', default='Test Project')
    p.add_argument('-d', '--description', default='Project description.')
    p.add_argument('-v', '--version', default='7.8.9')
    p.add_argument('-z', '--zippath', default=ZIPFILE)
    p.add_argument('-D', '--delete', action='store_true')
    p.add_argument('-A', '--deleteall', action='store_true')
    return p.parse_args()


def _post(address, metadata, opts):
    print 'POSTing to', address
    print '  metadata:', metadata
    print '  zippath:', opts.zippath
    got = requests.post(
        address,
        data=metadata,
        files={"archive": ("test.zip", open(opts.zippath, 'rb'))})
    return got


def _delete(address, metadata, opts):
    address += '?name=%s&version=%s' % (
        metadata['name'], metadata['version'])
    if opts.deleteall:
        address += '&entire_project=True'
    print 'DELETING to', address
    got = requests.delete(address)
    return got


def main():
    opts = parse()
    address = 'http://%s:%s/hmfd' % (cfg.server, cfg.port)
    metadata = {
        'name': opts.name,
        'version': opts.version,
        'description': opts.description}
    if opts.delete or opts.deleteall:
        got = _delete(address, metadata, opts)
    else:
        got = _post(address, metadata, opts)
    print 'Recieved:', got.status_code, got.content.replace('\n', '')


if __name__ == '__main__':
    main()
