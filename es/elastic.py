from settings import ES_PASSWORD,ES_URL,ES_USER
from elasticsearch import Elasticsearch

client = Elasticsearch(ES_URL,basic_auth=(ES_USER,ES_PASSWORD))
