from pyappacitive import AppacitiveObject
from pyappacitive.utilities import logfilter
import datetime
import nose
import logging


def create_object_test():
    #logger = logging.getLogger('pyappacitive')
    #
    #logger.setLevel(logging.DEBUG)
    #sh = logging.StreamHandler()
    #sh.addFilter(logfilter.SlowCallLogFilter(3.0))
    #logger.addHandler(sh)
    obj = AppacitiveObject('object')
    obj.set_property('intfield', 100)
    obj.set_property('decimalfield', 20.250)
    obj.set_property('boolfield', True)
    obj.set_property('stringfield', 'hello world')
    obj.set_property('textfield', '''Objects represent your data stored inside the Appacitive platform. Every object is mapped to the type that you create via the designer in your management console. If we were to use conventional databases as a metaphor, then a type would correspond to a table and an object would correspond to one row inside that table.

The object api allows you to store, retrieve and manage all the data that you store inside Appacitive. You can retrieve individual records or lists of records based on a specific filter criteria.''')
    obj.set_property('datefield', datetime.date.today())
    obj.set_property('timefield', datetime.time.min)
    obj.set_property('datetimefield', datetime.datetime(2005,5,5,5))
    obj.set_property('geofield', '10.10,20.20')
    obj.set_property('multifield', ['val1', 'val2', 'val3'])

    resp = obj.create()
    assert resp.status.code == '200'
    assert obj.id > 0


def get_object_test():
    obj = AppacitiveObject('object')
    obj.create()

    resp = AppacitiveObject.get('object', obj.id)
    assert resp.status.code == '200'
    assert resp.object is not None


def multiget_object_test():
    object_ids = []
    for i in range(12):
        obj = AppacitiveObject('object')
        obj.create()
        object_ids.append(obj.id)

    resp = AppacitiveObject.multi_get('object', object_ids)
    assert resp.status.code == '200'
    assert hasattr(resp, 'objects')
    assert len(resp.objects) == 12


def delete_object_test():
    obj = AppacitiveObject('object')
    obj.create()
    id = obj.id
    resp = obj.delete()
    assert resp.status.code == '200'

    resp = AppacitiveObject.get('object', id)
    assert resp.status.code != '200'
    assert not hasattr(resp, 'object')


def delete_object_with_connection_test():
    assert True


def multi_delete_object_test():
    object_ids = []
    for i in range(10):
        obj = AppacitiveObject('object')
        obj.create()
        object_ids.append(obj.id)

    resp = AppacitiveObject.multi_delete('object', object_ids)
    assert resp.status.code == '200'

    for object_id in object_ids:
        resp = AppacitiveObject.get('object', object_id)
        assert resp.status.code != '200'


def update_object_test():
    obj = AppacitiveObject('object')
    obj.set_property('intfield', 100)
    obj.set_property('decimalfield', 10.10)
    obj.set_property('boolfield', False)
    obj.set_property('stringfield', 'hello world')
    obj.set_property('textfield', '''Objects represent your data stored inside the Appacitive platform. Every object is
    mapped to the type that you create via the designer in your management console. If we were to use conventional
    databases as a metaphor, then a type would correspond to a table and an object would correspond to one
    row inside that table.


                        The object api allows you to store, retrieve and manage all the data that you store inside
                        Appacitive. You can retrieve individual records or lists of records based on a specific filter
                        criteria.''')
    obj.set_property('datefield', datetime.date.today())
    obj.set_property('timefield', datetime.time.min)
    obj.set_property('datetimefield', datetime.datetime.now())
    obj.set_property('geofield', '10.10,20.20')
    obj.set_property('multifield', ['val1', 'val2', 'val3'])

    obj.create()

    obj.set_property('intfield', 200)
    obj.set_property('decimalfield', 20.20)
    obj.set_property('boolfield', True)
    obj.set_property('stringfield', 'world hello')
    obj.set_property('textfield', '''To update an existing object, you need to provide the type
    and id of the object along with the list
    of updates that are to be made. As the Appacitive platform supports
    partial updates, and update only needs the information that has
    actually changed.''')
    obj.set_property('datefield', datetime.date(1990, 5, 20))
    obj.set_property('timefield', datetime.time.max)
    obj.set_property('datetimefield', datetime.datetime(2000,2,3))
    obj.set_property('geofield', '30.30, 40.40')
    obj.set_property('multifield', ['val4', 'val5', 'val6'])

    resp = obj.update()
    assert resp.status.code == '200'




