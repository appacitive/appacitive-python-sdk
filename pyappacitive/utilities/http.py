__author__ = 'sushant'

import json
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def put(url, headers, payload):
    response_from_api = requests.put(url, payload, headers=headers)
    response = to_dict(response_from_api)
    return response


def post(url, headers, payload):
    response_from_api = requests.post(url, payload, headers=headers)
    response = to_dict(response_from_api)
    return response


def delete(url, headers):
    response_from_api = requests.delete(url, headers=headers)
    response = to_dict(response_from_api)
    return response


def get(url, headers):
    response_from_api = requests.get(url, headers=headers)
    response = to_dict(response_from_api)
    return response


def to_dict(response):
    return json.loads(response.content.decode('utf-8-sig'))

