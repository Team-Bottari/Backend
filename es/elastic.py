# from settings import ES_PASSWORD,ES_URL,ES_USER
from elasticsearch import Elasticsearch
ES_URL = "http://192.168.0.32:9200"
ES_USER = "elastic"
ES_PASSWORD = "94a07s02d*fg"
client = Elasticsearch(ES_URL,basic_auth=(ES_USER,ES_PASSWORD))



# title:str
# content:str
# price:int
# email :EmailStr # example@google.com
# category:str
# can_discount:bool


if __name__ =="__main__":
    # print(client.indices.create(index="posting"))
    pass