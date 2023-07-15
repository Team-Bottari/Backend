from fastapi.responses import JSONResponse
from fastapi import Depends, HTTPException
from fastapi_utils.cbv import cbv
from fastapi.background import BackgroundTasks
from fastapi.encoders import jsonable_encoder
from config import MEMBER_URL,STORAGE_DIR
from fastapi_utils.inferring_router import InferringRouter
from .member_data import Member_signup,Member_override,Member_login,Member_changepw,Member_findpw,Member_findemail, Member_info_check, Member_logout, Member_withdrawal, Member_checkpw, Member_update_info, Token
from .member_utils import send_pw_mail, send_certificate_email, make_bcrypt_pw_from_origin_pw, verify_bycrypt_pw, create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from db import session, Member
from sqlalchemy import select, update
from utils import make_random_value
import datetime
import os

member_router = InferringRouter()

@cbv(member_router)
class MemberSource:
    @member_router.post(MEMBER_URL+"/override", summary="아이디 중복 확인")
    async def is_override(self,member_info: Member_override):
        member_info = jsonable_encoder(member_info)
        query = select(Member).where(Member.email==member_info["email"], Member.withdrawal == False, Member.certificate_status == True)
        result = await session.execute(query)
        if result.first() is None:
            return {"override":False}
        else:
            return {"override":True}
    
    @member_router.post(MEMBER_URL+"/sign_up", summary="회원가입" )
    async def sign_up(self, member_info: Member_signup ,background_task:BackgroundTasks):
        member_info = jsonable_encoder(member_info)
        # birth date로 형변환
        member_info['birth'] = datetime.datetime.strptime(member_info['birth'],'%Y-%m-%d')
        member_info['create_at'] = datetime.datetime.now()
        member_info['update_at'] = datetime.datetime.now()
        member_info['withdrawal'] = False
        member_info['certificate_status'] = False
        random_value = make_random_value()
        member_info['certificate_num'] = random_value # 인증번호
        

        # 아이디 중복확인
        query = select(Member).where(Member.email==member_info["email"], Member.withdrawal == False, Member.certificate_status == True)
        result = await session.execute(query)
        if result.first() is not None:
            return {"result":"사용중인 아이디가 있습니다."}
        
        # 암호화
        member_info['pw'] = make_bcrypt_pw_from_origin_pw(member_info['pw'])
        print(member_info)
        
        # 회원가입
        member = Member(**member_info)
        session.add(member)
        await session.commit()

        background_task.add_task(send_certificate_email, member_info['email'], random_value)
        
        
        
        # FileStorage 만들기
        try:
            os.makedirs(os.path.join(STORAGE_DIR,"profiles",member_info["email"]))
        except:
            pass
        return JSONResponse({"sign_up":True})

    @member_router.post(MEMBER_URL+"/login", summary="로그인",)
    async def login(self,member_info:Member_login):
        member_info = jsonable_encoder(member_info)
        query = select(Member).where(Member.email==member_info["email"], Member.pw == member_info['pw'], Member.withdrawal == False, Member.certificate_status == True)
        result = await session.execute(query)

        if result.first() is None:
            return {"sign_in": False}
        else:
            # 최근 로그인한 시간 체크
            query = update(Member).where(Member.email==member_info["email"]).values(last_login=datetime.datetime.now())
            result = await session.execute(query)
            await session.commit()
            return {"sign_in": True}

    @member_router.post(MEMBER_URL+"/logout",summary="로그아웃",)
    async def logout(self,member_info:Member_logout):
        member_info = jsonable_encoder(member_info)
        query = update(Member).where(Member.email==member_info["email"]).values(last_logout=datetime.datetime.now())
        result = await session.execute(query)
        await session.commit()
        return {"logout":True}
        
    @member_router.post(MEMBER_URL+"/info",summary="회원정보",)
    async def member_info(self,member_info:Member_info_check):
        member_info = jsonable_encoder(member_info)
        query = select(Member).where(Member.email==member_info["email"])
        result = await session.execute(query)
        info = result.first()
        if info is None:
            return JSONResponse({"email":False})
        else:
            return JSONResponse(jsonable_encoder(info[0]))

        
        
    @member_router.post(MEMBER_URL+"/withdrawal",summary="회원탈퇴",)
    async def member_delete(self,member_info:Member_withdrawal):
        member_info = jsonable_encoder(member_info)
        query = update(Member).where(Member.email==member_info["email"]).values(last_logout=datetime.datetime.now(), withdrawal=True)
        result = await session.execute(query)
        await session.commit()
        return {"withdrawal":True}



    @member_router.post(MEMBER_URL+"/id-find",summary="이메일찾기",)
    async def find_email(self,member_info:Member_findemail):
        member_info = jsonable_encoder(member_info)
        query = select(Member).where(Member.name==member_info["name"]).where(Member.birth==member_info["birth"], Member.phone == member_info['phone'], Member.withdrawal==False)
        result = await session.execute(query)
        info = result.first()
        if info is None:
            return JSONResponse({"email":False})
        else:
            info = jsonable_encoder(info[0])
            return JSONResponse({'email':info["email"]})
        
    
    @member_router.post(MEMBER_URL+"/pw-find",summary="비밀번호찾기",)
    async def find_pw(self,member_info:Member_findpw,background_task:BackgroundTasks):
        member_info = jsonable_encoder(member_info)
        target_email = member_info["email"]
        random_value = make_random_value()
        query = update(Member).where(Member.email==member_info["email"]).values(pw = random_value)
        result = await session.execute(query)
        await session.commit()
        background_task.add_task(send_pw_mail,target_email,random_value)
        return {"random_value" : random_value}
        
    
    @member_router.post(MEMBER_URL+"/pw-change",summary="비밀번호변경",)
    async def change_pw(self,member_info:Member_changepw):
        member_info = jsonable_encoder(member_info)
        query = select(Member).where(Member.email==member_info["email"])
        result = await session.execute(query)
        
        if jsonable_encoder(result.first()[0])['pw'] == member_info['before_pw']:
            query = update(Member).where(Member.email==member_info["email"], Member.pw == member_info['before_pw']).values(pw = member_info["new_pw"])
            result = await session.execute(query)
            await session.commit()
            return {"pw_change": True}
        else:
            return {"pw_change":False, "before_pw":"이전 비밀번호가 다릅니다."}
        
    @member_router.post(MEMBER_URL+"/pw-check", summary="비밀번호 확인(인증용)")
    async def check_pw(self, member_info:Member_checkpw):
        member_info = jsonable_encoder(member_info)
        query = select(Member).where(Member.email==member_info["email"], Member.pw==member_info["pw"])
        result = await session.execute(query)
        info = result.first()
        if info is None:
            return JSONResponse({"pw_check":"비밀번호 확인 부탁드립니다."})
        else:
            return JSONResponse({'pw_check':True})
        

    @member_router.post(MEMBER_URL+"/update-member-info", summary="회원정보 수정")
    async def update_member_info(self, member_info:Member_update_info):
        member_info = jsonable_encoder(member_info)
        query = update(Member).where(Member.email==member_info["email"]).values(nick_name = member_info["nick_name"], name = member_info["name"], phone = member_info["phone"], update_at=datetime.datetime.now())
        result = await session.execute(query)
        await session.commit()
        return {"update_member_info": True}
    
    
    @member_router.post("/login-token", response_model=Token, summary="토큰으로 로그인")
    async def login_for_access_token(self, form_data: OAuth2PasswordRequestForm = Depends()):
        query = select(Member).where(Member.email==form_data.username, Member.withdrawal == False, Member.certificate_status == True)
        member = await session.execute(query)
        
        if member is None:
            return {"sign_in": "아이디를 확인하거나 회원가입을 해주세요."}
        else:
            member = jsonable_encoder(member.first()[0])
            if not verify_bycrypt_pw(member['pw'], form_data.password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect username or password",
                    headers={"WWW-Authenticate": "Bearer"},
                    )
            
        access_token = create_access_token(member)
        return {"access_token":access_token, "token_type":"bearer", "nick_name":member['nick_name'], "email":member['email']}
