from pyappacitive import AppacitiveObject, AppacitiveConnection
import datetime
import nose


def create_connection_with_object_ids_test():
    obj1 = AppacitiveObject('object')
    obj1.create()

    obj2 = AppacitiveObject('object')
    obj2.create()

    conn = AppacitiveConnection('sibling')
    conn.set_property('field1', 'hello')
    conn.set_property('field2', 101)

    conn.endpoint_a.objectid = obj1.id
    conn.endpoint_a.label = 'object'
    conn.endpoint_b.objectid = obj2.id
    conn.endpoint_b.label = 'object'
    resp = conn.create()

    assert resp.status_code == '200'
    assert conn.id != 0


def create_connection_with_objects_test():
    obj1 = AppacitiveObject('object')

    obj2 = AppacitiveObject('object')

    conn = AppacitiveConnection('sibling')
    conn.set_property('field1', 'hello')
    conn.set_property('field2', 101)

    conn.endpoint_a.object = obj1
    conn.endpoint_a.label = 'object'
    conn.endpoint_b.object = obj2
    conn.endpoint_b.label = 'object'
    resp = conn.create()

    assert resp.status_code == '200'
    assert conn.id != 0
    assert conn.endpoint_a.objectid > 0
    assert conn.endpoint_b.objectid > 0

    assert conn.endpoint_a.object is not None
    assert conn.endpoint_b.object is not None

    assert conn.endpoint_a.object.id > 0
    assert conn.endpoint_b.object.id > 0


def get_connection_test():
    obj1 = AppacitiveObject('object')
    obj1.create()

    obj2 = AppacitiveObject('object')
    obj2.create()

    conn = AppacitiveConnection('sibling')
    conn.set_property('field1', 'hello')
    conn.set_property('field2', 101)

    conn.endpoint_a.objectid = obj1.id
    conn.endpoint_a.label = 'object'
    conn.endpoint_b.objectid = obj2.id
    conn.endpoint_b.label = 'object'
    conn.create()

    resp = AppacitiveConnection.get('sibling', conn.id)

    assert resp.status_code == '200'
    assert hasattr(resp, 'connection')
    assert resp.connection.id == conn.id


def multiget_connection_test():
    conn_ids = []
    for i in range(12):
        obj1 = AppacitiveObject('object')
        obj2 = AppacitiveObject('object')
        conn = AppacitiveConnection('sibling')
        conn.endpoint_a.object = obj1
        conn.endpoint_a.label = 'object'
        conn.endpoint_b.object = obj2
        conn.endpoint_b.label = 'object'
        resp = conn.create()
        conn_ids.append(conn.id)

    resp = AppacitiveConnection.multi_get('sibling', conn_ids)
    assert resp.status_code == '200'
    assert hasattr(resp, 'connections')
    assert len(resp.connections) == 12


def delete_connection_test():
    obj1 = AppacitiveObject('object')
    obj1.create()

    obj2 = AppacitiveObject('object')
    obj2.create()

    conn = AppacitiveConnection('sibling')
    conn.set_property('field1', 'hello')
    conn.set_property('field2', 101)

    conn.endpoint_a.objectid = obj1.id
    conn.endpoint_a.label = 'object'
    conn.endpoint_b.objectid = obj2.id
    conn.endpoint_b.label = 'object'
    conn.create()
    id = conn.id

    resp = conn.delete()
    assert resp.status_code == '200'

    resp = AppacitiveConnection.get('sibling', id)
    assert resp.status_code != '200'


def multi_delete_connection_test():
    conn_ids = []
    for i in range(5):
        obj1 = AppacitiveObject('object')
        obj1.create()

        obj2 = AppacitiveObject('object')
        obj2.create()

        conn = AppacitiveConnection('sibling')
        conn.set_property('field1', 'hello')
        conn.set_property('field2', 101)
        conn.set_attribute('a1', 'v1')
        conn.add_tag('1')
        conn.endpoint_a.objectid = obj1.id
        conn.endpoint_a.label = 'object'
        conn.endpoint_b.objectid = obj2.id
        conn.endpoint_b.label = 'object'
        conn.create()
        conn_ids.append(conn.id)

    resp = AppacitiveConnection.multi_delete('sibling', conn_ids)
    assert resp.status_code == '200'

    for conn_id in conn_ids:
        resp = AppacitiveConnection.get('sibling', conn_id)
        assert resp.status_code != '200'


def update_connection_test():
    obj1 = AppacitiveObject('object')
    obj1.create()

    obj2 = AppacitiveObject('object')
    obj2.create()

    conn = AppacitiveConnection('sibling')
    conn.set_property('field1', 'hello')
    conn.set_property('field2', 101)
    conn.endpoint_a.objectid = obj1.id
    conn.endpoint_a.label = 'object'
    conn.add_tag('1')
    conn.set_attribute('a1', 'v1')
    conn.endpoint_b.objectid = obj2.id
    conn.endpoint_b.label = 'object'
    conn.create()

    conn.set_property('field1', 'world')
    conn.set_property('field2', 202)

    conn.remove_tag('1')
    conn.remove_tag('random')
    conn.add_tag('2')
    conn.add_tag('3')

    conn.remove_attribute('a1')
    conn.remove_attribute('random')
    conn.set_attribute('a2', 'v2')

    resp = conn.update()
    assert resp.status_code == '200'

    assert conn.get_property('field1') == 'world'
    assert conn.get_property('field2') == '202'
    assert conn.get_attribute('a1') == None
    assert conn.get_attribute('a2') == 'v2'
    assert conn.tag_exists('1') == False
    assert conn.tag_exists('2') == True


