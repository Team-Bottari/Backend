from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from config import LIKE_URL
from .like_data import Like_create, Cancle_like_create
from fastapi.encoders import jsonable_encoder
from db import session, Member, Posting, Like
from sqlalchemy import select,update
like_router = InferringRouter()


@cbv(like_router)
class LikeSource:
    @like_router.post(LIKE_URL,summary="좋아요")
    async def create_like(self, posting_member_info:Like_create):
        posting_member_info = jsonable_encoder(posting_member_info)
        # posting 유효한 포스팅인지 확인
        query = select(Posting).where(Posting.posting_id==posting_member_info['posting_id'], Posting.remove==False)
        result = await session.execute(query)
        posting = result.first()
        if posting is None:
            return {"response":"해당 게시물이 없습니다."}
        else: 
            # 이미 누른 좋아요 인지 check(사실상 클릭을 막아야함.)
            query = select(Like).where(Like.posting_id == posting_member_info['posting_id'], Like.member_id == posting_member_info['member_id'], Like.status == True)
            result = await session.execute(query)
            like = result.first()
            if like is not None:
                return {"response":"이미 좋아요를 하셨습니다."}
            else:
                # posting 수정
                query = update(Posting).where(Posting.posting_id==posting_member_info['posting_id'], Posting.remove==False).values(like = Posting.like + 1)
                result = await session.execute(query)
                # like 테이블 생성
                posting_member_info['status'] = True
                like = Like(**posting_member_info)
                session.add(like)
                await session.commit()

        return {"response":"좋아요 완료"}
    
    @like_router.put(LIKE_URL, summary="좋아요 취소")
    async def cancle_like(self, posting_member_info: Cancle_like_create):
        posting_member_info = jsonable_encoder(posting_member_info)
        # posting 유효한 포스팅인지 확인
        query = select(Posting).where(Posting.posting_id==posting_member_info['posting_id'], Posting.remove==False)
        result = await session.execute(query)
        posting = result.first()
        if posting is None:
            return {"response":"해당 게시물이 없습니다."}
        else: 
            # 좋아요 목록에 있는지 확인.(좋아요 클릭 안했는데 이 api는 호출 되면 안됨.)
            query = select(Like).where(Like.posting_id == posting_member_info['posting_id'], Like.member_id == posting_member_info['member_id'], Like.status == True)
            result = await session.execute(query)
            like = result.first()
            if like is None:
                return {"response":"이전에 좋아요를 안했습니다."}
            else:
                # like 테이블 수정
                query = update(Like).where(Like.posting_id == posting_member_info['posting_id'], Like.member_id == posting_member_info['member_id'], Like.status == True).values(status = False)
                await session.execute(query)
                # posting 수정
                query = update(Posting).where(Posting.posting_id==posting_member_info['posting_id'], Posting.remove==False).values(like = Posting.like - 1)
                result = await session.execute(query)
                await session.commit()
        return {"response":"좋아요 취소"}
    
        
    
   
    
    
    
    