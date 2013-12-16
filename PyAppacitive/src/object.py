from os import system

__author__ = 'sathley'

from entity import Entity
from error import *
from utilities import urlfactory, http, settings
import json



class AppacitiveObject(Entity):
    def __init__(self):
        super(AppacitiveObject, self).__init__()
        self.type = None
        self.type_id = 0

    system_properties = ['__type', '__typeid', '__id', '__createdby', '__lastmodifiedby', '__utcdatecreated',
                         '__utclastupdateddate', '__tags', '__attributes', '__properties', '__revision']

    #@staticmethod
    #def get_object(obj):
    #    system_properties = ['__type', '__typeid', '__id', '__createdby', '__lastmodifiedby',
    # '__utcdatecreated', '__utclastupdateddate', '__tags', '__attributes', '__properties', '__revision']
    #    return_object = AppacitiveObject()
    #    return_object.id = int(obj['__id']) if '__id' in obj else 0
    #    return_object.type = obj['__type'] if '__type' in obj else None
    #    return_object.type_id = int(obj['__typeid']) if '__typeid' in obj else 0
    #    return_object.created_by = obj['__createdby'] if '__createdby' in obj else None
    #    return_object.last_modified_by = obj['__lastmodifiedby'] if '__lastmodifiedby' in obj else None
    #    return_object.utc_date_created = obj['__utcdatecreated'] if '__utcdatecreated' in obj else None
    #    return_object.utc_last_updated_date = obj['__utclastupdateddate'] if '__utclastupdateddate' in obj else None
    #    return_object._tags = obj['__tags'] if '__tags' in obj else None
    #    return_object._attributes = obj['__attributes'] if '__attributes' in obj else None
    #    return_object.revision = int(obj['__revision']) if '__revision' in obj else None
    #    for k, v in obj.iteritems():
    #        if k not in system_properties:
    #            return_object._properties[k] = v
    #    return return_object

    def __set_self(self, obj):

        system_properties = ['__type', '__typeid', '__id', '__createdby', '__lastmodifiedby', '__utcdatecreated',
                             '__utclastupdateddate', '__tags', '__attributes', '__properties', '__revision']

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
            if k not in system_properties:
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

    def create(self):

        if self.type is None and self.type_id <= 0:
            raise ValidationException('Provide at least one among type name or type id.')
        url = urlfactory.object_urls["create"](self.type if self.type is not None else self.type_id)
        headers = urlfactory.get_headers()
        resp = http.put(url, headers, self.get_json())
        if resp['status']['code'] == '200':
            self.__set_self(resp['object'])

    def delete(self):

        if self.type is None and self.type_id <= 0:
            raise ValidationException('Provide at least one among type name or type id.')

        if self.id <=0:
            raise ValidationException('Object id is missing.')

        url = urlfactory.object_urls["delete"](self.type if self.type is not None else self.type_id, self.id)
        headers = urlfactory.get_headers()
        return http.delete(url, headers)

    def delete_with_connections(self):

        if self.type is None and self.type_id <= 0:
            raise ValidationException('Provide at least one among type name or type id.')

        if self.id <= 0:
            raise ValidationException('Object id is missing.')

        url = urlfactory.object_urls["delete_with_connection"](self.type if self.type is not None else self.type_id, self.id)
        headers = urlfactory.get_headers()
        return http.delete(url, headers)

    @staticmethod
    def multi_delete(object_type, object_ids):

        if object_type is None :
            raise ValidationException('Type is missing.')

        if object_ids is None:
            raise ValidationException('Object ids are missing.')

        url = urlfactory.object_urls["multidelete"](object_type)
        headers = urlfactory.get_headers()

        payload = {"idlist": []}
        for object_id in object_ids:
            payload["idlist"].append(str(object_id))

        return http.post(url, headers, json.dumps(payload))

    def update(self):

        if self.type is None and self.type_id <= 0:
            raise ValidationException('Provide at least one among type name or type id.')

        if self.id <= 0:
            raise ValidationException('Object id is missing.')
        url = urlfactory.object_urls["update"](self.type if self.type is not None else self.type_id, self.id)
        headers = urlfactory.get_headers()
        payload = self.get_update_command()
        return http.post(url, headers, payload)

    @staticmethod
    def get(object_type, object_id):

        if object_type is None:
            raise ValidationException('Type is missing.')

        if object_id is None:
            raise ValidationException('Object id is missing.')

        url = urlfactory.object_urls["get"](object_type, object_id)
        headers = urlfactory.get_headers()
        response = http.get(url, headers)
        if response['status']['code'] != '200':
            return None

        return_obj = AppacitiveObject()
        return_obj.__set_self(response['object'])
        return return_obj

    @staticmethod
    def multi_get(object_type, object_ids):

        if object_type is None:
            raise ValidationException('Type is missing.')

        if object_ids is None:
            raise ValidationException('Object ids are missing.')

        url = urlfactory.object_urls["multiget"](object_type, object_ids)
        headers = urlfactory.get_headers()
        response = http.get(url, headers)
        if response['status']['code'] != '200':
            return None

        return_objs = []
        for obj in response['objects']:
            obj1 = AppacitiveObject()
            obj1.__set_self(obj)
            return_objs.append(obj1)
        return return_objs

    @staticmethod
    def find(object_type, query):

        if object_type is None:
            raise ValidationException('Type is missing.')

        url = urlfactory.object_urls["find_all"](object_type, query)
        headers = urlfactory.get_headers()
        response = http.get(url, headers)
        if response['status']['code'] != '200':
            return None
        return_objs = []
        for obj in response['objects']:
            obj1 = AppacitiveObject()
            obj1.__set_self(obj)
            return_objs.append(obj1)
        return return_objs