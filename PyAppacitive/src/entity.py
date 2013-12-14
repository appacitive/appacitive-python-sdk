__author__ = 'sathley'

from datetime import datetime


class Entity(object):

    def __init__(self):
        self.__id = 0
        self.__revision = 0
        self.__properties = {}
        self.__attributes = {}
        self.__tags = []
        self.__createdBy = None
        self.__lastUpdatedBy = None
        self.__createdby = None
        self.__utcdatecreated = None
        self.__utclastupdateddate = None
        self.__lastmodifiedby = None


    #def __setattr__(self, key, value):
    #    self.__attributes[key] = value
    #
        
    #def __getattr__(self, item):
    #    if self.__attributes.__contains__(item):
    #        return self.__attributes[item]
    #    return None
