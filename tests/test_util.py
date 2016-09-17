import tempfile
import unittest

from werkzeug.test import EnvironBuilder
from werkzeug.wrappers import Request

from hostthedocs import util


class UtilityTests(unittest.TestCase):
    def test_extracting_filestream_from_request(self):
        # GIVEN a file to upload.
        with tempfile.NamedTemporaryFile('w+') as f:
            # GIVEN the file's contents.
            content = 'foo'
            f.write(content)

            # GIVEN a POST request containing the file to upload.
            builder = EnvironBuilder(method='POST', data={'file': f})
            request = Request(builder.get_environ())

            # WHEN we process the request.
            filestream = util.get_filestream_from_request(request)

            # THEN the file-stream should correspond to the provided file.
            self.assertEqual(content, filestream.read())
