__author__ = 'sathley'

from user import AppacitiveUser
from utilities import urlfactory, http, appcontext
from error import ValidationError


class FileHelper(object):
    def __init__(self):
        pass

    @staticmethod
    def get_upload_url(content_type, filename=None, expires=None):

        if content_type is None:
            raise ValidationError('content-type is mandatory for file upload.')

        url = urlfactory.file_urls['get_upload_url'](content_type)

        if filename is not None:
            url+'&filename='+filename
        if expires is not None:
            url+'&expires='+expires

        headers = urlfactory.get_headers()

        response = http.get(url, headers)
        if response['status']['code'] != '200':
            return None

        return response['id'], response['url']

    @staticmethod
    def get_download_url(file_id, expires=None):

        if file_id is None:
            raise ValidationError('file id is mandatory for file download.')

        url = urlfactory.file_urls['get_download_url'](file_id)

        if expires is not None:
            url+'?expires='+expires

        headers = urlfactory.get_headers()

        response = http.get(url, headers)
        if response['status']['code'] != '200':
            return None

        return response['uri']

    @staticmethod
    def delete_file(file_id):

        if file_id is None:
            raise ValidationError('file id is mandatory for file delete.')

        url = urlfactory.file_urls['file_delete'](file_id)

        headers = urlfactory.get_headers()

        response = http.delete(url, headers)
        if response['status']['code'] != '200':
            return None


