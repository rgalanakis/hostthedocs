"""
Provides utility methods.
"""

import os
import logging
import zipfile
import tarfile


logger = logging.getLogger()

def file_from_request(request):
    """
    Get the uploaded file from a POST request, which should contain exactly one file.

    :param werkzeug.wrappers.BaseRequest request: The POST request.
    :return: The instantiated UploadedFile.
    :raises ValueError: if no files exist within the request.
    """
    uploaded_files = list(request.files.values())
    if len(uploaded_files) > 1:
        logger.warning(
            'Only one file can be uploaded for each request. '
            'Only the first file will be used.'
        )
    elif len(uploaded_files) == 0:
        raise ValueError('Request does not contain uploaded file')

    return uploaded_files[0]

class FileExpander(object):
    """
    Manager for exanding compressed project files.

    It automatically detects the compression method and allocates
    the right handler.

    Currently the supported methods are:
    - zip
    - tar
    """

    ZIP_EXTENSIONS = ('.zip', )
    TAR_EXTENSIONS = ('.tar', '.tgz', '.tar.gz', '.tar.bz2')

    def __init__(self, uploaded_file):
        self._file = uploaded_file
        self._handle = None

    @classmethod
    def detect_compression_method(cls, filename):
        """
        Attempt to detect the compression method from the filename extension.

        :param str extension: The file extension.
        :return: The compression method ('zip' or 'tar').
        :raises ValueError: If fails to detect the compression method.
        """
        if any(filename.endswith(ext) for ext in cls.ZIP_EXTENSIONS):
            return 'zip'
        if any(filename.endswith(ext) for ext in cls.TAR_EXTENSIONS):
            return 'tar'

        raise ValueError('Unknown compression method for %s' % filename)

    def __enter__(self):
        method = self.detect_compression_method(self._file.filename)
        if method == 'zip':
            self._handle = zipfile.ZipFile(self._file)
        elif method == 'tar':
            self._handle = tarfile.open(fileobj=self._file, mode='r:*')
        else:
            raise ValueError('Unsupported method %s' % method)

        return self._handle

    def __exit__(self, exc_type, exc_value, traceback):
        self._handle.close()
