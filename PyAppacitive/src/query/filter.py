from PyAppacitive.src.query.value import ValueBase, GeoValue, DistanceValue

__author__ = 'sathley'

import types


class FilterBase(object):
    def __init__(self):
        self.operator = None
        self.key = None
        self.value = None

    def __repr__(self):
        raise NotImplementedError('This method should be overridden in derived classes.')


class PropertyFilter(FilterBase):
    def __init__(self, operator, property_name, value):
        super(PropertyFilter, self).__init__()
        self.operator = operator
        self.key = property_name
        self.value = value
        self.value_datatype = None

    def __repr__(self):

        if self.operator == 'within_circle':
            geo_code, distance = self.value
            #if isinstance(geo_code, GeoValue) is False or isinstance(distance, DistanceValue) is False:
            #    raise TypeError('This filter expects a geo value and a distance value.')
            return "*{0} {1} {2},{3}".format(self.key, self.operator, str(geo_code), str(distance))

        if self.operator == 'between':
            value1, value2 = self.value
            #if isinstance(value1, ValueBase) is False or isinstance(value2, ValueBase) is False:
            #    raise TypeError('Both values should be derived from ValueBase. Use appropriate value objects.')
            return "*{0} {1} ({2},{3})".format(self.key, self.operator, str(value1), str(value2))

        #if isinstance(self.value, ValueBase) is False:
        #    raise TypeError('Value should be derived from ValueBase. Use an appropriate value object.')
        return "*{0} {1} {2}".format(self.key, self.operator, str(self.value))

    @classmethod
    def is_equal_to(cls, property_name, value):
        return cls('==', property_name, value)

    @classmethod
    def is_not_equal_to(cls, property_name, value):
        return cls('!=', property_name, value)

    @classmethod
    def is_greater_than(cls, property_name, value):
        return cls('>', property_name, value)

    @classmethod
    def is_less_than(cls, property_name, value):
        return cls('<', property_name, value)

    @classmethod
    def is_greater_than_equal_to(cls, property_name, value):
        return cls('>=', property_name, value)

    @classmethod
    def is_less_than_equal_to(cls, property_name, value):
        return cls('<=', property_name, value)

    @classmethod
    def like(cls, property_name, value):
        return cls('like', property_name, value)

    @classmethod
    def starts_with(cls, property_name, value):
        return cls('like', property_name, '*'+value)

    @classmethod
    def ends_with(cls, property_name, value):
        return cls('like', property_name, value+'*')

    @classmethod
    def between(cls, property_name, value1, value2):
        return cls('between', property_name, (value1, value2))

    # Move geo searches to GeoFilter
    @classmethod
    def within_circle(cls, property_name, geo_code, distance):
        return cls('within_circle', property_name, (geo_code, distance))

    @classmethod
    def within_polygon(cls, property_name, geo_codes):
        return cls('within_polygon', property_name, geo_codes)


class AttributeFilter(FilterBase):
    def __init__(self, operator, attribute_key, value):
        super(AttributeFilter, self).__init__()
        self.operator = operator,
        self.key = attribute_key
        self.value = value

    def __repr__(self):
        if isinstance(self.value, str) is False:
            raise TypeError('Value should be string.')
        return "@{0} {1} {2}".format(self.key, self.operator, self.value)

    @classmethod
    def is_equal_to(cls, property_name, value):
        return cls('==', property_name, value)

    @classmethod
    def like(cls, property_name, value):
        return cls('like', property_name, value)

    @classmethod
    def starts_with(cls, property_name, value):
        return cls('like', property_name, '*'+value)

    @classmethod
    def ends_with(cls, property_name, value):
        return cls('like', property_name, value+'*')


class TagFilter(FilterBase):

    def __init__(self, operator, tags):
        super(TagFilter, self).__init__()
        self.tags = tags
        self.operator = operator

    def __repr__(self):
        if isinstance(self.tags, types.ListType) is False:
            raise TypeError('Expected list of string tags.')
        return "{0}('{1}')".format(self.operator, ','.join(self.tags))

    @classmethod
    def match_one_or_more(cls, tags):
        return cls('tagged_with_one_or_more', tags)

    @classmethod
    def match_atleast_one(cls, tags):
        return cls('tagged_with_all', tags)

