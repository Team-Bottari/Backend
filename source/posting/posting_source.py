from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from config import POSTING_URL
from .posting_data import Posting_create
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
        query = select(Member).where(Member.id==posting["member_id"])
        result = await session.execute(query)
        member_id = jsonable_encoder(result.first()[0])["member_id"]
        posting_info = await update_poting_create(posting,member_id)
        posting = Posting(**posting_info)
        session.add(posting)
        await session.commit()
        return {"response":200}
    
    @posting_router.get(POSTING_URL+"/list")
    async def posting_list(self,keyword : str = None):
        if keyword is not None:
            query = select(Posting).filter(Posting.title.like(f"%{keyword}%")).order_by(Posting.create_at)
        else:
            query = select(Posting).order_by(Posting.create_at)
        result = await session.execute(query)
        list_tems = jsonable_encoder(result.all())
        return {"response":200,"items":list_tems}
    