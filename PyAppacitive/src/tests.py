__author__ = 'sathley'

import json


from object import AppacitiveObject

resp = AppacitiveObject.multi_delete('restaurant',['45530091000825605','45530370168455584'])

print resp
#json_str = '''{
#	"object": {
#		"__id": "45519880301184560",
#		"__type": "restaurant",
#		"__createdby": "System",
#		"__lastmodifiedby": "System",
#		"__typeid": "44869167526052794",
#		"__revision": "1",
#		"__tags": ["1", "2", "3"],
#		"__utcdatecreated": "2013-12-16T10:38:59.1972000Z",
#		"__utclastupdateddate": "2013-12-16T10:38:59.1972000Z",
#		"name": "name",
#		"address": "123456il",
#		"location": "18.534064,73.899551",
#		"__attributes": {
#		    "1": "2",
#		    "3": "4"
#		}
#	},
#	"status": {
#		"code": "200",
#		"referenceid": "e9454ddb-5510-4aa4-b587-d2a36dd7caae",
#		"version": "1.0"
#	}
#}'''
#
#yoyo =  AppacitiveObject.get_object(json.loads(json_str)['object'])
#print yoyo.get_json()