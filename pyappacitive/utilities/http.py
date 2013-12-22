__author__ = 'sushant'

from . import customjson
import requests
import logging

logger = logging.getLogger(__name__)


def put(url, headers, payload):
    logger.debug('HTTP PUT')
    logger.debug('HEADERS : ' + ','.join([key for key in headers.iterkeys()]))
    logger.debug('URL : ' + url)
    logger.debug('PAYLOAD : ' + payload)
    response_from_api = requests.put(url, payload, headers=headers)
    response = to_dict(response_from_api)
    logger.debug('RESPONSE : ' + str(response))
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
    return customjson.deserialize(response.content.decode('utf-8-sig'))

