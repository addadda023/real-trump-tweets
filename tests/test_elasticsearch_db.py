import unittest
from src.elasticsearch_db import ElasticConn
from elasticmock import elasticmock


class TestEsDb(unittest.TestCase):

    @elasticmock
    def test_create_and_read_object(self):
        index = 'text-index'
        expected_document = {
            'foo': 'bar'
        }

        # Instantiate service
        es = ElasticConn()
        driver = es.get_es()
        id = es.insert(index, expected_document)
        self.assertIsNotNone(id)


