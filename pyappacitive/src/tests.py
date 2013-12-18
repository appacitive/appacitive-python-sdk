__author__ = 'sathley'

import json
from object import AppacitiveObject
from connection import AppacitiveConnection
from appacitive_email import Email


Email.send_raw_email(['sathley@appacitive.com'],[],[],'hello from pysdk', 'Hello')
