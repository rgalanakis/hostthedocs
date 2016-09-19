"""
Provides utility methods.
"""


def get_filestream_from_request(request):
    """
    Extract the file-stream of the first file object from
    a :class:`werkzeug.wrappers.BaseRequest`.

    :param werkzeug.wrappers.BaseRequest request: the `werkzeug` request
    :return: the file-stream of the first file within the request
    :raises ValueError: if no files exist within the request
    """
    try:
        return list(request.files.values())[0].stream
    except IndexError:
        raise ValueError('Request does not contain uploaded file')
