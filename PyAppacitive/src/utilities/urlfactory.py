__author__ = 'sushant'

import settings

base_url = settings.api_base_url


def object_create_url(type):
    return '{0}/object/{1}'.format(base_url, type)

user_urls = {
    "create":"user/create",
}

object_urls = {
    "create": object_create_url
}




