from pyappacitive import AppacitiveObject
import datetime


def create_article_test():
    obj = AppacitiveObject()
    obj.type = 'object'
    obj.set_property('intfield', 100)
    obj.set_property('decimalfield', 20.250)
    obj.set_property('boolfield', True)
    obj.set_property('stringfield', 'hello world')
    obj.set_property('textfield', '''Objects represent your data stored inside the Appacitive platform. Every object is mapped to the type that you create via the designer in your management console. If we were to use conventional databases as a metaphor, then a type would correspond to a table and an object would correspond to one row inside that table.

The object api allows you to store, retrieve and manage all the data that you store inside Appacitive. You can retrieve individual records or lists of records based on a specific filter criteria.''')
    obj.set_property('datefield', datetime.date.today())
    obj.set_property('timefield', datetime.time.min)
    obj.set_property('datetimefield', datetime.datetime.now())
    obj.set_property('geofield', '10.10,20.20')
    obj.set_property('multifield', ['val1', 'val2', 'val3'])

    obj.create()

    assert obj.id is not None





create_article_test()