__author__ = 'sushant'

import json
import requests


def put(url, headers, payload):
    response = requests.put(url, payload, headers=headers)
    return to_dict(response)


def post(url, headers, payload):
    response = requests.post(url, payload, headers=headers)
    return to_dict(response)


def delete(url, headers):
    response = requests.delete(url, headers=headers)
    return to_dict(response)


def get(url, headers):
    response = requests.get(url, headers=headers)
    return to_dict(response)


def to_dict(response):
    return json.loads(response.content.decode('utf-8-sig'))

