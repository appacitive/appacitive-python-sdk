from pyappacitive.utilities import http, urlfactory, customjson
from response import AppacitiveResponse

__author__ = 'sathley'

from pyappacitive.entity import Entity, connection_system_properties
from pyappacitive.error import *
from pyappacitive.object import AppacitiveObject
from endpoint import AppacitiveEndpoint


class AppacitiveConnection(Entity):

    def __init__(self, connection=None):
        self.relation_type = None
        self.relation_id = 0
        self.endpoint_a = AppacitiveEndpoint()
        self.endpoint_b = AppacitiveEndpoint()

        if isinstance(connection, str):

            super(AppacitiveConnection, self).__init__()
            self.relation_type = connection
            self.relation_id = 0
            return
        if isinstance(connection, int):
            super(AppacitiveConnection, self).__init__()
            self.relation_type = None
            self.relation_id = connection
            return

        super(AppacitiveConnection, self).__init__(connection)

        if connection is not None:
            self.relation_type = connection.get('__relationtype', None)
            self.relation_id = int(connection.get('__relationid', 0))
            if '__endpointa' in connection:
                self.endpoint_a = AppacitiveEndpoint(connection['__endpointa'])

            if '__endpointb' in connection:
                self.endpoint_b = AppacitiveEndpoint(connection['__endpointb'])

    @staticmethod
    def _get_object_dict(obj):

        if obj is None:
            return None
        return obj.get_dict()

    def get_dict(self):

        native = {}
        if self.relation_type is not None:
            native['__relationtype'] = self.relation_type

        if self.relation_id is not None:
            native['__relationid'] = str(self.relation_id)

        if self.id is not None:
            native['__id'] = str(self.id)

        if self.revision is not 0:
            native['__revision'] = str(self.revision)

        if self.created_by is not None:
            native['__createdby'] = self.created_by

        if self.last_modified_by is not None:
            native['__lastmodifiedby'] = self.last_modified_by

        if self.utc_date_created is not None:
            native['__utcdatecreated'] = self.utc_date_created

        if self.utc_last_updated_date is not None:
            native['__utclastupdateddate'] = self.utc_last_updated_date

        tags = self.get_all_tags()
        if tags is not None:
            native['__tags'] = tags

        attributes = self.get_all_attributes()
        if attributes is not None:
            native['__attributes'] = attributes

        properties = self.get_all_properties()
        for property_name, property_value in properties.iteritems():
            native[property_name] = property_value

        native['__endpointa'] = {
            'label': self.endpoint_a.label,
            'type': self.endpoint_a.type,
            'objectid': str(self.endpoint_a.objectid),
            'object': self._get_object_dict(self.endpoint_a.object)
        }

        native['__endpointb'] = {
            'label': self.endpoint_b.label,
            'type': self.endpoint_b.type,
            'objectid': str(self.endpoint_b.objectid),
            'object': self._get_object_dict(self.endpoint_b.object)
        }

        return native

    def __set_self(self, connection):

        super(AppacitiveConnection, self)._set_self(connection)

        self.relation_type = connection.get('__relationtype', None)
        self.relation_id = int(connection.get('__relationid', 0))

        if '__endpointa' in connection:
                self.endpoint_a = AppacitiveEndpoint(connection['__endpointa'])

        if '__endpointb' in connection:
                self.endpoint_b = AppacitiveEndpoint(connection['__endpointb'])

    def create(self):

        if self.relation_type is None and self.relation_id <= 0:
            raise ValidationError('Provide at least one among relation name or relation id.')

        if self.endpoint_a.objectid is 0 and self.endpoint_a.object is None:
            raise ValidationError('Provide object or objectid for endpoint a.')

        if self.endpoint_b.objectid is 0 and self.endpoint_b.object is None:
            raise ValidationError('Provide object or objectid for endpoint b.')

        if self.endpoint_a.label is None and self.endpoint_b.label is None:
            raise ValidationError('Label on both endpoints is mandatory.')


        url = urlfactory.connection_urls["create"](self.relation_type if self.relation_type is not None else self.relation_id)
        headers = urlfactory.get_headers()

        api_resp = http.put(url, headers, customjson.serialize(self.get_dict()))

        response = AppacitiveResponse(api_resp['status'])
        if response.status_code == '200':
            self.__set_self(api_resp['connection'])
            self._reset_update_commands()
        return response

    @classmethod
    def get(cls, relation_type, connection_id, fields=None):

        if relation_type is None:
            raise ValidationError('Relation type is missing.')

        if connection_id is None:
            raise ValidationError('Connection id is missing.')

        url = urlfactory.connection_urls["get"](relation_type, connection_id, fields)

        headers = urlfactory.get_headers()
        api_response = http.get(url, headers)
        response = AppacitiveResponse(api_response['status'])

        if response.status_code == '200':
            response.connection = cls(api_response['connection'])

        return response

    def fetch_latest(self):
        url = urlfactory.connection_urls["get"](self.relation_type, self.id)
        headers = urlfactory.get_headers()
        api_response = http.get(url, headers)
        response = AppacitiveResponse(api_response['status'])
        if response.status_code == '200':
            self._set_self(api_response['connection'])
            self._reset_update_commands()
        return response

    def delete(self):

        if self.relation_type is None and self.relation_id <= 0:
            raise ValidationError('Provide at least one among relation name or relation id.')

        if self.id <= 0:
            raise ValidationError('Connection id is missing.')

        url = urlfactory.connection_urls["delete"](self.relation_type if self.relation_type is not None else self.relation_id, self.id)
        headers = urlfactory.get_headers()
        api_resp = http.delete(url, headers)
        response = AppacitiveResponse(api_resp['status'])
        return response

    @classmethod
    def multi_delete(cls, relation_type, connection_ids):

        if relation_type is None:
            raise ValidationError('Relation type is missing.')

        if connection_ids is None:
            raise ValidationError('Connection ids are missing.')

        url = urlfactory.connection_urls["multidelete"](relation_type)
        headers = urlfactory.get_headers()

        payload = {"idlist": []}
        for connection_id in connection_ids:
            payload["idlist"].append(str(connection_id))

        api_resp = http.post(url, headers, customjson.serialize(payload))
        response = AppacitiveResponse(api_resp['status'])
        return response

    @classmethod
    def multi_get(cls, relation_type, connection_ids, fields=None):

        if relation_type is None:
            raise ValidationError('Relation type is missing.')

        if connection_ids is None:
            raise ValidationError('Connection ids are missing.')

        url = urlfactory.connection_urls["multiget"](relation_type, connection_ids, fields)

        headers = urlfactory.get_headers()
        api_response = http.get(url, headers)

        response = AppacitiveResponse(api_response['status'])
        if response.status_code == '200':

            return_connections = []
            for connection in api_response.get('connections', None):
                appacitive_connection = cls(connection)
                return_connections.append(appacitive_connection)
            response.connections = return_connections
            return response

    def update(self, with_revision=False):

        if self.relation_type is None and self.relation_id <= 0:
            raise ValidationError('Provide at least one among type name or type id.')

        if self.id <= 0:
            raise ValidationError('Connection id is missing.')

        url = urlfactory.connection_urls["update"](self.relation_type if self.relation_type is not None else self.relation_id, self.id)

        if with_revision:
            url += '?revision=' + self.revision

        headers = urlfactory.get_headers()
        payload = self.get_update_command()
        api_resp = http.post(url, headers, customjson.serialize(payload))
        response = AppacitiveResponse(api_resp['status'])

        if response.status_code == '200':
            self.__set_self(api_resp['connection'])
        return response

    @classmethod
    def find(cls, relation_type, query, fields=None):

        if relation_type is None:
            raise ValidationError('Relation type is missing.')

        url = urlfactory.connection_urls["find_all"](relation_type, query, fields)
        headers = urlfactory.get_headers()
        api_response = http.get(url, headers)

        response = AppacitiveResponse(api_response['status'])
        if response.status_code == '200':

            api_connections = api_response.get('connections', None)

            return_connections = []
            for connection in api_connections:
                appacitive_connection = cls(connection)
                return_connections.append(appacitive_connection)
            response.connections = return_connections
            response.paging_info = api_response['paginginfo']
            return response

    @classmethod
    def find_by_objects(cls, object_id_1, object_id_2, relation=None, fields=None):
        if relation is None:
            url = urlfactory.connection_urls["find_for_objects"](object_id_1, object_id_2, fields)
        else:
            url = urlfactory.connection_urls["find_for_objects_and_relation"](relation, object_id_1, object_id_2, fields)

        headers = urlfactory.get_headers()
        api_response = http.get(url, headers)
        response = AppacitiveResponse(api_response['status'])
        if response.status_code == '200':

            api_connections = api_response.get('connections', None)

            return_connections = []
            for connection in api_connections:
                appacitive_connection = cls(connection)
                return_connections.append(appacitive_connection)
            response.connections = return_connections
            response.paging_info = api_response['paginginfo']
            return response

    @classmethod
    def find_interconnects(cls, object_1_id, object_2_ids, fields=None):

        url = urlfactory.connection_urls["find_interconnects"](fields)
        headers = urlfactory.get_headers()

        payload = {"object1id": str(object_1_id), "object2ids": []}

        for object_id in object_2_ids:
            payload['object2ids'].append(str(object_id))

        api_response = http.post(url, headers, customjson.serialize(payload))
        response = AppacitiveResponse(api_response['status'])
        if response.status_code == '200':

            api_connections = api_response.get('connections', None)

            return_connections = []
            for connection in api_connections:
                appacitive_connection = cls(connection)
                return_connections.append(appacitive_connection)
            response.connections = return_connections
            response.paging_info = api_response['paginginfo']
            return response

    @classmethod
    def find_by_object_and_label(cls, relation, object_id, label, fields=None):

        query = '?objectid={1}&label={2}'.format(object_id, label)
        if fields is not None:
            query += '&fields=' + ','.join(fields)

        url = urlfactory.connection_urls["find_all"](relation, object_id, query)

        headers = urlfactory.get_headers()
        api_response = http.get(url, headers)
        response = AppacitiveResponse(api_response['status'])
        if response.status_code == '200':

            api_connections = api_response.get('connections', None)

            return_connections = []
            for connection in api_connections:
                appacitive_connection = cls(connection)
                return_connections.append(appacitive_connection)
            response.connections = return_connections
            response.paging_info = api_response['paginginfo']
            return response

    @classmethod
    def find_connected_objects(cls, relation, object_type, object_id, fields=None):

        url = urlfactory.connection_urls["find_connected_objects"](relation, object_type, object_id, fields)

        headers = urlfactory.get_headers()
        api_response = http.get(url, headers)
        response = AppacitiveResponse(api_response['status'])
        if response.status_code == '200':

            api_objects = api_response.get('nodes', None)

            return_objects = []
            for obj in api_objects:
                appacitive_object = AppacitiveObject(obj)
                return_objects.append(appacitive_object)
            response.nodes = return_objects
            response.paging_info = api_response['paginginfo']
            response.parent = api_response['parent']
            return response






