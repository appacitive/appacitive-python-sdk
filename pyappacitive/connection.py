from pyappacitive.utilities import http, urlfactory

__author__ = 'sathley'

# remove values.py and figure out data type from Python type
# use dict.get to set up objects
# add logging

from pyappacitive.entity import Entity, connection_system_properties
from pyappacitive.error import *
import json
from pyappacitive.object import AppacitiveObject


class AppacitiveConnection(Entity):

    def __init__(self, connection=None):
        super(AppacitiveConnection, self).__init__(connection)
        self.relation_type = None
        self.relation_id = 0
        self.endpoint_a = {
            'label': None,
            'type': None,
            'objectid': None,
            'object': None
        }
        self.endpoint_b = {
            'label': None,
            'type': None,
            'objectid': None,
            'object': None
        }
        if connection is not None:
            self.relation_type = connection.get('__relationtype', None)
            self.relation_id = int(connection.get('__relationid', 0))
            if '__endpointa' in connection:
                self.endpoint_a['label'] = connection['__endpointa']['label'] if 'label' in connection['__endpointa'] else None
                self.endpoint_a['type'] = connection['__endpointa']['type'] if 'type' in connection['__endpointa'] else None
                self.endpoint_a['objectid'] = int(connection['__endpointa']['objectid']) if 'objectid' in connection['__endpointa'] else None

                if 'object' in connection['__endpointa']:
                    self.endpoint_a['object'] = AppacitiveObject(connection['__endpointa']['object'])

            if '__endpointb' in connection:
                self.endpoint_b['label'] = connection['__endpointb']['label'] if 'label' in connection['__endpointb'] else None
                self.endpoint_b['type'] = connection['__endpointb']['type'] if 'type' in connection['__endpointb'] else None
                self.endpoint_b['objectid'] = int(connection['__endpointb']['objectid']) if 'objectid' in connection['__endpointb'] else None

                if 'object' in connection['__endpointb']:
                    self.endpoint_b['object'] = AppacitiveObject(connection['__endpointb']['object'])

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
        for property_name, property_value in properties:
            native[property_name] = property_value

        native['__endpointa'] = {
            'label': self.endpoint_a['label'],
            'type': self.endpoint_a['type'],
            'objectid': str(self.endpoint_a['objectid']),
            'object': self._get_object_dict(self.endpoint_a['object'])
        }

        native['__endpointb'] = {
            'label': self.endpoint_b['label'],
            'type': self.endpoint_b['type'],
            'objectid': str(self.endpoint_b['objectid']),
            'object': self._get_object_dict(self.endpoint_b['object'])
        }

        return native

    def __set_self(self, connection):

        super(AppacitiveConnection, self)._set_self(connection)

        self.relation_type = connection.get('__relationtype', None)
        self.relation_id = int(connection.get('__relationid', 0))

        if '__endpointa' in connection:
                self.endpoint_a['label'] = connection['__endpointa']['label'] if 'label' in connection['__endpointa'] else None
                self.endpoint_a['type'] = connection['__endpointa']['type'] if 'type' in connection['__endpointa'] else None
                self.endpoint_a['objectid'] = int(connection['__endpointa']['objectid']) if 'objectid' in connection['__endpointa'] else None

                if 'object' in connection['__endpointa']:
                    self.endpoint_a['object'] = AppacitiveObject(connection['__endpointa']['object'])

        if '__endpointb' in connection:
                self.endpoint_b['label'] = connection['__endpointb']['label'] if 'label' in connection['__endpointb'] else None
                self.endpoint_b['type'] = connection['__endpointb']['type'] if 'type' in connection['__endpointb'] else None
                self.endpoint_b['objectid'] = int(connection['__endpointb']['objectid']) if 'objectid' in connection['__endpointb'] else None

                if 'object' in connection['__endpointb']:
                    self.endpoint_b['object'] = AppacitiveObject(connection['__endpointb']['object'])

    def create(self):

        if self.relation_type is None and self.relation_id <= 0:
            raise ValidationError('Provide at least one among relation name or relation id.')

        if self.endpoint_a['objectid'] is None and self.endpoint_a['object'] is None:
            raise ValidationError('Provide object or objectid for endpoint a.')

        if self.endpoint_b['objectid'] is None and self.endpoint_b['object'] is None:
            raise ValidationError('Provide object or objectid for endpoint b.')

        if self.endpoint_a['label'] is None and self.endpoint_b['label'] is None:
            raise ValidationError('Label on both endpoints is mandatory.')

        url = urlfactory.connection_urls["create"](self.relation_type if self.relation_type is not None else self.relation_id)
        headers = urlfactory.get_headers()
        resp = http.put(url, headers, json.dumps(self.get_dict()))
        if resp['status']['code'] == '200':
            self.__set_self(resp['connection'])

    @classmethod
    def get(cls, relation_type, connection_id):

        if relation_type is None:
            raise ValidationError('Relation type is missing.')

        if connection_id is None:
            raise ValidationError('Connection id is missing.')

        url = urlfactory.connection_urls["get"](relation_type, connection_id)
        headers = urlfactory.get_headers()
        response = http.get(url, headers)
        if response['status']['code'] != '200':
            return None

        return cls(response['connection'])

    def delete(self):

        if self.relation_type is None and self.relation_id <= 0:
            raise ValidationError('Provide at least one among relation name or relation id.')

        if self.id <= 0:
            raise ValidationError('Connection id is missing.')

        url = urlfactory.connection_urls["delete"](self.relation_type if self.relation_type is not None else self.relation_id, self.id)
        headers = urlfactory.get_headers()
        return http.delete(url, headers)

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

        return http.post(url, headers, json.dumps(payload))

    @classmethod
    def multi_get(cls, relation_type, connection_ids):

        if relation_type is None:
            raise ValidationError('Relation type is missing.')

        if connection_ids is None:
            raise ValidationError('Connection ids are missing.')

        url = urlfactory.connection_urls["multiget"](relation_type, connection_ids)
        headers = urlfactory.get_headers()
        response = http.get(url, headers)
        if response['status']['code'] != '200':
            return None

        return_conns = []
        for conn in response['connections']:
            conn1 = cls(conn)
            return_conns.append(conn1)
        return return_conns

    def update(self):

        if self.relation_type is None and self.relation_id <= 0:
            raise ValidationError('Provide at least one among type name or type id.')

        if self.id <= 0:
            raise ValidationError('Connection id is missing.')

        url = urlfactory.connection_urls["update"](self.relation_type if self.relation_type is not None else self.relation_id, self.id)
        headers = urlfactory.get_headers()
        payload = self.get_update_command()
        resp = http.post(url, headers, payload)
        if resp['status']['code'] == '200':
            self.__set_self(resp['connection'])

    @classmethod
    def find(cls, relation_type, query):

        if relation_type is None:
            raise ValidationError('Relation type is missing.')

        url = urlfactory.connection_urls["find_all"](relation_type, query)
        headers = urlfactory.get_headers()
        response = http.get(url, headers)
        if response['status']['code'] != '200':
            return None

        return_conns = []
        for conn in response['connections']:
            conn1 = cls(conn)
            return_conns.append(conn1)
        return return_conns

    @classmethod
    def find_by_objects(cls, object_id_1, object_id_2, relation=None):
        if relation is None:
            url = urlfactory.connection_urls["find_for_objects"](object_id_1, object_id_2)
        else:
            url = urlfactory.connection_urls["find_for_objects_and_relation"](relation, object_id_1, object_id_2)

        headers = urlfactory.get_headers()
        response = http.get(url, headers)
        if response['status']['code'] != '200':
            return None

        return_conns = []
        for conn in response['connections']:
            conn1 = cls(conn)
            return_conns.append(conn1)
        return return_conns

    @classmethod
    def find_interconnects(cls, object_1_id, object_2_ids):

        url = urlfactory.connection_urls["find_interconnects"]()
        headers = urlfactory.get_headers()

        payload = {"object1id": str(object_1_id), "object2ids": []}

        for object_id in object_2_ids:
            payload['object2ids'].append(str(object_id))

        response = http.post(url, headers, json.dumps(payload))
        if response['status']['code'] != '200':
            return None

        return_conns = []
        for conn in response['connections']:
            conn1 = cls(conn)
            return_conns.append(conn1)
        return return_conns

    @classmethod
    def find_by_object_and_label(cls, relation, object_id, label):

        query = '?objectid={1}&label={2}'.format(object_id, label)
        url = urlfactory.connection_urls["find_all"](relation, object_id, query)

        headers = urlfactory.get_headers()
        response = http.get(url, headers)
        if response['status']['code'] != '200':
            return None

        return_conns = []
        for conn in response['connections']:
            conn1 = cls(conn)
            return_conns.append(conn1)
        return return_conns





