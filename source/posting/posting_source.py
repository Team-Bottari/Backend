from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from config import POSTING_URL,MAIN_DIR
from settings import ES_SIZE
from .posting_data import Posting_create,Posting_update, Member_id_check
from fastapi.encoders import jsonable_encoder
from fastapi.background import BackgroundTasks
from fastapi.responses import FileResponse
from .posting_utils import posting_create,posting2summaries,delete_none_in_posting,delete_posting_dir,create_posting_dir, posting_update_data,get_image_path, add_images_list
from db import session, Member, Posting, Like
from es import client
from sqlalchemy import select,update
import os, datetime
posting_router = InferringRouter()

BASIC_POSTING_RESPONSES = {
    "mini":FileResponse(os.path.join(MAIN_DIR,"static","posting_mini.png")),
    "standard":FileResponse(os.path.join(MAIN_DIR,"static","posting_standard.png")),
    "origin":FileResponse(os.path.join(MAIN_DIR,"static","posting_origin.png")),
}

@cbv(posting_router)
class PostingSource:
    @posting_router.post(POSTING_URL,summary="포스팅 생성")
    async def create_posting(self,posting:Posting_create,background_task:BackgroundTasks):
        posting = jsonable_encoder(posting)
        query = select(Member).where(Member.email==posting["email"])
        result = await session.execute(query)
        member_id = jsonable_encoder(result.first()[0])["member_id"]
        posting_info = await posting_create(posting,member_id)
        posting_result = client.index(index="posting", body=posting_info)
        posting_id = posting_result['_id']
        background_task.add_task(create_posting_dir,posting_id)
        return {"response":200,"posting_id":posting_id} 
    
    @posting_router.get(POSTING_URL+"/list/",summary="포스팅 검색")
    async def posting_list(self,keyword : str = None, _from: int = 0):
        if keyword is not None: # 제목에서 검색할 것인지 content안에서도 검색이 될것인지, 닉네임으로 검색을 할것인지
            result = client.search(
                index='posting',
                body={
                    "from":_from,
                    'size':ES_SIZE,                                          
                    "query": {
                        "bool": {
                            "must": [
                                        {
                                            "match": {
                                                    "title": keyword
                                                }
                                        },
                                        {
                                            "match": {
                                                    "remove": False
                                                }
                                        }
                                ]
                            }
                        }
                    }
                )
        else:
            result = client.search(index='posting',body={"from":_from, 'size':ES_SIZE,
                                                         "query": {
                                                                "bool": {
                                                                    "must": [
                                                                                {
                                                                                    "match": {
                                                                                            "remove": False
                                                                                        }
                                                                                }
                                                                        ]
                                                                    }
                        }})
        """
        result["hits"]["hits"][0] = {'_index': 'posting', '_id': 'EWkSD4kBg4HIUcUDUlsn', '_score': 0.13353139, '_source': {'title': 'jjanggu', 'content': '짱구입니다.', 'price': 5000, 'email': 'user@example.com', 'category': '만화', 'can_discount': False, 'create_at': '2023-07-01T10:30:06', 'views': 0, 'like': 0, 'update_nums': 0, 'sold_out': False, 'remove': False, 'update_at': '2023-07-01T10:30:06', 'member_id': 7}}
        """
        for index in range(len(result["hits"]["hits"])):
            item = result["hits"]["hits"][index]
            item["_source"]["posting_id"]=item["_id"] 
        result = [ add_images_list(item["_source"]) for item in result["hits"]["hits"]]
        return {"response":200,"items":result}
    
    @posting_router.post(POSTING_URL+"/{posting_id}",summary="포스팅 상세조회")
    async def posting_read(self,member_id_check: Member_id_check, posting_id:str=None):
        member_id = jsonable_encoder(member_id_check)['member_id']
        #try:
        item = client.get(index='posting',id=posting_id)
        # 본인이 올린 글이 아니면 조회수 올리기
        if int(item['_source']['member_id']) !=int(member_id):
            # 조회수 update
            item["_source"]['views'] = item["_source"]['views'] + 1
            client.update(index='posting', id =posting_id, doc=item['_source'])
        item["_source"]['posting_id']=posting_id
        return {"response": 200,"posting":add_images_list(item["_source"])}
        #except:
            #return {"response":"해당 posting_id의 포스팅이 없습니다."}
            
        
    @posting_router.put(POSTING_URL+"/{posting_id}",summary="포스팅 업데이트")
    async def posting_update(self,member_id_check: Member_id_check, posting_id:str, new_posting:Posting_update):
        
        new_posting = jsonable_encoder(new_posting)
        member_id = jsonable_encoder(member_id_check)['member_id']
        # 수정 권한 체크
        try:
            item = client.get(index='posting',id=posting_id)
            posting = item['_source']
            if int(posting["member_id"]) != int(member_id):
                return {"response":"해당 게시물을 수정할 권한이 없습니다."}
            else: 
                new_posting = delete_none_in_posting(new_posting)
                posting = posting_update_data(posting,new_posting)
                print(posting)
                client.update(index='posting', id =posting_id, doc=posting)
                return {"response":"수정 완료"}
        except:
            return {"response":"해당 게시물이 없습니다."}
            
    
    @posting_router.delete(POSTING_URL+"/{posting_id}",summary="포스팅 삭제")
    async def posting_delete(self,member_id_check: Member_id_check, posting_id:str, background_task:BackgroundTasks):
        member_id = jsonable_encoder(member_id_check)['member_id']
        # 삭제 권한 체크
        try:
            item = client.get(index='posting',id=posting_id)
            posting = item['_source']
            if int(posting["member_id"]) != int(member_id):
                return {"response":"해당 게시물을 삭제할 권한이 없습니다."}
            elif posting['remove'] == True:
                return {"response":"해당 게시물은 이미 삭제되었습니다."}
            else:
                posting['remove'] = True # 삭제
                client.update(index='posting', id =posting_id, doc=posting)
                background_task.add_task(delete_posting_dir,posting_id)
                return {"response":"삭제 완료"}
        except:
            return {"response":"해당 게시물이 없습니다."}
    
    @posting_router.put(POSTING_URL+"/{posting_id}/pull-up",summary="포스팅 끌어올리기")
    async def posting_pull_up(self,member_id_check: Member_id_check,posting_id:str):
        member_id = jsonable_encoder(member_id_check)['member_id']
        try:
            item = client.get(index='posting',id=posting_id)
            posting = item['_source']
            if int(posting["member_id"]) != int(member_id):
                return {"response":"해당 게시물을 끌어올릴 권한이 없습니다."}
            elif posting['remove'] == True:
                return {"response":"해당 게시물은 삭제되었습니다."}
            else:
                now = datetime.datetime.now()
                now = datetime.datetime(now.year,now.month,now.day,now.hour,now.minute,now.second)
                if datetime.datetime.strptime(jsonable_encoder(posting)["update_at"], '%Y-%m-%dT%H:%M:%S') + datetime.timedelta(days=2) < datetime.datetime.now():
                    posting['update_at'] = now
                    posting['update_nums'] +=1
                    client.update(index='posting', id =posting_id, doc=posting)
                    return{"response": True}
                else:
                    can_pull_up_time = datetime.datetime.strptime(jsonable_encoder(posting)["update_at"], '%Y-%m-%dT%H:%M:%S') +datetime.timedelta(days=2)
                    return {"response": 200, "can_pull_up_time" : str(can_pull_up_time)}
        except:
            return {"response":"해당 게시물을 끌어올릴수 없습니다."} # 이미 삭제되었거나, 게시물을 올린 당사자가 아니거나.
        

#  @posting_router.put(POSTING_URL+"/{posting_id}/pull-up",summary="포스팅 끌어올리기")
#     async def posting_pull_up(self,member_id_check: Member_id_check,posting_id:str):
#         member_id = jsonable_encoder(member_id_check)['member_id']
#         query = select(Posting).where(Posting.posting_id==posting_id, Posting.member_id==member_id, Posting.remove==False)
#         result = await session.execute(query)
#         posting = result.first()
#         if posting is None:
#             return {"response":"해당 게시물을 끌어올릴 수 없습니다."} # 이미 삭제 되었거나, 게시물을 올린 당사자가 아니거나
#         else:
#             # 업데이트 시간 비교해서 2일 이후 이면 가능
#             if datetime.datetime.strptime(jsonable_encoder(posting[0])["update_at"], '%Y-%m-%dT%H:%M:%S') + datetime.timedelta(days=2) < datetime.datetime.now():
#                 query = update(Posting).where(Posting.posting_id==posting_id).values(update_nums = Posting.update_nums+1, update_at = datetime.datetime.now())
#                 await session.execute(query)
#                 await session.commit()
#                 return {"response":"끌어올리기 완료"}
#             else:
#                 # 한번도 끌올 안했으면 2일 후 가능
#                 if jsonable_encoder(posting[0])["update_nums"] == 0:
#                     return {"response":"글 작성 후 2일 후 끌어올리기가 가능합니다."}
#                 # 끌올 했으면 끌올 후 2일 지난 후 가능.
#                 else:
#                     return {"response":"마지막 끌어올리기 시점부터 2일 후 가능합니다."}
    
    # @posting_router.get(POSTING_URL+"/{posting_id}/mini",summary="포스팅 썸네일 mini")
    # async def posting_thumbnail_mini(self,posting_id:str):
    #     path = get_image_path(posting_id,"mini")
    #     if path is None:
    #         return BASIC_POSTING_RESPONSES["mini"]
    #     else:
    #         return FileResponse(path)
    
    # @posting_router.get(POSTING_URL+"/{posting_id}/standard",summary="포스팅 썸네일 standard")
    # async def posting_thumbnail_standard(self,posting_id:str):
    #     path = get_image_path(posting_id,"standard")
    #     if path is None:
    #         return BASIC_POSTING_RESPONSES["standard"]
    #     else:
    #         return FileResponse(path)
    
    # @posting_router.get(POSTING_URL+"/{posting_id}/origin",summary="포스팅 썸네일 origin")
    # async def posting_thumbnail_origin(self,posting_id:str):
    #     path = get_image_path(posting_id,"origin")
    #     if path is None:
    #         return BASIC_POSTING_RESPONSES["origin"]
    #     else:
    #         return FileResponse(path)