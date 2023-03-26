from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from config import POSTING_URL
from .posting_data import Posting_create,Posting_update
from fastapi.encoders import jsonable_encoder
from fastapi.background import BackgroundTasks
from .posting_utils import update_posting_create,posting2summaries,delete_none_in_posting,delete_posting_dir,create_posting_dir
from db import session, Member, Posting
from sqlalchemy import select,update,delete
posting_router = InferringRouter()

@cbv(posting_router)
class PostingSource:
    @posting_router.post(POSTING_URL,summary="포스팅 생성")
    async def create_posting(self,posting:Posting_create,background_task:BackgroundTasks):
        posting = jsonable_encoder(posting)
        query = select(Member).where(Member.email==posting["email"])
        result = await session.execute(query)
        member_id = jsonable_encoder(result.first()[0])["member_id"]
        posting_info = await update_posting_create(posting,member_id)
        posting = Posting(**posting_info)
        session.add(posting)
        await session.flush()
        posting_id = posting.posting_id
        await session.commit()
        background_task.add_task(create_posting_dir,posting_id)
        return {"response":200,"posting_id":posting_id} 
    
    @posting_router.get(POSTING_URL+"/list",summary="포스팅 검색")
    async def posting_list(self,keyword : str = None):
        if keyword is not None:
            query = select(Posting).filter(Posting.title.like(f"%{keyword}%")).order_by(Posting.create_at)
        else:
            query = select(Posting).order_by(Posting.create_at)
        result = await session.execute(query)
        list_items = jsonable_encoder(result.all())
        list_item_summaries = posting2summaries(list_items)
        return {"response":200,"items":list_item_summaries}
    
    @posting_router.post(POSTING_URL+"/{posting_id}/read",summary="포스팅 상세조회")
    async def posting_read(self,posting_id:str=None):
        query = select(Posting).where(Posting.posting_id==posting_id)
        result = await session.execute(query)
        item = result.first()
        if item is None:
            return {"response":"치명적인에러"}
        else:
            item = jsonable_encoder(item)
            return {"response": 200,"posting":item["Posting"]}
        
    @posting_router.post(POSTING_URL+"/{posting_id}/update",summary="포스팅 업데이트")
    async def posting_update(self,posting_id:str,posting:Posting_update):
        posting = jsonable_encoder(posting)
        posting = delete_none_in_posting(posting)
        query = update(Posting).where(Posting.posting_id==posting_id).values(**posting)
        await session.execute(query)
        await session.commit()
        return {"response":200}
    
    @posting_router.post(POSTING_URL+"/{posting_id}/delete",summary="포스팅 삭제")
    async def posting_delete(self,posting_id:str,background_task:BackgroundTasks):
        query = delete(Posting).where(Posting.posting_id==posting_id)
        await session.execute(query)
        await session.commit()
        background_task.add_task(delete_posting_dir,posting_id)
        return {"response":200}
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
"""
@posting_router.post(POSTING_URL)
    async def create_posting(self,posting:Posting_create):
        posting = jsonable_encoder(posting)
        query = select(Member).where(Member.email==posting["email"])
        result = await session.execute(query)
        member_id = jsonable_encoder(result.first()[0])["member_id"]
        posting_info = await update_posting_create(posting,member_id)
        create_at = posting_info["create_at"]
        posting = Posting(**posting_info)
        session.add(posting)
        result = await session.commit()
        query = select(Posting).where(Posting.member_id==member_id,Posting.create_at == create_at)
        result = await session.execute(query)
        item = result.first()
        if item is None:
            print("치명적 에러")
        else:
            posting_id = jsonable_encoder(item[0])["posting_id"]
        return {"response":200,"posting_id":posting_id}
"""