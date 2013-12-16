__author__ = 'sathley'


from entity import Entity
from error import *
from utilities import urlfactory, http, settings
import json


class AppacitiveConnection(Entity):

    def __init__(self):
        super(AppacitiveConnection, self).__init__()
        self.relation_type = None
        self.relation_id = 0
        self.endpoint_a = {}
        self.endpoint_b = {}

    system_properties = ['__type', '__typeid', '__id', '__createdby', '__lastmodifiedby', '__utcdatecreated', '__utclastupdateddate', '__tags', '__attributes', '__properties', '__revision', '__endpointa', '__endpointb']

