__author__ = 'sathley'

from object import AppacitiveObject
from connection import AppacitiveConnection


class GraphNode(object):
    def __init__(self, node=None):
        self.object = None
        self.connection = None
        self.children = {}
        self.parent = None

    def add_child_node(self, name, node):
        val = self.children.get(name, None)

        if val is None:
            self.children[name] = []

        self.children[name].append(node)









