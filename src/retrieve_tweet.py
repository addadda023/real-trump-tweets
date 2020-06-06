from .extensions import es
from .utils import process_str
import logging
import random
import time

# Log transport
logging.basicConfig(level=logging.INFO)

# Query body template
# To do: store body template in json file
body = \
        {
            "query": {
                "function_score": {
                    "query": {
                        "match": {
                            "tweet": {
                                "query": None
                            }
                        }
                    },
                    "boost": "5",
                    "random_score": {},
                    "boost_mode": "multiply"
                }
            },
            "from": 0,
            "size": 1
        }


def search_tweets(query):
    driver = es.get_es()
    index = list(driver.indices.get_alias().keys())[0]

    # Process query
    query = process_str(query)
    # Populate body
    if 1 <= len(query) <= 100:
        body['query']['function_score']['query']['match']['tweet']['query'] = query
    else:
        # Query is too short or too long, return a random tweet
        list_of_queries = ['MAGA', 'America', 'Trump', 'China', 'Russia', 'Twitter', 'Thank you']
        body['query']['function_score']['query']['match']['tweet']['query'] = random.choice(list_of_queries)

    # Search
    res = driver.search(index=index, body=body)
    hits = res['hits']['total']['value']
    logging.info('Got %d hits' % hits)

    # :)
    time.sleep(1.5)
    if hits >= 1:
        # logging.info("%(timestamp)s %(author)s: %(tweet)s" % res['hits']['hits'][0]['_source'])
        return res['hits']['hits'][0]["_source"]['tweet']
    else:
        return 'Oops couldnt understand. Try again.'
