__author__ = 'sathley'

from entity import AppacitiveEntity
from object import AppacitiveObject
from error import ValidationError
from utilities import customjson, urlfactory, http
from response import AppacitiveResponse, PagingInfo


class ObjectBase(AppacitiveEntity):
    def __init__(self, obj):
        pass


class Restaurant(ObjectBase):
    def __init__(self):
        super(Restaurant, self).__init__('restaurant')