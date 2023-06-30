# from settings import ES_PASSWORD,ES_URL,ES_USER
from elasticsearch import Elasticsearch
import requests
ES_URL = "http://192.168.0.32:9200"
ES_USER = "elastic"
ES_PASSWORD = "94a07s02d*fg"
client = Elasticsearch(ES_URL,basic_auth=(ES_USER,ES_PASSWORD))

if __name__ =="__main__":
    es = client.search(index="posting", pretty=True)
    print(es)
    # url = "http://192.168.0.33:9200/_license/start_trial"
    # payload = {'acknowledge': 'true'}
    # response = requests.post(url, data=payload)
    # print(response)