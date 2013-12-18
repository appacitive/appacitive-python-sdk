__author__ = 'sathley'

import json
from object import AppacitiveObject
from connection import AppacitiveConnection
from appacitive_email import Email
import datetime


d = datetime.date.today()
dt = datetime.datetime.today()


print isinstance(d, datetime.date)
print isinstance(d, datetime.datetime)

print isinstance(dt, datetime.date) and not isinstance(dt, datetime.datetime)
print isinstance(dt, datetime.datetime)

print str(d)
print str(dt)
