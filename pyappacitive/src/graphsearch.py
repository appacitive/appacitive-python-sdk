__author__ = 'sathley'

from utilities import urlfactory, http
import json


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
        resp = http.post(url, headers, json.dumps(payload))
        if resp['status']['code'] != '200':
            return None
        for k, v in resp.iteritems():
            if k != 'status':
                return resp[k]

    @staticmethod
    def filter(query_name, query_dict):
        url = urlfactory.graph_search_urls['filter'](query_name)
        headers = urlfactory.get_headers()
        payload = {
            'placeholders': query_dict
        }

        resp = http.post(url, headers, json.dumps(payload))
        if resp['status']['code'] == '200':
            return resp['ids']


