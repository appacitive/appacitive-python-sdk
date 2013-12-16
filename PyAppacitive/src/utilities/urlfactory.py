__author__ = 'sathley'

import settings

base_url = settings.api_base_url


def get_headers():
    return {
        "Appacitive-Apikey": settings.api_key,
        "Appacitive-Environment": settings.environment,
        "Content-Type": "application/json"
    }


def __object_create_url(type):
    return '{0}/object/{1}'.format(base_url, type)


def __object_delete_url(type, object_id):
    return '{0}/object/{1}/{2}'.format(base_url, type, object_id)

def __object_multidelete_url(type):
    return '{0}/object/{1}/bulkdelete'.format(base_url, type)

def __object_delete_with_connection_url(type, object_id):
    return '{0}/object/{1}/{2}?deleteconnections=true'.format(base_url, type, object_id)


def __object_get_url(type, object_id):
    return '{0}/object/{1}/{2}'.format(base_url, type, object_id)

def __object_multiget_url(type, object_ids):
    return '{0}/object/{1}/multiget/{2}'.format(base_url, type, ','.join(object_ids))


def __object_update_url(type, object_id):
    return '{0}/object/{1}/{2}'.format(base_url, type, object_id)


def __object_find_all_url(type):
    return '{0}/object/{1}/find/all'.format(base_url, type)

user_urls = {
    "create":"user/create",
}

object_urls = {
    "create": __object_create_url,
    "delete": __object_delete_url,
    "delete_with_connection": __object_delete_with_connection_url,
    "multidelete":__object_multidelete_url,
    "get": __object_get_url,
    "multiget": __object_multiget_url,
    "update": __object_update_url,
    "find_all": __object_find_all_url
}


