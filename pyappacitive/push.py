__author__ = 'sathley'

from utilities import urlfactory, http, customjson
from error import ValidationError
from response import Response


class PushNotifications(object):
    def __init__(self):
        pass

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
            response.notification = api_response['pushnotification']

    @staticmethod
    def get_all_notification():

        url = urlfactory.push_urls['get_all']()
        headers = urlfactory.get_headers()

        api_response = http.get(url, headers)
        response = Response(api_response['status'])

        if response.status_code == '200':
            response.notification = api_response['pushnotifications']


