from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from config import POSTING_URL,MAIN_DIR
from settings import ES_SIZE
from utils import get_current_member_by_token
from .posting_data import Posting_create,Posting_update
from fastapi.encoders import jsonable_encoder
from fastapi.background import BackgroundTasks
from fastapi.responses import FileResponse
from fastapi import Depends
from .posting_utils import posting_create,posting2summaries,delete_none_in_posting,delete_posting_dir,create_posting_dir, posting_update_data,get_image_path, add_images_list
from db import session, Member, Posting, Like
from es import ElasticSearchClient
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
    async def create_posting(self,posting:Posting_create,background_task:BackgroundTasks, member_by_token: Member = Depends(get_current_member_by_token)):
        posting = jsonable_encoder(posting)
        member_from_token = jsonable_encoder(member_by_token.first()[0])
        member_id = member_from_token["member_id"]
        posting_info = await posting_create(posting,member_id)
        client = ElasticSearchClient()
        posting_result = client.insert_posting(posting_info)
        posting_id = posting_result['_id']
        background_task.add_task(create_posting_dir,posting_id)
        return {"response":200,"posting_id":posting_id} 
    
    @posting_router.get(POSTING_URL+"/list/",summary="포스팅 검색")
    async def posting_list(self,keyword : str = None, _from: int = 0):
        client = ElasticSearchClient()
        result = client.search_with_keyword(keyword=keyword,_from=_from)
        return {"response":200,"items":result}
    
    @posting_router.post(POSTING_URL+"/{posting_id}",summary="포스팅 상세조회")
    async def posting_read(self, posting_id:str=None, member_by_token: Member = Depends(get_current_member_by_token)):
        member_from_token = jsonable_encoder(member_by_token.first()[0])
        client = ElasticSearchClient()
        posting = client.get_posting(posting_id,member_from_token)
        if posting is not None:
            return {"response": 200,"posting":posting}
        else:
            return {"response":"해당 posting_id의 포스팅이 없습니다."}
            
        
    @posting_router.put(POSTING_URL+"/{posting_id}",summary="포스팅 업데이트")
    async def posting_update(self, posting_id:str, new_posting:Posting_update, member_by_token: Member = Depends(get_current_member_by_token)):
        new_posting = jsonable_encoder(new_posting)
        member_from_token = jsonable_encoder(member_by_token.first()[0])
        client = ElasticSearchClient()
        result = client.update_posting(posting_id=posting_id,member = member_from_token)
        return result
            
    
    @posting_router.delete(POSTING_URL+"/{posting_id}",summary="포스팅 삭제")
    async def posting_delete(self, posting_id:str, background_task:BackgroundTasks, member_by_token: Member = Depends(get_current_member_by_token)):
        member_from_token = jsonable_encoder(member_by_token.first()[0])
        client = ElasticSearchClient()
        result = client.delete_posting(posting_id,member_from_token)
        background_task.add_task(delete_posting_dir,posting_id)
        return result
    
    @posting_router.put(POSTING_URL+"/{posting_id}/pull-up",summary="포스팅 끌어올리기")
    async def posting_pull_up(self ,posting_id:str, member_by_token: Member = Depends(get_current_member_by_token)):
        member_from_token = jsonable_encoder(member_by_token.first()[0])
        client = ElasticSearchClient()
        return client.raise_posting(posting_id,member_from_token)
