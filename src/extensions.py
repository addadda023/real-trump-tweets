from .elasticsearch_db import ElasticConn
import logging

# Log transport
logging.basicConfig(level=logging.INFO)

es = ElasticConn()