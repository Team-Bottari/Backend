# from elasticsearch import Elasticsearch
# es = Elasticsearch(
#     "http://192.168.0.33:9200",
#     http_auth=("elastic",'94a07s02d*fg')
# )
# # res = es.get(index="product_list",doc_type="_doc", id=1)
# # print(res)

# # def make_inde(ex, index)
# index_name = 'goods'
# # es.indices.create(index=index_name)
# def create_es():
    
#     doc1 = {"name":"샘송1", "price":101}
#     doc2 = {"name":"샘송2", "price":102}
#     doc3 = {"name":"샘송3", "price":103}

#     es.index(index_name, doc_type="sting", body=doc1)
#     es.index(index_name, doc_type="sting", body=doc2)
#     es.index(index_name, doc_type="sting", body=doc3)

#     es.indices.refresh(index=index_name)
# # create_es()

# result = es.search(index=index_name, body={"from":0, "size":10, "query":{"match":{"name":"샘송1"}}})
# print(result)
# for x in result['hits']['hits']:
#     print(x)
# A
# b