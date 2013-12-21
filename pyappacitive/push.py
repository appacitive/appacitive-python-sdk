__author__ = 'sathley'

from utilities import urlfactory, http, customjson
from error import ValidationError
from response import Response


class PushNotification(object):
    def __init__(self, push=None):

        if push is not None:
            self.id = int(push.get('id', 0))
            self.isbroadcast = push.get('isbroadcast', None)
            self.alert = push.get('alert', None)
            self.badge = push.get('badge', None)
            self.expireafter = int(push.get('expireafter', 0))
            self.devicecount = int(push.get('devicecount', 0))
            self.successfulcount = int(push.get('successfulcount', 0))
            self.failurecount = int(push.get('failurecount', 0))
            self.status = push.get('status', None)
            self.timestamp = push.get('timestamp', None)
            self.lastmodifieddate = push.get('lastmodifieddate', None)
            self.customdata = push.get('customdata', {})
            self.devicedata = push.get('devicedata', {})
        else:
            self.id = 0
            self.isbroadcast = None
            self.alert = None
            self.badge = None
            self.expireafter = None
            self.customdata = {}
            self.devicedata = {}
            self.devicecount = 0
            self.successfulcount = 0
            self.failurecount = 0
            self.status = None
            self.timestamp = None
            self.lastmodifieddate = None


    @property
    def id(self):
        return self.get_property('id')

    @id.setter
    def id(self, value):
        self.set_property('id', value)

    @property
    def isbroadcast(self):
        return self.get_property('isbroadcast')

    @isbroadcast.setter
    def isbroadcast(self, value):
        self.set_property('isbroadcast', value)

    @property
    def alert(self):
        return self.get_property('alert')

    @alert.setter
    def alert(self, value):
        self.set_property('alert', value)

    @property
    def badge(self):
        return self.get_property('badge')

    @badge.setter
    def badge(self, value):
        self.set_property('badge', value)

    @property
    def expireafter(self):
        return self.get_property('expireafter')

    @expireafter.setter
    def expireafter(self, value):
        self.set_property('expireafter', value)

    @property
    def customdata(self):
        return self.get_property('customdata')

    @customdata.setter
    def customdata(self, value):
        self.set_property('customdata', value)

    @property
    def devicedata(self):
        return self.get_property('devicedata')

    @devicedata.setter
    def devicedata(self, value):
        self.set_property('devicedata', value)

    @property
    def devicecount(self):
        return self.get_property('devicecount')

    @devicecount.setter
    def devicecount(self, value):
        self.set_property('devicecount', value)

    @property
    def successfulcount(self):
        return self.get_property('successfulcount')

    @successfulcount.setter
    def successfulcount(self, value):
        self.set_property('successfulcount', value)

    @property
    def failurecount(self):
        return self.get_property('failurecount')

    @failurecount.setter
    def failurecount(self, value):
        self.set_property('failurecount', value)

    @property
    def status(self):
        return self.get_property('status')

    @status.setter
    def status(self, value):
        self.set_property('status', value)

    @property
    def timestamp(self):
        return self.get_property('timestamp')

    @timestamp.setter
    def timestamp(self, value):
        self.set_property('timestamp', value)

    @property
    def lastmodifieddate(self):
        return self.get_property('lastmodifieddate')

    @lastmodifieddate.setter
    def lastmodifieddate(self, value):
        self.set_property('lastmodifieddate', value)

    @staticmethod
    def broadcast(platform_options=None, data=None, expire_after=None):
        push_request = {
            'broadcast': True
        }

        if platform_options is not None:
            push_request['platformoptions'] = platform_options

        if data is not None:
            push_request['data'] = data

        if expire_after is not None:
            push_request['expire_after'] = expire_after

        url = urlfactory.push_urls['send']()
        headers = urlfactory.get_headers()

        payload = customjson.serialize(push_request)

        api_response = http.post(url, headers, payload)
        return Response(api_response['status'])


    @staticmethod
    def send_to_channels(channels, platform_options=None, data=None, expire_after=None):
        push_request = {
            'channels': channels
        }

        if platform_options is not None:
            push_request['platformoptions'] = platform_options

        if data is not None:
            push_request['data'] = data

        if expire_after is not None:
            push_request['expire_after'] = expire_after

        url = urlfactory.push_urls['send']()
        headers = urlfactory.get_headers()

        payload = customjson.serialize(push_request)

        response = http.post(url, headers, payload)
        return Response(response['status'])

    @staticmethod
    def send_to_specific_devices(device_ids, platform_options=None, data=None, expire_after=None):
        push_request = {
            'deviceids': device_ids
        }

        if platform_options is not None:
            push_request['platformoptions'] = platform_options

        if data is not None:
            push_request['data'] = data

        if expire_after is not None:
            push_request['expire_after'] = expire_after

        url = urlfactory.push_urls['send']()
        headers = urlfactory.get_headers()

        payload = customjson.serialize(push_request)

        response = http.post(url, headers, payload)
        return Response(response['status'])

    @staticmethod
    def send_using_query(query, platform_options=None, data=None, expire_after=None):
        push_request = {
            'query': str(query)
        }

        if platform_options is not None:
            push_request['platformoptions'] = platform_options

        if data is not None:
            push_request['data'] = data

        if expire_after is not None:
            push_request['expire_after'] = expire_after

        url = urlfactory.push_urls['send']()
        headers = urlfactory.get_headers()

        payload = customjson.serialize(push_request)

        response = http.post(url, headers, payload)
        return Response(response['status'])

    @staticmethod
    def send(platform_options, data, expire_after, **kwargs):
        push_request = {}
        for key, val in kwargs:
            push_request[key] = val

        if platform_options is not None:
            push_request['platformoptions'] = platform_options

        if data is not None:
            push_request['data'] = data

        if expire_after is not None:
            push_request['expire_after'] = expire_after

        url = urlfactory.push_urls['send']()
        headers = urlfactory.get_headers()

        payload = customjson.serialize(push_request)

        response = http.post(url, headers, payload)
        return Response(response['status'])

    @staticmethod
    def get_notification_by_id(notification_id):

        if notification_id is None:
            raise ValidationError('Notification id is required to fetch push notification.')

        url = urlfactory.push_urls['get'](notification_id)
        headers = urlfactory.get_headers()

        api_response = http.get(url, headers)
        response = Response(api_response['status'])

        if response.status_code == '200':
            response.notification = PushNotification(api_response['pushnotification'])

    @staticmethod
    def get_all_notification():

        url = urlfactory.push_urls['get_all']()
        headers = urlfactory.get_headers()

        api_response = http.get(url, headers)
        response = Response(api_response['status'])

        if response.status_code == '200':
            return_notifications = []
            for notification in api_response['pushnotifications']:
                if notification:
                    return_notifications.append(PushNotification(notification))
            response.notifications = return_notifications
            return response


