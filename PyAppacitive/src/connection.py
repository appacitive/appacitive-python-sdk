__author__ = 'sathley'


from entity import Entity
from error import *
from utilities import urlfactory, http, settings
import json
from object import AppacitiveObject

connection_system_properties = ['__relationtype', '__relationid', '__id', '__createdby', '__lastmodifiedby',
                                '__utcdatecreated', '__utclastupdateddate', '__tags', '__attributes', '__properties',
                                '__revision', '__endpointa', '__endpointb']


class AppacitiveConnection(Entity):

    def __init__(self, connection=None):
        super(AppacitiveConnection, self).__init__()
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

            self.id = int(connection['__id']) if '__id' in connection else 0
            self.relation_type = connection['__relationtype'] if '__relationtype' in connection else None
            self.relation_id = int(connection['__relationid']) if '__relationid' in connection else 0
            self.created_by = connection['__createdby'] if '__createdby' in connection else None
            self.last_modified_by = connection['__lastmodifiedby'] if '__lastmodifiedby' in connection else None
            self.utc_date_created = connection['__utcdatecreated'] if '__utcdatecreated' in connection else None
            self.utc_last_updated_date = connection['__utclastupdateddate'] if '__utclastupdateddate' in connection else None
            self._tags = connection['__tags'] if '__tags' in connection else None
            self._attributes = connection['__attributes'] if '__attributes' in connection else None
            self.revision = int(connection['__revision']) if '__revision' in connection else None

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

            for k, v in connection.iteritems():
                if k not in connection_system_properties:
                    self._properties[k] = v

    @staticmethod
    def _get_object_dict(obj):

        if obj is None:
            return None
        native = {}
        native['__type'] = obj.type
        native['__typeid'] = str(obj.type_id)
        native['__id'] = str(obj.id)
        native['__revision'] = str(obj.revision)
        native['__createdby'] = obj.created_by
        native['__lastmodifiedby'] = obj.last_modified_by
        native['__utcdatecreated'] = obj.utc_date_created
        native['__utclastupdateddate'] = obj.utc_last_updated_date
        native['__tags'] = obj._tags
        native['__attributes'] = obj._attributes
        for property_name, property_value in obj._properties.iteritems():
            native[property_name] = property_value
        return native

    def get_json(self):

        native = {}
        native['__relationtype'] = self.relation_type
        native['__relationid'] = str(self.relation_id)
        native['__id'] = str(self.id)
        native['__revision'] = str(self.revision)
        native['__createdby'] = self.created_by
        native['__lastmodifiedby'] = self.last_modified_by
        native['__utcdatecreated'] = self.utc_date_created
        native['__utclastupdateddate'] = self.utc_last_updated_date
        native['__tags'] = self._tags
        native['__attributes'] = self._attributes

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

        for property_name, property_value in self._properties.iteritems():
            native[property_name] = property_value

        return json.dumps(native)

    def __set_self(self, connection):

        self.id = int(connection['__id']) if '__id' in connection else 0
        self.relation_type = connection['__relationtype'] if '__relationtype' in connection else None
        self.relation_id = int(connection['__relationid']) if '__relationid' in connection else 0
        self.created_by = connection['__createdby'] if '__createdby' in connection else None
        self.last_modified_by = connection['__lastmodifiedby'] if '__lastmodifiedby' in connection else None
        self.utc_date_created = connection['__utcdatecreated'] if '__utcdatecreated' in connection else None
        self.utc_last_updated_date = connection['__utclastupdateddate'] if '__utclastupdateddate' in connection else None
        self._tags = connection['__tags'] if '__tags' in connection else None
        self._attributes = connection['__attributes'] if '__attributes' in connection else None
        self.revision = int(connection['__revision']) if '__revision' in connection else None

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

        for k, v in connection.iteritems():
            if k not in connection_system_properties:
                self._properties[k] = v

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
        resp = http.put(url, headers, self.get_json())
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
        #return_obj = AppacitiveObject()
        #return_obj.__set_self(response['object'])
        #return return_obj

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

        #return_objs = []
        #for obj in response['objects']:
        #    obj1 = AppacitiveObject()
        #    obj1.__set_self(obj)
        #    return_objs.append(obj1)
        #return return_objs

        return_conns = []
        for conn in response['connections']:
            obj1 = cls(conn)
            return_conns.append(conn)
        return return_conns

    def update(self):

        if self.relation_type is None and self.relation_id <= 0:
            raise ValidationError('Provide at least one among type name or type id.')

        if self.id <= 0:
            raise ValidationError('Connection id is missing.')

        url = urlfactory.connection_urls["update"](self.relation_type if self.relation_typee is not None else self.relation_id, self.id)
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
            #return_objs = []
        #for obj in response['objects']:
        #    obj1 = AppacitiveObject()
        #    obj1.__set_self(obj)
        #    return_objs.append(obj1)
        #return return_objs

        return_conns = []
        for conn in response['connections']:
            obj1 = cls(conn)
            return_conns.append(conn)
        return return_conns







