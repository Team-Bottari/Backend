from fastapi.responses import JSONResponse
from fastapi_utils.cbv import cbv
from fastapi import UploadFile, File, Request
from fastapi.encoders import jsonable_encoder
from config import MEMBER_URL
from fastapi_utils.inferring_router import InferringRouter
from .member_data import Member_signup,Member_override,Member_login,Member_changepw,Member_findpw,Member_findemail, Member_info_check
from async_db import session, Member
from sqlalchemy import select, update
import datetime

member_router = InferringRouter()


@cbv(member_router)
class MemberSource:
    @member_router.post(MEMBER_URL+"/override", summary="아이디 중복 확인")
    async def is_override(self,member_info: Member_override):
        member_info = jsonable_encoder(member_info)
        query = select(Member).where(Member.id==member_info["id"])
        result = await session.execute(query)
        if result is None:
            return {"override":False}
        else:
            return {"override":True}
    
    @member_router.post(MEMBER_URL+"/sign_up", summary="회원가입")
    async def sign_up(self, member_info: Member_signup):
        member_info = jsonable_encoder(member_info)
        # birth date로 형변환
        member_info['birth'] = datetime.datetime.strptime(member_info['birth'],'%Y-%m-%d')
        member_info['create_at'] = datetime.datetime.now()
        # 회원가입
        member = Member(**member_info)
        session.add(member)
        await session.commit()
        #TODO 암호화 필요.
        return JSONResponse({"sign_up":True})

    @member_router.post(MEMBER_URL+"/login", summary="로그인",)
    async def login(self,member_info:Member_login):
        member_info = jsonable_encoder(member_info)
        query = select(Member).where(Member.id==member_info["id"], Member.pw == member_info['pw'])
        result = await session.execute(query)
        
        if result is None:
            return {"sign_in": False}
        else:
            # 최근 로그인한 시간 체크
            print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            query = update(Member).where(Member.id==member_info["id"]).values(last_login=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            result = await session.execute(query)
            await session.commit()
            return {"sign_in": True}

    @member_router.post(MEMBER_URL+"/logout",summary="로그아웃",)
    async def logout(self,member_info:Member_override):
        member_info = jsonable_encoder(member_info)
        return {"logout":True}
        
    @member_router.post(MEMBER_URL+"/info",summary="회원정보",)
    async def member_info(self,member_info:Member_info_check):
        member_info = jsonable_encoder(member_info)
        member_info_from_id = session.query(Member).filter_by(id = member_info['id']).first()
        print(jsonable_encoder(member_info_from_id))

        
        
        
    @member_router.post(MEMBER_URL+"/withdrawal",summary="회원탈퇴",)
    async def member_delete(self,member_info:Member_override):
        member_info = jsonable_encoder(member_info)
        

    @member_router.post(MEMBER_URL+"/id-find",summary="이메일찾기",)
    async def find_email(self,member_info:Member_findemail):
        member_info = jsonable_encoder(member_info)
        query = select(Member).where(Member.name==member_info["name"]).where(Member.birth==member_info["birth"])
        result = await session.execute(query)
        info = result.first()
        if info is None:
            return JSONResponse({"id":False})
        else:
            info = jsonable_encoder(info[0])
            return JSONResponse({'id':info["id"]})
        
    
    @member_router.post(MEMBER_URL+"/pw-find",summary="비밀번호찾기",)
    async def find_pw(self,member_info:Member_findpw):
        member_info = jsonable_encoder(member_info)
        
    
    @member_router.post(MEMBER_URL+"/pw-change",summary="비밀번호변경",)
    async def change_pw(self,member_info:Member_changepw):
        member_info = jsonable_encoder(member_info)
        
        