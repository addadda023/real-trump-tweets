from elasticsearch import Elasticsearch
import logging
import os
import re

# Log transport
logging.basicConfig(level=logging.INFO)


class ElasticConn:
    def __init__(self):
        self.app = None
        self.driver = None
        # self.index = None

    def init_app(self, app):
        self.app = app
        self.connect()

    def connect(self):
        bonsai = os.environ['BONSAI_URL']
        auth = re.search('https\:\/\/(.*)\@', bonsai).group(1).split(':')
        host = bonsai.replace('https://%s:%s@' % (auth[0], auth[1]), '')

        # Port
        match = re.search('(:\d+)', host)
        if match:
            p = match.group(0)
            host = host.replace(p, '')
            port = int(p.split(':')[1])
        else:
            port = 443

        # Connect to Bonsai over SSL using auth for best security:
        es_header = [{
            'host': host,
            'port': port,
            'use_ssl': True,
            'http_auth': (auth[0], auth[1])
        }]

        # Connect
        try:
            self.driver = Elasticsearch(es_header)
            # Populate index, there's only one for this application
            # self.index = list(self.driver.indices.get_alias().keys())[0]
            return self.driver
        except Exception as e:
            logging.error(e)

    def get_es(self):
        if not self.driver:
            return self.connect()
        return self.driver

    def get_index(self):
        return list(self.driver.indices.get_alias().keys())[0]

    def search(self, index, body):
        return self.driver.search(index=index, body=body)

    def insert(self, index, body):
        try:
            # self.get_es()
            es_object = self.driver.index(index=index, body=body)
            return es_object.get('_id')
        except Exception as e:
            logging.error('Error inserting {}'.format(e))
