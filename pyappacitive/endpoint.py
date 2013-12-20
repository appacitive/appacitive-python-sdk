__author__ = 'sathley'

from pyappacitive.object import AppacitiveObject


class AppacitiveEndpoint(object):
    def __init__(self, endpoint=None):
        if endpoint is not None:
            self.label = endpoint.get('label', None)
            self.type = endpoint.get('type', None)
            self.objectid = endpoint.get('objectid', 0)
            obj = endpoint.get('object', None)
            if obj is not None:
                self.object = AppacitiveObject(obj)
        else:
            self.label = None
            self.object = None
            self.type = None
            self.objectid = 0