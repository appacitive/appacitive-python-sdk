__author__ = 'sathley'

from object import AppacitiveObject
from entity import object_system_properties
from error import ValidationError, UserAuthError
from utilities import http, urlfactory, appcontext
import json


class AppacitiveDevice(AppacitiveObject):
    def __init__(self, device=None):
        super(AppacitiveDevice, self).__init__()
        self.type = 'device'

    def __set_self(self, device):
        super(AppacitiveDevice, self)._set_self(device)

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

    def create(self):
        mandatory_fields = ['devicetype', 'devicetoken']
        for field in mandatory_fields:
            if self.__getattribute__(field) is None:
                raise ValidationError('{0} is a mandatory field.'.format(field))

        resp = super(AppacitiveDevice, self).create()
        self.__set_self(resp['device'])