from pyappacitive.utilities import http, urlfactory

__author__ = 'sathley'

from utilities import customjson
from response import AppacitiveResponse


class GraphSearch(object):
    def __init__(self):
        pass

    @staticmethod
    def project(query_name, id_list, query_dict):
        url = urlfactory.graph_search_urls['project'](query_name)
        headers = urlfactory.get_headers()
        payload = {
            'ids': id_list,
            'placeholders': query_dict
        }
        resp = http.post(url, headers, customjson.serialize(payload))
        response = AppacitiveResponse(resp['status'])
        if response.status_code == '200':
            for k, v in resp.iteritems():
                if k is not 'status':
                    response.__setattr__(k, v)
        return response

    @staticmethod
    def filter(query_name, query_dict):
        url = urlfactory.graph_search_urls['filter'](query_name)
        headers = urlfactory.get_headers()
        payload = {
            'placeholders': query_dict
        }

        api_response = http.post(url, headers, customjson.serialize(payload))
        response = AppacitiveResponse(api_response['status'])
        if response.status_code == '200':
            response.ids = api_response['ids']
        return response


