from pyappacitive import AppacitiveObject, AppacitiveConnection, AppacitiveQuery, TagFilter
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

    assert resp.status.code == '200'
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

    assert resp.status.code == '200'
    assert conn.id != 0
    assert conn.endpoint_a.objectid > 0
    assert conn.endpoint_b.objectid > 0

    assert conn.endpoint_a.object is not None
    assert conn.endpoint_b.object is not None

    assert conn.endpoint_a.object.id > 0
    assert conn.endpoint_b.object.id > 0


def create_using_fluent_syntax_test():
    obj1 = AppacitiveObject('object')
    obj1.create()

    obj2 = AppacitiveObject('object')
    obj2.create()

    conn = AppacitiveConnection('sibling').from_created_object_id('object', obj1.id).to_created_object_id('object', obj2.id)
    resp = conn.create()
    assert resp.status.code == '200'
    assert conn.id != 0


def create_using_fluent_syntax_test_2():
    obj1 = AppacitiveObject('object')

    obj2 = AppacitiveObject('object')

    conn = AppacitiveConnection('sibling').from_new_object('object', obj1).to_new_object('object', obj2)
    resp = conn.create()
    assert resp.status.code == '200'
    assert conn.id != 0



def get_connection_test():
    obj1 = AppacitiveObject('object')
    obj1.create()

    obj2 = AppacitiveObject('object')
    obj2.create()

    conn = AppacitiveConnection('sibling')

    conn.endpoint_a.objectid = obj1.id
    conn.endpoint_a.label = 'object'
    conn.endpoint_b.objectid = obj2.id
    conn.endpoint_b.label = 'object'
    conn.create()

    resp = AppacitiveConnection.get('sibling', conn.id)

    assert resp.status.code == '200'
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
    assert resp.status.code == '200'
    assert hasattr(resp, 'connections')
    assert len(resp.connections) == 12


def delete_connection_test():
    obj1 = AppacitiveObject('object')
    obj1.create()

    obj2 = AppacitiveObject('object')
    obj2.create()

    conn = AppacitiveConnection('sibling')

    conn.endpoint_a.objectid = obj1.id
    conn.endpoint_a.label = 'object'
    conn.endpoint_b.objectid = obj2.id
    conn.endpoint_b.label = 'object'
    conn.create()
    id = conn.id

    resp = conn.delete()
    assert resp.status.code == '200'

    resp = AppacitiveConnection.get('sibling', id)
    assert resp.status.code != '200'


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
    assert resp.status.code == '200'

    for conn_id in conn_ids:
        resp = AppacitiveConnection.get('sibling', conn_id)
        assert resp.status.code != '200'


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
    assert resp.status.code == '200'

    assert conn.get_property('field1') == 'world'
    assert conn.get_property('field2') == '202'
    assert conn.get_attribute('a1') == None
    assert conn.get_attribute('a2') == 'v2'
    assert conn.tag_exists('1') == False
    assert conn.tag_exists('2') == True


def fetch_latest_test():
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

    resp = AppacitiveConnection.get('sibling', conn.id)
    conn1 = resp.connection
    conn1.add_tag('2')
    conn1.remove_tag('1')

    conn1.update()

    conn.add_tag('3')
    response = conn.fetch_latest()
    assert response.status.code == '200'
    assert conn.tag_exists('2')
    assert conn.tag_exists('1') is False
    assert conn.tag_exists('3') is False


def find_connection_test():
    obj1 = AppacitiveObject('object')
    obj1.create()

    obj2 = AppacitiveObject('object')
    obj2.create()

    conn = AppacitiveConnection('sibling')
    conn.set_property('field1', 'hello')
    conn.set_property('field2', 101)
    conn.endpoint_a.objectid = obj1.id
    conn.endpoint_a.label = 'object'
    conn.add_tags(['1', '4', '5'])
    conn.set_attribute('a1', 'v1')
    conn.endpoint_b.objectid = obj2.id
    conn.endpoint_b.label = 'object'
    conn.create()

    query = AppacitiveQuery()
    query.filter = TagFilter.match_one_or_more(['1', '2', '3'])
    response = AppacitiveConnection.find('sibling', query)
    assert response.status.code == '200'
    assert hasattr(response, 'connections')
    assert len(response.connections) > 0





