__author__ = 'sathley'

from object import AppacitiveObject
from entity import Entity, object_system_properties
from error import ValidationError, UserAuthError
from utilities import http, urlfactory, appcontext, customjson
from response import Response


class AppacitiveDevice(Entity):
    def __init__(self, device=None):
        super(AppacitiveDevice, self).__init__()
        self.type = 'device'
        self.type_id = 0

        if device is not None:
            self.type = device.get('__type', None)
            self.type_id = int(device.get('__typeid', 0))

    def __set_self(self, device):
        super(AppacitiveDevice, self)._set_self(device)
        self.type = device.get('__type', None)
        self.type_id = int(device.get('__typeid', 0))

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

        native.update(self.get_all_properties())
        return native

    @property
    def devicetype(self):
        return self.get_property('devicetype')

    @devicetype.setter
    def devicetype(self, value):
        self.set_property('devicetype', value)

    @property
    def location(self):
        return self.get_property('location')

    @location.setter
    def location(self, value):
        self.set_property('location', value)

    @property
    def devicetoken(self):
        return self.get_property('devicetoken')

    @devicetoken.setter
    def devicetoken(self, value):
        self.set_property('devicetoken', value)

    @property
    def channels(self):
        return self.get_property('channels')

    @channels.setter
    def channels(self, value):
        self.set_property('channels', value)

    @property
    def badge(self):
        return self.get_property('badge')

    @badge.setter
    def badge(self, value):
        self.set_property('badge', value)

    @property
    def timezone(self):
        return self.get_property('timezone')

    @timezone.setter
    def timezone(self, value):
        self.set_property('timezone', value)

    @property
    def isactive(self):
        return self.get_property('isactive')

    @isactive.setter
    def isactive(self, value):
        self.set_property('isactive', value)

    def register(self):
        mandatory_fields = ['devicetype', 'devicetoken']
        for field in mandatory_fields:
            if self.__getattribute__(field) is None:
                raise ValidationError('{0} is a mandatory field.'.format(field))

        url = urlfactory.device_urls["register"]()
        headers = urlfactory.get_headers()

        api_resp = http.put(url, headers, customjson.serialize(self.get_dict()))

        response = Response(api_resp['status'])

        if response.status_code == '200':
            self.__set_self(api_resp['device'])
            self._reset_update_commands()
        return response

    @classmethod
    def get(cls, device_id):

        if device_id is None:
            raise ValidationError('Device id is missing.')

        url = urlfactory.device_urls["get"](device_id)

        headers = urlfactory.get_headers()

        api_response = http.get(url, headers)

        response = Response(api_response['status'])

        if response.status_code == '200':
            response.device = cls(api_response['device'])
        return response

    @classmethod
    def multi_get(cls, device_ids):

        if device_ids is None:
            raise ValidationError('Device ids are missing.')

        url = urlfactory.object_urls["multiget"]('device', device_ids)
        headers = urlfactory.get_headers()
        api_response = http.get(url, headers)

        response = Response(api_response['status'])
        if response.status_code == '200':

            api_devices = api_response.get('devices', None)

            return_devices = []
            for device in api_devices:
                appacitive_device = cls(device)
                return_devices.append(appacitive_device)
            response.devices = return_devices
            return response

    def update(self, with_revision=False):
        if self.type is None and self.type_id <= 0:
            raise ValidationError('Provide at least one among type name or type id.')

        if self.id <= 0:
            raise ValidationError('Device id is missing.')

        url = urlfactory.device_urls["update"](self.id)

        if with_revision:
            url += '?revision=' + self.revision

        headers = urlfactory.get_user_headers()

        payload = self.get_update_command()
        api_resp = http.post(url, headers, customjson.serialize(payload))
        response = Response(api_resp['status'])

        if response.status_code == '200':
            self.__set_self(api_resp['device'])
        return response

    @classmethod
    def delete_by_id(cls, device_id, delete_connections=False):

        if device_id is None:
            raise ValidationError('Device id is missing.')

        url = urlfactory.device_urls["delete"](device_id, delete_connections)

        headers = urlfactory.get_user_headers()

        api_resp = http.delete(url, headers)
        response = Response(api_resp['status'])
        return response

    def delete(self, delete_connections=False):
        return AppacitiveDevice.delete_by_id(self.id, delete_connections)

    @classmethod
    def find(cls, query):

        url = urlfactory.device_urls["find_all"](query)

        headers = urlfactory.get_user_headers()

        api_response = http.get(url, headers)
        response = Response(api_response['status'])
        if response.status_code == '200':

            api_devices = api_response.get('devices', None)

            return_devices = []
            for device in api_devices:
                appacitive_device = cls(device)
                return_devices.append(appacitive_device)
            response.devices = return_devices
            return response
