from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from config import LIKE_URL
from .like_data import Like_create, Cancle_like_create, Like_list
from fastapi.encoders import jsonable_encoder
from es import client
from db import session, Posting, Like
from sqlalchemy import select,update
from .like_utils import delete_none_in_posting, posting_update_data
like_router = InferringRouter()


@cbv(like_router)
class LikeSource:
    @like_router.post(LIKE_URL,summary="좋아요")
    async def create_like(self, posting_member_info:Like_create):
        posting_member_info = jsonable_encoder(posting_member_info)
        # posting 유효한 포스팅인지 확인
        posting = client.get(index='posting',id=posting_member_info['posting_id'])

        if posting is None:
            return {"response":"해당 게시물이 없습니다."}
        elif posting['_source']['remove'] == True:
            return {"response":"해당 게시물이 삭제되었습니다."}
        else: 
            # 이미 누른 좋아요 인지 check(사실상 클릭을 막아야함.)
            query = select(Like).where(Like.posting_id == posting['_id'], Like.member_id == posting_member_info['member_id'], Like.status == True)
            result = await session.execute(query)
            like = result.first()
            if like is not None:
                return {"response":"이미 좋아요를 하셨습니다."}
            else:
                # posting 수정
                posting_source = posting['_source']
                posting_source['like'] += 1
                new_posting = delete_none_in_posting(posting_source)
                new_posting = posting_update_data(posting_source,new_posting)
                client.update(index='posting', id =posting['_id'], doc=posting_source)
                posting_member_info['status'] = True
                
                like = Like(posting_id = posting_member_info['posting_id'], member_id =posting_member_info['member_id'], status=True)
                session.add(like)
                await session.commit()

        return {"response":"좋아요 완료"}
    
    @like_router.put(LIKE_URL, summary="좋아요 취소")
    async def cancle_like(self, posting_member_info: Cancle_like_create):
        posting_member_info = jsonable_encoder(posting_member_info)
        # posting 유효한 포스팅인지 확인
        posting = client.get(index='posting',id=posting_member_info['posting_id'])
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
                print(posting_member_info)
                query = update(Like).where(Like.posting_id == posting_member_info['posting_id'], Like.member_id == posting_member_info['member_id'], Like.status == True).values(status = False)
                await session.execute(query)
                await session.commit()
                
                # posting 수정
                posting_source = posting['_source']
                if posting_source['like'] > 0:
                    posting_source['like'] -= 1
                new_posting = delete_none_in_posting(posting_source)
                new_posting = posting_update_data(posting_source,new_posting)
                client.update(index='posting', id =posting['_id'], doc=new_posting)
                
        return {"response":"좋아요 취소"}
    
    
    @like_router.get(LIKE_URL + "/list", summary="좋아요 목록")
    async def like_list(self, member_id:str):
        query = select(Like).where(Like.status == True, Like.member_id == member_id)
        result = await session.execute(query)
        list_items = jsonable_encoder(result.all())
        print(list_items)
        
        return {"response":list_items}
    
    
        
    
   
    
    
    
    