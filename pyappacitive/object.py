from pyappacitive.utilities import http, urlfactory

__author__ = 'sathley'

from pyappacitive.entity import Entity, object_system_properties
from pyappacitive.error import *
import json

# add support for update with revision number 
# add fetch latest.call
# add fields in get calls
# add file upload support using urllib2
# add imports in init.py
## stop sending None properties
## remove .idea folder
# logging and nosetests
## set_self should have only specific setting implementation for the current class. It should call the set self of base for #others
## add aggregate filter,
## check tag filter method names
## push send - single function using kwargs
# email- use kwargs
# move object/conn/user class methods to new provider classes ?? Or make user inherit from entity and provide a objectbase class to the user
## properties in user/device should use setproperty and getproperty funcs to keep track of changes
## make properties private and provide a get all properties function


class AppacitiveObject(Entity):

    def __init__(self, obj=None):
        super(AppacitiveObject, self).__init__(obj)
        self.type = None
        self.type_id = 0

        if obj is not None:
            self.type = obj['__type'] if '__type' in obj else None
            self.type_id = int(obj['__typeid']) if '__typeid' in obj else 0

    def __set_self(self, obj):

        super(AppacitiveObject, self)._set_self(obj)

        self.type = obj.get('__type', None)
        self.type_id = int(obj.get('__typeid', 0))

    def get_dict(self):

        native = {}
        if self.type is not None:
            native['__type'] = self.type

        if self.type_id is not None:
            native['__typeid'] = str(self.type_id)

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
        return native

    def create(self):

        if self.type is None and self.type_id <= 0:
            raise ValidationError('Provide at least one among type name or type id.')

        url = urlfactory.object_urls["create"](self.type if self.type is not None else self.type_id)
        headers = urlfactory.get_headers()
        resp = http.put(url, headers, json.dumps(self.get_dict()))
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
