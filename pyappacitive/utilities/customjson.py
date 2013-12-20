__author__ = 'sathley'
from json import JSONEncoder, dumps, loads
import datetime
import types


class CustomEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.time):
            # convert time to hh:mm:ss:ffffff and the add a trailing 0
            return obj.strftime('%H:%M:%S.%f') + '0'
        if isinstance(obj, datetime.date):
            if isinstance(obj, datetime.datetime) is False:
                return str(obj)
            else:
                # convert datetime to iso and add the trailing 0Z
                return obj.strftime('%Y-%m-%dT%H:%M:%S.%f') + '0Z'

        return JSONEncoder.default(self, obj)


def serialize(obj):
    # Custom encode object for datetime magnificence
    serialized_json = dumps(obj, cls=CustomEncoder)

    # Reload json string to perform further magnificence into the unknown realm
    reloaded_json_object = loads(serialized_json)

    # oh yeaaaaaahh !!!!!
    stringified_json_object = {k: str(v) if not isinstance(v, types.ListType) else v for k, v in
                               reloaded_json_object.iteritems()}

    # Re serialize object into json for magnificence level over 9000
    return dumps(stringified_json_object)


def deserialize(obj):
    # I am here ladies !!!
    return loads(obj)