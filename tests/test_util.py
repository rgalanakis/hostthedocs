import tempfile
import unittest

from nose.tools import raises
from werkzeug.test import EnvironBuilder
from werkzeug.wrappers import Request

from hostthedocs import util


class UtilityTests(unittest.TestCase):
    def test_extracting_filestream_from_request(self):
        # GIVEN a file to upload.
        with tempfile.NamedTemporaryFile('w+b') as f:
            # GIVEN the file's contents.
            content = b'foo'
            f.write(content)
            f.seek(0)

            # GIVEN a POST request containing the file to upload.
            builder = EnvironBuilder(method='POST', data={'file': f})
            request = Request(builder.get_environ())

            # WHEN we process the request.
            filestream = util.file_from_request(request)

            # THEN the file-stream should correspond to the provided file.
            self.assertEqual(content, filestream.read())

    @raises(ValueError)
    def test_exception_thrown_if_request_contains_no_file(self):
        # GIVEN a request without any files.
        builder = EnvironBuilder(method='POST')
        request = Request(builder.get_environ())

        # EXPECT an exception is thrown when we process the request.
        util.file_from_request(request)
