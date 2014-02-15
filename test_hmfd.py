name = 'Test Project'
description = 'Fucking test project'
version = '2.5.2'
from tests.test_filekeeper import ZIPFILE

if __name__ == '__main__':
    from hostthedocs import getconfig as cfg
    import requests
    fileobj = open(ZIPFILE, 'rb')
    got = requests.post(
        'http://%s:%s/hmfd' % (cfg.server, cfg.port),
        data={'name': name, 'version': version, 'description': description},
        files={"archive": ("test.zip", fileobj)})
    print got.status_code, got.content
