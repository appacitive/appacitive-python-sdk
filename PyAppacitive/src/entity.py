__author__ = 'sathley'

from datetime import datetime


class Entity(object):

    def __init__(self):
        self._properties = {}
        self._attributes = {}
        self._tags = []
        self.id = 0
        self.revision = 0
        self.created_by = None
        self.last_updated_by = None
        self.created_by = None
        self.utc_date_created = None
        self.utc_last_updated_date = None
        self.last_modified_by = None

        self.__properties_changed = {}
        self.__attributes_changed = {}
        self.__tags_added = []
        self.__tags_removed = []

    def set_property(self, property_name, property_value):
        self._properties[property_name] = property_value
        self.__properties_changed[property_name] = property_value

    def get_property(self, property_name):
        return self._properties[property_name]

    def remove_property(self, property_name):
        self.set_property(property_name, None)

    def set_attribute(self, attribute_key, attribute_value):
        self._attributes[attribute_key] = attribute_value
        self.__attributes_changed[attribute_key]= attribute_value

    def get_attribute(self, attribute_key):
        return self._attributes[attribute_key]

    def remove_attribute(self, attribute_key):
        if attribute_key in self._attributes:
            self.set_attribute(attribute_key, None)

    def add_tag(self, tag):
        if tag not in self._tags:
            self._tags.append(tag)
            self.__tags_added.append(tag)

    def remove_tag(self, tag):
        if tag in self._tags:
            self._tags.remove(tag)
            self.__tags_removed.append(tag)

    def tag_exists(self, tag):
        return tag in self._tags

    def get_update_command(self):
        update_command = {}
        update_command['__addtags'] = self.__tags_added
        update_command['__removetags'] = self.__tags_removed
        update_command['__attributes'] = self.__attributes_changed
        for k, v in self.__properties_changed.iteritems():
            update_command[k] = v
        return update_command

