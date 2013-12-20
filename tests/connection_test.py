from pyappacitive import AppacitiveObject, AppacitiveConnection
import datetime
import nose


def create_connection_with_object_ids_test():
    obj1 = AppacitiveObject('object')
    obj1.create()

    obj1 = AppacitiveObject('object')
    obj1.create()

    conn = AppacitiveConnection('sibling')
    conn.set_property('field1', 'hello')
    conn.set_property('field2', 101)

    conn.endpoint_a['id']
    resp = conn.create()

    assert resp.status_code == '200'
    assert conn.id != 0


def get_connection_test():
    pass


def multiget_connection_test():
    pass


def delete_connection_test():
    pass


def multi_delete_connection_test():
    pass


def update_connection_test():
    pass


