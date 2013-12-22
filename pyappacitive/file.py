__author__ = 'sathley'

from utilities import urlfactory, http
from error import ValidationError
from response import AppacitiveResponse


class AppacitiveFile(object):
    def __init__(self):
        pass

    @staticmethod
    def get_upload_url(content_type, filename=None, expires=None):

        if content_type is None:
            raise ValidationError('content-type is mandatory for file upload.')

        url = urlfactory.file_urls['get_upload_url'](content_type)

        if filename is not None:
            url += '&filename='+filename
        if expires is not None:
            url += '&expires='+expires

        headers = urlfactory.get_headers()

        api_response = http.get(url, headers)
        response = AppacitiveResponse(api_response['status'])
        if response.status.code == '200':
            response.id = api_response['id']
            response.url = api_response['url']
        return response

    @staticmethod
    def get_download_url(file_id, expires=None):

        if file_id is None:
            raise ValidationError('file id is mandatory for file download.')

        url = urlfactory.file_urls['get_download_url'](file_id)

        if expires is not None:
            url += '?expires='+expires

        headers = urlfactory.get_headers()

        api_response = http.get(url, headers)
        response = AppacitiveResponse(api_response['status'])
        if response.status.code == '200':
            response.url = api_response['uri']
        return response

    @staticmethod
    def delete_file(file_id):

        if file_id is None:
            raise ValidationError('file id is mandatory for file delete.')

        url = urlfactory.file_urls['file_delete'](file_id)

        headers = urlfactory.get_headers()

        api_response = http.delete(url, headers)
        return AppacitiveResponse(api_response['status'])


