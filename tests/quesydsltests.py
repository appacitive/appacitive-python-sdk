from pyappacitive.query import filter, value, operator

__author__ = 'sathley'

from pyappacitive.query.query import AppacitiveQuery
import datetime


def simple_filter_query_test():

    print isinstance(10.10, int)
    q = AppacitiveQuery()
    q.fields_to_return = ['f1', 'f2', 'f3']
    q.free_text_tokens = ['ft1', 'ft2', 'ft3']
    q.is_ascending = True
    q.order_by = 'orderByProperty'
    q.language = 'english'
    q.page_number = 1
    q.page_size = 200


    filter1 = filter.TagFilter.match_atleast_one(['123','qwe'])
    filter2 = filter.PropertyFilter.between('prop123', value.DateValue(datetime.date.today()), value.DateValue(datetime.date.today()))
    filter3 = filter.PropertyFilter.within_polygon('prop', value.GeoValues([value.GeoValue(10.10, -20.20), value.GeoValue(10.10, -20.20), value.GeoValue(10.10, -20.20)]))
    #q.filter = filter1
    q.filter = operator.BooleanOperator.or_query([operator.BooleanOperator.and_query([filter1, filter2]), filter3])

    print str(q)

simple_filter_query_test()