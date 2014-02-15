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
    return p.parse_args()

def main():
    opts = parse()
    address = 'http://%s:%s/hmfd' % (cfg.server, cfg.port)
    metadata = {
        'name': opts.name,
        'version': opts.version,
        'description': opts.description}
    print 'POSTing to', address
    print '  metadata:', metadata
    print '  zippath:', opts.zippath
    got = requests.post(
        address,
        data=metadata,
        files={"archive": ("test.zip", open(opts.zippath, 'rb'))})
    print 'Recieved:', got.status_code, got.content.replace('\n', '')

if __name__ == '__main__':
    main()
