__author__ = 'sathley'
import logging


class SlowCallLogFilter(logging.Filter):
    def __init__(self, duration):
        self.duration = duration

    def filter(self, rec):
        if hasattr(rec, 'TIME_TAKEN') is False:
            return True
        if rec.TIME_TAKEN >= self.duration:
            return True
        else:
            return False


class FailedRequestsLogFilter(logging.Filter):
    def __init__(self):
        pass

    def filter(self, rec):
        if hasattr(rec, 'RESPONSE') is False:
            return True
        status1 = rec.RESPONSE.get('status', None)
        if status1 is not None:
            if status1["code"] == '200':
                return False
            else:
                return True
        else:
            return True