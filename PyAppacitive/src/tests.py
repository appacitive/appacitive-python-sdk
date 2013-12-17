__author__ = 'sathley'

import json
from object import AppacitiveObject
from connection import AppacitiveConnection

# conn = AppacitiveConnection()
#conn.relation_type = 'user_restaurant'
#conn.set_property('rating', 3)
#conn.endpoint_b['objectid'] = 45530024245331928
#conn.endpoint_a['objectid'] = 45532199466959193
#conn.endpoint_a['label'] = 'user'
#conn.endpoint_b['label'] = 'restaurant'
#
#conn.create()
#print conn.get_json()
#
#
#conn1 = AppacitiveConnection.get('user_restaurant', conn.id)
#print conn1.get_json()
#
#
#conn1.delete()
#
#conn2 = AppacitiveConnection.get('user_restaurant', conn.id)
#print conn2.get_json()

conns = AppacitiveConnection.find('user_restaurant', None)

print conns