__author__ = 'sathley'

from pyappacitive.utilities import http, urlfactory
from response import AppacitiveResponse
from utilities import customjson


class AppacitiveEmail(object):
    def __init__(self):
        pass

    @staticmethod
    def send_raw_email(to, subject, body, cc=None, bcc=None, is_body_html=False, smtp=None, from_email=None, reply_to_email=None):
        payload = {}
        payload['to'] = to
        payload['cc'] = cc
        payload['bcc'] = bcc
        payload['subject'] = subject
        payload['body'] = {
            'content': body,
            'ishtml': is_body_html
        }

        if smtp is not None:
            payload['smtp'] = smtp
        if from_email is not None:
            payload['from'] = from_email
        if reply_to_email is not None:
            payload['replyto'] = reply_to_email

        url = urlfactory.email_urls["send"]()
        headers = urlfactory.get_headers()

        api_response = http.post(url, headers, customjson.serialize(payload))
        return AppacitiveResponse(api_response['status'])

    @staticmethod
    def send_templated_email(to, subject, template_name, template_fillers, cc=None, bcc=None, is_body_html=False, smtp=None, from_email=None, reply_to_email=None):
        payload = {}
        payload['to'] = to
        payload['cc'] = cc
        payload['bcc'] = bcc
        payload['subject'] = subject
        payload['body'] = {
            'templatename': template_name,
            'data': template_fillers,
            'ishtml': is_body_html
        }

        if smtp is not None:
            payload['smtp'] = smtp
        if from_email is not None:
            payload['from'] = from_email
        if reply_to_email is not None:
            payload['replyto'] = reply_to_email

        url = urlfactory.email_urls["send"]()
        headers = urlfactory.get_headers()

        api_response = http.post(url, headers, customjson.serialize(payload))
        return AppacitiveResponse(api_response['status'])


