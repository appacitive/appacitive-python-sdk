from pyappacitive import nodehelper
from pyappacitive.utilities import http, urlfactory

__author__ = 'sathley'

from utilities import customjson
from response import AppacitiveResponse


class AppacitiveGraphSearch(object):
    def __init__(self):
        pass

    @staticmethod
    def project(query_name, id_list, query_dict=None):
        url = urlfactory.graph_search_urls['project'](query_name)
        headers = urlfactory.get_headers()
        stringified_id_list = [str(i) for i in id_list]
        payload = {
            'ids': stringified_id_list,
            'placeholders': query_dict
        }
        resp = http.post(url, headers, customjson.serialize(payload))
        response = AppacitiveResponse(resp['status'])

        if response.status.code == '200':
            for k, v in resp.iteritems():
                if k != 'status':
                    response.nodes = AppacitiveGraphSearch.parse_projection_result(v['values'])

        return response


    @staticmethod
    def filter(query_name, query_dict=None):
        url = urlfactory.graph_search_urls['filter'](query_name)
        headers = urlfactory.get_headers()
        payload = {
            'placeholders': query_dict
        }

        api_response = http.post(url, headers, customjson.serialize(payload))
        response = AppacitiveResponse(api_response['status'])
        if response.status.code == '200':
            response.ids = api_response['ids']
        return response

    @staticmethod
    def parse_projection_result(values):
        nodes = []
        for val in values:
            nodes.append(nodehelper.convert_node(val))
        return nodes



