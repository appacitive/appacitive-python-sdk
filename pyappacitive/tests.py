__author__ = 'sathley'

from pyappacitive.object import AppacitiveObject


#u1 = AppacitiveUser()
#u1.firstname = 'sathley'
#u1.username = 'qwer'
#u1.password = 'test123!@#'
#u1.email = 'sathley@appacitive.com'
#u1.lastname = 'athley'
#u1.birthdate = str(datetime.date.today())
#u1.create()
#
#print u1.get_json()


r1 = AppacitiveObject()
r1.type = 'restaurant'
r1.set_property('name', 'pizza')
r1.create()


print r1.get_json()