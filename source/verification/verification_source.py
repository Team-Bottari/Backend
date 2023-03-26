from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from fastapi import Path
from fastapi.encoders import jsonable_encoder
from config import VERIFICATION_URL
from db import session, Member
from datetime import datetime,timedelta
from sqlalchemy import update, select
from fastapi.responses import RedirectResponse
verification_router = InferringRouter()

@cbv(verification_router)
class Verification:
    @verification_router.get(VERIFICATION_URL)
    async def verify(self,random_value:str=Path(min_length=16,max_length=16)):
        # 1. 인증번호가 같은 사람
        query = select(Member).where(Member.certificate_num==random_value)
        result = await session.execute(query)
        member = result.first()
        if member is None:
            return {"돌아가" : "빨리"}
        else:
            member_enc = jsonable_encoder(member[0])
            date_time_obj = datetime.strptime(member_enc['create_at'], '%Y-%m-%dT%H:%M:%S')
            if (datetime.now() - date_time_obj)<timedelta(minutes=5):
                query = update(Member).where(Member.certificate_num==random_value).values(certificate_status=True)
                result = await session.execute(query)
                await session.commit()
                return RedirectResponse("http://wisixicidi.iptime.org:10000")
            else:
                return RedirectResponse("http://wisixicidi.iptime.org:10000")
            # if member_enc['create_at']
        
        


