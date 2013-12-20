__author__ = 'sathley'


class Response(object):
    def __init__(self, status):
        self.status_code = status['code']

        message = status.get('message', None)
        if message is not None:
            self.status_message = message

        additional_messages = status.get('additionalmessages', [])
        if additional_messages is not None:
            self.additional_messages = additional_messages

        self.reference_id = status['referenceid']
        self.version = status['version']


