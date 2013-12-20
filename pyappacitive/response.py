__author__ = 'sathley'


class Response(object):
    def __init__(self, status):
        self.status_code = status['code']
        self.status_message = status.get('message', None)
        self.additional_messages = status.get('additionalmessages', [])
        self.reference_id = status['referenceid']
        self.version = status['version']


