__author__ = 'sathley'

from entity import AppacitiveEntity


class ObjectBase(AppacitiveEntity):
    def __init__(self, object_type):
        self._type = object_type



class Restaurant(ObjectBase):
    def __init__(self):
        super(Restaurant, self).__init__('restaurant')