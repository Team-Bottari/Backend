from fastapi.responses import JSONResponse
from fastapi_utils.cbv import cbv
from fastapi import UploadFile, File, Request
from fastapi.encoders import jsonable_encoder
from config import MEMBER_URL
from fastapi_utils.inferring_router import InferringRouter
from .member_data import Member_signup
from async_db import session,Member
import datetime

member_router = InferringRouter()


@cbv(member_router)
class MemberSource:
    @member_router.post(MEMBER_URL+"/sign_up",summary="회원가입",)
    async def sign_up(self, member_info: Member_signup):
        # birth date로 형변환
        format = '%Y/%m/%d'
        member_info.birth = datetime.datetime.strptime(member_info.birth,format)
        # 회원가입
        member = Member(**jsonable_encoder(member_info))
        session.add(member)
        await session.commit()
        return JSONResponse({"이거야":"맞아!","정말?":"응!","ABCD":"1234"})


    @member_router.post(MEMBER_URL+"/image_upload",summary="프로필 이미지 업로드",)
    async def image_upload(self, profile_image: UploadFile=File()):
        return profile_image



    