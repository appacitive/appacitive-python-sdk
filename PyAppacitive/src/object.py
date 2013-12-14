__author__ = 'sathley'

from entity import Entity
from error import *
from utilities import urlfactory, http


class Object(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.__type = None
        self.__typeid = None

    def getJSON(self):
        native = {}
        native['__type'] = self.__type
        native['__typeid'] = self.__typeid
        native['__id'] = self.__id
        native['__createdby'] = self.__createdby
        native['__lastmodifiedby'] = self.__lastmodifiedby
        native['__utcdatecreated'] = self.__utcdatecreated
        native['__utclastupdateddate'] = self.__utclastupdateddate
        native['__tags'] = self.__tags
        native['__attributes'] = self.__attributes
        for property_name, property_value in self.__properties:
            native[property_name] = property_value
        return native

    #@staticmethod
    #def get(objectid):
    #    pass

    #@classmethod
    #def create(self):
    #    if self.__type is None and self.__typeid is None:
    #        raise ValidationException('Provide at least one among type name or type id.');