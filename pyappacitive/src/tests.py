__author__ = 'sathley'

import json
from object import AppacitiveObject
from connection import AppacitiveConnection
from appacitive_email import Email
from user import AppacitiveUser
import datetime


u1 = AppacitiveUser()
u1.firstname = 'sathley'
u1.username = 'qwe'
u1.password = 'test123!@#'
u1.email = 'sathley@appacitive.com'
u1.lastname = 'athley'

u1.create()

print u1.get_json()