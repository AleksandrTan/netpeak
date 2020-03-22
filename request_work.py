"""
    Class for queries
"""
import requests
from requests.exceptions import Timeout


class Query:
    def __init__(self, url_target):
        self.url_target = url_target

    def do_query_post(self, param: str) -> dict:
        try:
            result = requests.post(self.url_target, data={'q': param}, timeout=(3, 3), allow_redirects=False)
        except (Timeout, requests.ConnectTimeout) as eror:
            return {'querys': '', 'products': '', 'categories': '', 'status': 'fails',
                    'message': f'bad server status {eror}'}
        data_json = result.json()
        if result.status_code == 200:
            if not result.text:
                return {'querys': '', 'products': '', 'categories': '', 'status': 'fail',
                        'message': 'empty data'}
            return self.parse_response(data_json)
    """
        Parse result
    """
    def parse_response(self, data: dict) -> dict:
        if type(data) == list:
            return {'querys': '', 'products': '', 'categories': '', 'status': 'fail',
                    'message': 'empty response'}

        if data.get('query', 0) and data.get('products', 0) and data.get('categories', 0):
            query = ', '.join(data['query'])
            products = ','.join([text['name'] for text in data['products']])
            categories = ','.join([text['name'] for text in data['categories']])
            return {'querys': query, 'products': products, 'categories': categories, 'status': 'ok',
                    'message': 'successful request'}

        if not data.get('query', 0) and data.get('products', 0) and data.get('categories', 0):
            query = ''
            products = ','.join([text['name'] for text in data['products']])
            categories = ','.join([text['name'] for text in data['categories']])
            return {'querys': query, 'products': products, 'categories': categories, 'status': 'ok',
                    'message': 'successful request'}

        if not data.get('query', 0) and not data.get('products', 0) and data.get('categories', 0):
            query = ''
            products = ''
            categories = ','.join([text['name'] for text in data['categories']])
            return {'querys': query, 'products': products, 'categories': categories, 'status': 'ok',
                    'message': 'successful request'}

        if not data.get('query', 0) and data.get('products', 0) and not data.get('categories', 0):
            query = ''
            products = ','.join([text['name'] for text in data['products']])
            categories = ''
            return {'querys': query, 'products': products, 'categories': categories, 'status': 'ok',
                    'message': 'successful request'}

        return {'querys': '', 'products': '', 'categories': '', 'status': 'fail',
                'message': 'bad status server'}