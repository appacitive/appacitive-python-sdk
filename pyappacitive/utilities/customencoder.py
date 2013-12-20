__author__ = 'sathley'
from json import JSONEncoder, dumps
import datetime


class CustomEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.time):
            # convert time to hh:mm:ss:ffffff and the add a trailing 0
            return obj.strftime("%H:%M:%S.%f") + '0'
        if isinstance(obj, datetime.date):
            if isinstance(obj, datetime.datetime) is False:
                return str(obj)
            else:
                # convert datetime to iso and add  the trailing 0Z
                return str(obj.isoformat()) + '0Z'

        return JSONEncoder.default(self, obj)

