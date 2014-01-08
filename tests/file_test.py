__author__ = 'sathley'

from pyappacitive import AppacitiveFile


def get_file_upload_url_test():
    file_id, url = AppacitiveFile.get_upload_url('image/jpeg', 'foto.jpeg')
    assert url is not None
    assert id is not None


def get_download_url_test():
    url = AppacitiveFile.get_download_url('random_file_id')
    assert url is not None


def delete_file_test():
    AppacitiveFile.delete_file('random_file_id')
