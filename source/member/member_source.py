from fastapi.responses import JSONResponse
from fastapi_utils.cbv import cbv
from fastapi import UploadFile, File, Request
from fastapi.encoders import jsonable_encoder
from config import MEMBER_URL
from fastapi_utils.inferring_router import InferringRouter
from .member_data import Member_signup,Member_override,Member_login,Member_changepw,Member_findpw,Member_findemail
from async_db import session,Member
import datetime

member_router = InferringRouter()


@cbv(member_router)
class MemberSource:
    @member_router.post(MEMBER_URL+"/override",summary="아이디 중복 확인",)
    async def is_override(self,member_info: Member_override):
        member_info = jsonable_encoder(member_info)
        
    
    @member_router.post(MEMBER_URL+"/sign_up",summary="회원가입",)
    async def sign_up(self, member_info: Member_signup):
        # birth date로 형변환
        member_info.birth = datetime.datetime.strptime(member_info.birth,'%Y/%m/%d')
        # 회원가입
        member = Member(**jsonable_encoder(member_info))
        session.add(member)
        await session.commit()
        return JSONResponse({"이거야":"맞아!","정말?":"응!","ABCD":"1234"})

    @member_router.post(MEMBER_URL+"/login",summary="로그인",)
    async def login(self,member_info:Member_login):
        member_info = jsonable_encoder(member_info)
        

    @member_router.post(MEMBER_URL+"/logout",summary="로그아웃",)
    async def logout(self,member_info:Member_override):
        member_info = jsonable_encoder(member_info)
        
        
    @member_router.post(MEMBER_URL+"/info",summary="회원정보",)
    async def member_info(self,member_info:Member_override):
        member_info = jsonable_encoder(member_info)
        
        
    @member_router.post(MEMBER_URL+"/withdrawal",summary="회원탈퇴",)
    async def member_delete(self,member_info:Member_override):
        member_info = jsonable_encoder(member_info)
        

    @member_router.post(MEMBER_URL+"/id-find",summary="이메일찾기",)
    async def find_email(self,member_info:Member_findemail):
        member_info = jsonable_encoder(member_info)
        
    
    @member_router.post(MEMBER_URL+"/pw-find",summary="비밀번호찾기",)
    async def find_pw(self,member_info:Member_findpw):
        member_info = jsonable_encoder(member_info)
        
    
    @member_router.post(MEMBER_URL+"/pw-change",summary="비밀번호변경",)
    async def change_pw(self,member_info:Member_changepw):
        member_info = jsonable_encoder(member_info)
        
        