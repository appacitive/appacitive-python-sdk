from pyappacitive.utilities import http, urlfactory

__author__ = 'sathley'

from pyappacitive.entity import Entity, object_system_properties
from pyappacitive.error import *
import json


class AppacitiveObject(Entity):

    def __init__(self, obj=None):
        super(AppacitiveObject, self).__init__(obj)
        self.type = None
        self.type_id = 0

        if obj is not None:
            self.type = obj['__type'] if '__type' in obj else None
            self.type_id = int(obj['__typeid']) if '__typeid' in obj else 0

    def __set_self(self, obj):

        if obj is None:
            pass

        self.id = int(obj['__id']) if '__id' in obj else 0
        self.type = obj['__type'] if '__type' in obj else None
        self.type_id = int(obj['__typeid']) if '__typeid' in obj else 0
        self.created_by = obj['__createdby'] if '__createdby' in obj else None
        self.last_modified_by = obj['__lastmodifiedby'] if '__lastmodifiedby' in obj else None
        self.utc_date_created = obj['__utcdatecreated'] if '__utcdatecreated' in obj else None
        self.utc_last_updated_date = obj['__utclastupdateddate'] if '__utclastupdateddate' in obj else None
        self._tags = obj['__tags'] if '__tags' in obj else None
        self._attributes = obj['__attributes'] if '__attributes' in obj else None
        self.revision = int(obj['__revision']) if '__revision' in obj else None
        for k, v in obj.iteritems():
            if k not in object_system_properties:
                self._properties[k] = v

    def get_json(self):

        native = {}
        native['__type'] = self.type
        native['__typeid'] = str(self.type_id)
        native['__id'] = str(self.id)
        native['__revision'] = str(self.revision)
        native['__createdby'] = self.created_by
        native['__lastmodifiedby'] = self.last_modified_by
        native['__utcdatecreated'] = self.utc_date_created
        native['__utclastupdateddate'] = self.utc_last_updated_date
        native['__tags'] = self._tags
        native['__attributes'] = self._attributes
        for property_name, property_value in self._properties.iteritems():
            native[property_name] = property_value
        return json.dumps(native)

    def get_dict(self):

        native = {}
        native['__type'] = self.type
        native['__typeid'] = str(self.type_id)
        native['__id'] = str(self.id)
        native['__revision'] = str(self.revision)
        native['__createdby'] = self.created_by
        native['__lastmodifiedby'] = self.last_modified_by
        native['__utcdatecreated'] = self.utc_date_created
        native['__utclastupdateddate'] = self.utc_last_updated_date
        native['__tags'] = self._tags
        native['__attributes'] = self._attributes
        for property_name, property_value in self._properties.iteritems():
            native[property_name] = property_value
        return native

    def create(self):

        if self.type is None and self.type_id <= 0:
            raise ValidationError('Provide at least one among type name or type id.')

        url = urlfactory.object_urls["create"](self.type if self.type is not None else self.type_id)
        headers = urlfactory.get_headers()
        resp = http.put(url, headers, self.get_json())
        if resp['status']['code'] != '200':
            return None
        obj = resp.get('object', None)
        if obj is None:
            return resp
        self.__set_self(resp['object'])

    def delete(self):

        if self.type is None and self.type_id <= 0:
            raise ValidationError('Provide at least one among type name or type id.')

        if self.id <= 0:
            raise ValidationError('Object id is missing.')

        url = urlfactory.object_urls["delete"](self.type if self.type is not None else self.type_id, self.id)
        headers = urlfactory.get_headers()
        return http.delete(url, headers)

    def delete_with_connections(self):

        if self.type is None and self.type_id <= 0:
            raise ValidationError('Provide at least one among type name or type id.')

        if self.id <= 0:
            raise ValidationError('Object id is missing.')

        url = urlfactory.object_urls["delete_with_connections"](self.type if self.type is not None else self.type_id,
                                                               self.id)
        headers = urlfactory.get_headers()
        return http.delete(url, headers)

    @classmethod
    def multi_delete(cls, object_type, object_ids):

        if object_type is None:
            raise ValidationError('Type is missing.')

        if object_ids is None:
            raise ValidationError('Object ids are missing.')

        url = urlfactory.object_urls["multidelete"](object_type)
        headers = urlfactory.get_headers()

        payload = {"idlist": []}
        for object_id in object_ids:
            payload["idlist"].append(str(object_id))

        return http.post(url, headers, json.dumps(payload))

    def update(self):

        if self.type is None and self.type_id <= 0:
            raise ValidationError('Provide at least one among type name or type id.')

        if self.id <= 0:
            raise ValidationError('Object id is missing.')
        url = urlfactory.object_urls["update"](self.type if self.type is not None else self.type_id, self.id)
        headers = urlfactory.get_headers()
        payload = self.get_update_command()
        resp = http.post(url, headers, payload)
        if resp['status']['code'] != '200':
            return None

        obj = resp.get('object', None)
        if obj is None:
            return resp

        self.__set_self(obj)

    @classmethod
    def get(cls, object_type, object_id):

        if object_type is None:
            raise ValidationError('Type is missing.')

        if object_id is None:
            raise ValidationError('Object id is missing.')

        url = urlfactory.object_urls["get"](object_type, object_id)
        headers = urlfactory.get_headers()
        response = http.get(url, headers)

        if response['status']['code'] != '200':
            return None

        obj = response.get('object', None)
        if obj is None:
            return response

        return cls(response['object'])

    @classmethod
    def multi_get(cls, object_type, object_ids):

        if object_type is None:
            raise ValidationError('Type is missing.')

        if object_ids is None:
            raise ValidationError('Object ids are missing.')

        url = urlfactory.object_urls["multiget"](object_type, object_ids)
        headers = urlfactory.get_headers()
        response = http.get(url, headers)

        if response['status']['code'] != '200':
            return None

        objs = response.get('objects', None)
        if objs is None:
            return response

        return_objs = []
        for obj in objs:
            obj1 = cls(obj)
            return_objs.append(obj1)
        return return_objs

    @classmethod
    def find(cls, object_type, query):

        if object_type is None:
            raise ValidationError('Type is missing.')

        url = urlfactory.object_urls["find_all"](object_type, query)
        headers = urlfactory.get_headers()
        response = http.get(url, headers)
        if response['status']['code'] != '200':
            return None

        objects = response.get('objects', None)
        if objects is None:
            return response

        return_objs = []
        for obj in objects:
            obj1 = cls(obj)
            return_objs.append(obj1)
        return return_objs