import random

import requests

from pypubmed.util.logger import MyLogger


class WebRequest(object):

    logger = MyLogger('WebRequest')

    UA_LIST = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
        'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
    ]

    @classmethod
    def get_response(cls, url, method='GET', **kwargs):
        if 'headers' not in kwargs or 'User-Agent' not in kwargs['headers']:
            kwargs['headers'] = {'User-Agent': random.choice(cls.UA_LIST)}

        resp = requests.request(method, url, **kwargs)
        # cls.logger.info(resp.url)
        
        if resp.status_code != 200:
            cls.logger.warning('status {}: {} [params: {}, data: {}]'.format(
                resp.status_code, url, kwargs.get('params'), kwargs.get('data')))

        if resp.status_code not in (200, 400):
            cls.logger.error(resp.text)
            exit(1)

        return resp
