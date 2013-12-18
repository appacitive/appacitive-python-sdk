__author__ = 'sathley'

from object import AppacitiveObject
from entity import object_system_properties
from error import ValidationError, UserAuthError
from utilities import http, urlfactory, appcontext
import json

class AppacitiveDevice(AppacitiveObject):
    def __init__(self, device=None):
        super(AppacitiveDevice, self).__init__()
        self._properties = {
            'devicetype': None,
            'location': None,
            'devicetoken': None,
            'channels': None,
            'badge': None,
            'isactive': None,
            'timezone': None
        }
        self.type = 'device'

    def __set_self(self, device):

        if device is None:
            pass

        self.id = int(device['__id']) if '__id' in device else 0
        self.type = device['__type'] if '__type' in device else None
        self.type_id = int(device['__typeid']) if '__typeid' in device else 0
        self.created_by = device['__createdby'] if '__createdby' in device else None
        self.last_modified_by = device['__lastmodifiedby'] if '__lastmodifiedby' in device else None
        self.utc_date_created = device['__utcdatecreated'] if '__utcdatecreated' in device else None
        self.utc_last_updated_date = device['__utclastupdateddate'] if '__utclastupdateddate' in device else None
        self._tags = device['__tags'] if '__tags' in device else None
        self._attributes = device['__attributes'] if '__attributes' in device else None
        self.revision = int(device['__revision']) if '__revision' in device else None
        for k, v in device.iteritems():
            if k not in object_system_properties:
                self._properties[k] = v

    @property
    def devicetype(self):
        return self._properties['devicetype']

    @devicetype.setter
    def devicetype(self, value):
        self._properties['devicetype'] = value

    @property
    def location(self):
        return self._properties['location']

    @location.setter
    def location(self, value):
        self._properties['location'] = value

    @property
    def devicetoken(self):
        return self._properties['devicetoken']

    @devicetoken.setter
    def devicetoken(self, value):
        self._properties['devicetoken'] = value

    @property
    def channels(self):
        return self._properties['channels']

    @channels.setter
    def channels(self, value):
        self._properties['channels'] = value

    @property
    def badge(self):
        return self._properties['badge']

    @badge.setter
    def badge(self, value):
        self._properties['badge'] = value

    @property
    def timezone(self):
        return self._properties['timezone']

    @timezone.setter
    def timezone(self, value):
        self._properties['timezone'] = value

    @property
    def isactive(self):
        return self._properties['isactive']

    @isactive.setter
    def isactive(self, value):
        self._properties['isactive'] = value

    def create(self):
        mandatory_fields = ['devicetype', 'devicetoken']
        for field in mandatory_fields:
            if self.__getattribute__(field) is None:
                raise ValidationError('{0} is a mandatory field.'.format(field))

        resp = super(AppacitiveDevice, self).create()
        self.__set_self(resp['device'])