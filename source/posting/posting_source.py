from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from config import POSTING_URL
from .posting_data import Posting_create
from fastapi import UploadFile
from fastapi.encoders import jsonable_encoder
from utils import update_poting_create
from db import session, Member, Posting
from sqlalchemy import select
posting_router = InferringRouter()

@cbv(posting_router)
class PostingSource:
    @posting_router.post(POSTING_URL)
    async def create_posting(self,posting:Posting_create):
        posting = jsonable_encoder(posting)
        query = select(Member).where(Member.email==posting["email"])
        result = await session.execute(query)
        member_id = jsonable_encoder(result.first()[0])["member_id"]
        posting_info = await update_poting_create(posting,member_id)
        posting = Posting(**posting_info)
        session.add(posting)
        await session.flush()
        posting_id = posting.posting_id
        await session.commit()
        return {"response":200,"posting_id":posting_id} 
    
    @posting_router.post(POSTING_URL+"/image/{posting_id}/{image_id}")
    async def create_posting_image(self,posting_id:int,image_id:int,image:UploadFile(...)):
        
        return
    
    @posting_router.get(POSTING_URL+"/list")
    async def posting_list(self,keyword : str = None):
        if keyword is not None:
            query = select(Posting).filter(Posting.title.like(f"%{keyword}%")).order_by(Posting.create_at)
        else:
            query = select(Posting).order_by(Posting.create_at)
        result = await session.execute(query)
        list_tems = jsonable_encoder(result.all())
        return {"response":200,"items":list_tems}
    
    
    
    
"""
@posting_router.post(POSTING_URL)
    async def create_posting(self,posting:Posting_create):
        posting = jsonable_encoder(posting)
        query = select(Member).where(Member.email==posting["email"])
        result = await session.execute(query)
        member_id = jsonable_encoder(result.first()[0])["member_id"]
        posting_info = await update_poting_create(posting,member_id)
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