from fastapi.responses import JSONResponse
from fastapi_utils.cbv import cbv
from fastapi import UploadFile, File, Request
from fastapi.encoders import jsonable_encoder
from config import MEMBER_URL
from fastapi_utils.inferring_router import InferringRouter
# from db.database import engineconn
from async_db.database import engineconn
import os
from .member_data import Member_signup
from db.models import Member
import datetime

member_router = InferringRouter()

# engine = engineconn()
# session = engine.sessionmaker()
engine = engineconn()
session = engine.sessionmaker()

@cbv(member_router)
class MemberSource:
    @member_router.post(MEMBER_URL+"/sign_up")
    async def sign_up(self, member_info: Member_signup):

        # birth date로 형변환
        format = '%Y/%m/%d'
        member_info.birth = datetime.datetime.strptime(member_info.birth,format)
        
        # 회원가입
        member = Member(**member_info.dict())
        session.add(member)
        await session.commit()
        
        return member


    @member_router.post(MEMBER_URL+"/image_upload")
    async def image_upload(self, profile_image: UploadFile=File()):
        print(profile_image)
        return profile_image



    