__author__ = 'sathley'

import settings

base_url = settings.api_base_url


def get_headers():
    return {
        "Appacitive-Apikey": settings.api_key,
        "Appacitive-Environment": settings.environment,
        "Content-Type": "application/json"
    }

#region     OBJECT URLS


def __object_create_url(object_type):
    return '{0}/object/{1}'.format(base_url, object_type)


def __object_delete_url(object_type, object_id):
    return '{0}/object/{1}/{2}'.format(base_url, object_type, object_id)


def __object_multidelete_url(object_type):
    return '{0}/object/{1}/bulkdelete'.format(base_url, object_type)


def __object_delete_with_connection_url(object_type, object_id):
    return '{0}/object/{1}/{2}?deleteconnections=true'.format(base_url, object_type, object_id)


def __object_get_url(object_type, object_id):
    return '{0}/object/{1}/{2}'.format(base_url, object_type, object_id)


def __object_multiget_url(object_type, object_ids):
    return '{0}/object/{1}/multiget/{2}'.format(base_url, object_type, ','.join(object_ids))


def __object_update_url(object_type, object_id):
    return '{0}/object/{1}/{2}'.format(base_url, object_type, object_id)


def __object_find_all_url(object_type, query):
    return '{0}/object/{1}/find/all?{2}'.format(base_url, object_type, str(query))

#endregion

#region     CONNECTION URLS


def __connection_create_url(relation_type):
    return '{0}/connection/{1}'.format(base_url, relation_type)


def __connection_get_url(relation_type, connection_id):
    return '{0}/connection/{1}/{2}'.format(base_url, relation_type, connection_id)


def __connection_multiget_url(relation_type, connection_ids):
    return '{0}/connection/{1}/multiget/{2}'.format(base_url, relation_type, ','.join(connection_ids))


def __connection_delete_url(relation_type, connection_id):
    return '{0}/connection/{1}/{2}'.format(base_url, relation_type, connection_id)


def __connection_multidelete_url(relation_type):
    return '{0}/connection/{1}/bulkdelete'.format(base_url, relation_type)


def __connection_update_url(relation_type, connection_id):
    return '{0}/connection/{1}/{2}'.format(base_url, relation_type, connection_id)


def __connection_find_all_url(relation_type, query):
    return '{0}/connection/{1}/find/all?{2}'.format(base_url, relation_type, str(query))


def __connection_find_for_objects_url(object_id1, object_id2):
    return '{0}/connection/find/{1}/{2}'.format(base_url, str(object_id1), str(object_id2))


def __connection_find_for_objects_and_relation_url(relation_type, object_id1, object_id2):
    return '{0}/connection/{1}/find/{2}/{3}'.format(base_url, relation_type, str(object_id1), str(object_id2))


def __connection_find_interconnects_url():
    return '{0}/connection/interconnects'.format(base_url)

#endregion

#region     USER URLS

#endregion

user_urls = {
    "create": "user/create",
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

connection_urls = {
    "create": __connection_create_url,
    "get": __connection_get_url,
    "multiget": __connection_multiget_url,
    "delete": __connection_delete_url,
    "multidelete": __connection_multidelete_url,
    "update": __connection_update_url,
    "find_all": __connection_find_all_url,
    "find_for_objects": __connection_find_for_objects_url,
    "find_for_objects_and_relation": __connection_find_for_objects_and_relation_url,
    "find_interconnects": __connection_find_interconnects_url
}


