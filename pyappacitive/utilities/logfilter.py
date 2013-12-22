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