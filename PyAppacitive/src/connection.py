__author__ = 'sathley'


from entity import BaseObject

class Connection(BaseObject):

    def __init__(self, relation, connectionId):
        self.relation = relation
        self.connectionId = connectionId

