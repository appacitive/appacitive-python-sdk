from pyappacitive.utilities import settings

__author__ = 'sathley'

base_url = settings.api_base_url


def get_headers(**headers_key):
    headers_key.update({
        "Appacitive-Apikey": settings.api_key,
        "Appacitive-Environment": settings.environment,
        "Content-Type": "application/json"}
    )
    return headers_key


#region     OBJECT URLS


def __object_create_url(object_type):
    if object_type == 'user':
        return __user_create_url()
    return '{0}/object/{1}'.format(base_url, object_type)


def __object_delete_url(object_type, object_id):
    if object_type == 'user':
        return __user_delete_url(object_id)
    return '{0}/object/{1}/{2}'.format(base_url, object_type, object_id)


def __object_multidelete_url(object_type):
    if object_type == 'user':
        return __user_multidelete_url()
    return '{0}/object/{1}/bulkdelete'.format(base_url, object_type)


def __object_delete_with_connections_url(object_type, object_id):
    if object_type == 'user':
        return __user_delete_with_connections_url(object_id)
    return '{0}/object/{1}/{2}?deleteconnections=true'.format(base_url,
                                                              object_type,
                                                              object_id)


def __object_get_url(object_type, object_id):
    if object_type == 'user':
        return __user_get_url(object_id)
    return '{0}/object/{1}/{2}'.format(base_url, object_type, object_id)


def __object_multiget_url(object_type, object_ids):
    if object_type == 'user':
        return __user_multiget_url(object_ids)
    return '{0}/object/{1}/multiget/{2}'.format(base_url, object_type,
                                                ','.join(object_ids))


def __object_update_url(object_type, object_id):
    if object_type == 'user':
        return __user_update_url(object_id)
    return '{0}/object/{1}/{2}'.format(base_url, object_type, object_id)


def __object_find_all_url(object_type, query):
    if object_type == 'user':
        return __user_find_all_url(query)
    return '{0}/object/{1}/find/all?{2}'.format(base_url, object_type,
                                                str(query))

#endregion

#region     CONNECTION URLS


def __connection_create_url(relation_type):
    return '{0}/connection/{1}'.format(base_url, relation_type)


def __connection_get_url(relation_type, connection_id):
    return '{0}/connection/{1}/{2}'.format(base_url, relation_type,
                                           connection_id)


def __connection_multiget_url(relation_type, connection_ids):
    return '{0}/connection/{1}/multiget/{2}'.format(base_url, relation_type,
                                                    ','.join(connection_ids))


def __connection_delete_url(relation_type, connection_id):
    return '{0}/connection/{1}/{2}'.format(base_url, relation_type,
                                           connection_id)


def __connection_multidelete_url(relation_type):
    return '{0}/connection/{1}/bulkdelete'.format(base_url, relation_type)


def __connection_update_url(relation_type, connection_id):
    return '{0}/connection/{1}/{2}'.format(base_url, relation_type,
                                           connection_id)


def __connection_find_all_url(relation_type, query):
    return '{0}/connection/{1}/find/all?{2}'.format(base_url, relation_type,
                                                    str(query))


def __connection_find_for_objects_url(object_id1, object_id2):
    return '{0}/connection/find/{1}/{2}'.format(base_url, str(object_id1),
                                                str(object_id2))


def __connection_find_for_objects_and_relation_url(relation_type, object_id1,
                                                   object_id2):
    return '{0}/connection/{1}/find/{2}/{3}'.format(base_url, relation_type,
                                                    str(object_id1),
                                                    str(object_id2))


def __connection_find_interconnects_url():
    return '{0}/connection/interconnects'.format(base_url)


def __update__password_url(user_id, identification_type):
    return '%s/user/%s/changepassword?useridtype=%s' % (base_url, user_id,
                                                        identification_type)

#endregion

#region     USER URLS


def __user_create_url():
    return '{0}/user/create'.format(base_url)


def __user_delete_url(user_id, user_id_type='id', delete_connections=False):
    return '{0}/user/{1}?useridtype={2}&deleteconnections={3}'.format(base_url, user_id, user_id_type, delete_connections)


def __user_multidelete_url():
    return '{0}/user/bulkdelete'.format(base_url)


def __user_delete_with_connections_url(user_id):
    return '{0}/user/{1}?deleteconnections=true'.format(base_url, user_id)


def __user_get_url(user_id, user_id_type='id'):
    return '{0}/user/{1}?useridtype={2}'.format(base_url, user_id, user_id_type)


def __user_multiget_url(user_ids):
    return '{0}/user/multiget/{1}'.format(base_url, ','.join(user_ids))


def __user_update_url(user_id):
    return '{0}/user/{1}'.format(base_url, user_id)


def __user_find_all_url(query):
    return '{0}/user/find/all?{1}'.format(base_url, str(query))


def __user_authenticate_url():
    return '{0}/user/authenticate'.format(base_url)


def __user_send_reset_password_email_url():
    return '{0}/user/sendresetpassword'.format(base_url)


def __user_validate_session_url():
    return '{0}/user/validate'.format(base_url)


def __user_invalidate_session_url():
    return '{0}/user/invalidate'.format(base_url)


def __user_checkin_url(user_id, latitude, longitude):
    return '{0}/user/{1}/checkin?latitude={2}&longitude={3}'.format(base_url, user_id, latitude, longitude)

#endregion

#region MISC URLS

def __graph_filter_url(filter_query_name):
    return '{0}/search/filter/{1}'.format(base_url, filter_query_name)


def __graph_project_url(project_query_name):
    return '{0}/search/projection/{1}'.format(base_url, project_query_name)


def __email_send_url():
    return '{0}/email/send'.format(base_url)


def __get_file_upload_url(content_type):
    return '{0}/file/uploadurl?contenttype={1}'.format(base_url, content_type)


def __get_file_download_url(file_id):
    return '{0}/file/download/{1}'.format(base_url, file_id)


def __get_file_delete_url(file_id):
    return '{0}/file/delete/{1}'.format(base_url, file_id)

#endregion

user_urls = {
    "create": __user_create_url,
    "delete": __user_delete_url,
    "delete_with_connections": __user_delete_with_connections_url,
    "multidelete": __user_multidelete_url,
    "get": __user_get_url,
    "multiget": __user_multiget_url,
    "update": __user_update_url,
    "find_all": __user_find_all_url,
    "update_password": __update__password_url,
    "authenticate": __user_authenticate_url,
    "send_reset_password_email": __user_send_reset_password_email_url,
    "validate_session": __user_validate_session_url,
    "invalidate_session": __user_invalidate_session_url,
    "checkin": __user_checkin_url
}

object_urls = {
    "create": __object_create_url,
    "delete": __object_delete_url,
    "delete_with_connections": __object_delete_with_connections_url,
    "multidelete": __object_multidelete_url,
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

email_urls = {
    "send": __email_send_url
}

graph_search_urls = {
    "filter": __graph_filter_url,
    "project": __graph_project_url
}

file_urls = {
    "get_upload_url": __get_file_upload_url,
    "get_download_url": __get_file_download_url,
    "file_delete": __get_file_delete_url
}
