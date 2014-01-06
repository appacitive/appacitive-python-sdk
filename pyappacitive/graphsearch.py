from . import nodehelper
from .utilities import http, urlfactory

__author__ = 'sathley'

from .utilities import customjson
import logging

graph_logger = logging.getLogger(__name__)
graph_logger.addHandler(logging.NullHandler())


class AppacitiveGraphSearch(object):
    def __init__(self):
        pass

    @staticmethod
    def project(query_name, id_list, place_holder_fillers=None):
        url = urlfactory.graph_search_urls['project'](query_name)
        headers = urlfactory.get_headers()
        stringified_id_list = [str(i) for i in id_list]
        payload = {
            'ids': stringified_id_list,
            'placeholders': place_holder_fillers
        }
        graph_logger.info('Projection graph query')
        resp = http.post(url, headers, customjson.serialize(payload))

        for k, v in resp.iteritems():
            if k != 'status':
                return AppacitiveGraphSearch.__parse_projection_result(v['values'])


    @staticmethod
    def filter(query_name, place_holder_fillers=None):
        url = urlfactory.graph_search_urls['filter'](query_name)
        headers = urlfactory.get_headers()
        payload = {
            'placeholders': place_holder_fillers
        }
        graph_logger.info('Filter graph query')
        api_response = http.post(url, headers, customjson.serialize(payload))
        return [int(id) for id in api_response['ids']]

    @staticmethod
    def __parse_projection_result(values):
        nodes = []
        for val in values:
            nodes.append(nodehelper.convert_node(val))
        return nodes



