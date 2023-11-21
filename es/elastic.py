from elasticsearch import Elasticsearch
from config import STORAGE_DIR
from fastapi.encoders import jsonable_encoder
import datetime
import os 
ES_URL = "http://192.168.0.32:9200"
ES_USER = "elastic"
ES_PASSWORD = "94a07s02d*fg"

client = Elasticsearch(ES_URL,basic_auth=(ES_USER,ES_PASSWORD))
class ElasticSearchClient:
    def __init__(self):
        self.client = Elasticsearch(ES_URL,basic_auth=(ES_USER,ES_PASSWORD))
        
    def insert_posting(self,body:dict):
        """
        1. 포스팅 삽입
        """
        return self.client.index(index = "posting",body = body)
    
    def search_with_keyword(self,keyword:str,_from:int=0,size:int=20):
        """
        1. keyword의 None 여부 확인
        2. keyword의 여부에 따라 body 객체 생성
        3. 검색 수행
        4. 검색 포스팅에 이미지를 더해서 리턴
        """
        if keyword is not None:
            body = {"from":_from,'size':size,"query": {"bool": {"must": [{"match": {"title": keyword}},{"match": {"remove": False}}]}}}
        else:
            body = {"from":_from, 'size':size,"query": {"bool": {"must": [{"match": {"remove": False}}]}}}
        result = self.client.search(index="posting",body=body)
        """
        result["hits"]["hits"][0] = {'_index': 'posting', '_id': 'EWkSD4kBg4HIUcUDUlsn', '_score': 0.13353139, '_source': {'title': 'jjanggu', 'content': '짱구입니다.', 'price': 5000, 'email': 'user@example.com', 'category': '만화', 'can_discount': False, 'create_at': '2023-07-01T10:30:06', 'views': 0, 'like': 0, 'update_nums': 0, 'sold_out': False, 'remove': False, 'update_at': '2023-07-01T10:30:06', 'member_id': 7}}
        """
        for index in range(len(result["hits"]["hits"])):
            item = result["hits"]["hits"][index]
            item["_source"]["posting_id"]=item["_id"] 
        result = [ self.add_images_list(item["_source"]) for item in result["hits"]["hits"]]
        return result
    
    def add_images_list(self,posting):
        """
        포스팅의 이미지는 따로 관리되기 때문에, 이미지정보를 추가
        """
        target_path = os.path.join(STORAGE_DIR,"postings",posting["posting_id"])
        posting["posting_images"] = sorted([ path for path in os.listdir(target_path)])
        return posting
    
    def get_posting(self,posting_id:int,member:dict):
        """
        1. 포스팅 아이디로 포스팅 획득
        2. 해당 포스팅의 저자와 조회자가 다르면 조회수 1 업
        3. 리턴
        """
        try:
            item = self.client.get(index="posting",id=posting_id)
            if int(item['_source']['member_id']) !=int(member['member_id']):
                item["_source"]['views'] = item["_source"]['views'] + 1
                self.client.update(index='posting', id =posting_id, doc=item['_source'])
            item["_source"]['posting_id']=posting_id
            return self.add_images_list(item["_source"])
        except:
            return None
        
    def update_posting(self,posting_id,member):
        try:
            item = self.client.get(index='posting',id=posting_id)
            posting = item['_source']
            if int(posting["member_id"]) != int(member['member_id']):
                return {"response":"해당 게시물을 수정할 권한이 없습니다."}
            else: 
                new_posting = self.delete_none_in_posting(new_posting)
                posting = self.posting_update_data(posting,new_posting)
                self.client.update(index='posting', id =posting_id, doc=posting)
                return {"response":"수정 완료"}
        except:
            return {"response":"해당 게시물이 없습니다."}
    
    def delete_posting(self,posting_id,member):
        item = self.client.get(index="posting",id=posting_id)
        posting = item['_source']
        try:
            if int(posting["member_id"]) != int(member['member_id']):
                return {"response":"해당 게시물을 삭제할 권한이 없습니다."}
            elif posting['remove'] == True:
                return {"response":"해당 게시물은 이미 삭제되었습니다."}
            else:
                posting['remove'] = True # 삭제
                self.client.update(index='posting', id =posting_id, doc=posting)
                return {"response":"삭제 완료"}
        except:
            return {"response":"해당 게시물이 없습니다."}
    
    def raise_posting(self,posting_id,member):
        try:
            item = self.client.get(index='posting',id=posting_id)
            posting = item['_source']
            if int(posting["member_id"]) != int(member['member_id']):
                return {"response":"해당 게시물을 끌어올릴 권한이 없습니다."}
            elif posting['remove'] == True:
                return {"response":"해당 게시물은 삭제되었습니다."}
            else:
                now = datetime.datetime.now()
                now = datetime.datetime(now.year,now.month,now.day,now.hour,now.minute,now.second)
                if datetime.datetime.strptime(jsonable_encoder(posting)["update_at"], '%Y-%m-%dT%H:%M:%S') + datetime.timedelta(days=2) < datetime.datetime.now():
                    posting['update_at'] = now
                    posting['update_nums'] +=1
                    self.client.update(index='posting', id =posting_id, doc=posting)
                    return{"response": True}
                else:
                    can_pull_up_time = datetime.datetime.strptime(jsonable_encoder(posting)["update_at"], '%Y-%m-%dT%H:%M:%S') +datetime.timedelta(days=2)
                    return {"response": 200, "can_pull_up_time" : str(can_pull_up_time)}
        except:
            return {"response":"해당 게시물을 끌어올릴수 없습니다."} # 이미 삭제되었거나, 게시물을 올린 당사자가 아니거나.






    def delete_none_in_posting(self,posting):
        return { key:posting[key] for key in posting if posting[key] is not None}
    
    def posting_update_data(self,posting,new_posting):
        now = datetime.now()
        now = datetime(now.year,now.month,now.day,now.hour,now.minute,now.second)
        posting.update(new_posting)
        posting["update_at"]=now
        return posting