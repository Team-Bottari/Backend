from fastapi.responses import FileResponse
from fastapi import Body,Request, Depends
from fastapi_utils.cbv import cbv
from fastapi.background import BackgroundTasks
from fastapi.encoders import jsonable_encoder
from config import PROFILE_URL
from fastapi_utils.inferring_router import InferringRouter
from .profile_utils import profile_image_save,profile_image_delete,read_profile_ext
from .profile_data import Member_upload
from utils import get_current_member_by_token
from db import Member
from config import STORAGE_DIR,MAIN_DIR
import os



profile_router = InferringRouter()

BASIC_PROFILE_RESPONSES = {
    "mini":FileResponse(os.path.join(MAIN_DIR,"static","profile_mini.jpg")),
    "standard":FileResponse(os.path.join(MAIN_DIR,"static","profile_standard.jpg")),
    "origin":FileResponse(os.path.join(MAIN_DIR,"static","profile_origin.jpg")),
}


@cbv(profile_router)
class ProfileSource:
    @profile_router.post(PROFILE_URL+"/upload", summary="프로필 이미지 업로드",)
    async def upload_profile(self, request: Request):
        await profile_image_save(request)
        return {"response":200}
    
    @profile_router.post(PROFILE_URL+"/mini", summary="프로필 이미지 조회 mini")
    async def get_profile_mini(self, member_by_token: Member = Depends(get_current_member_by_token)):
        member_from_token = jsonable_encoder(member_by_token.first()[0])
        id = member_from_token["email"]
        ext = await read_profile_ext(member_from_token)
        profile_path = os.path.join(STORAGE_DIR,"profiles",id,f"profile_mini{ext}")
        if os.path.isfile(profile_path):
            return FileResponse(profile_path)
        else:
            return BASIC_PROFILE_RESPONSES['mini']
    
    @profile_router.post(PROFILE_URL+"/standard", summary="프로필 이미지 조회 standard")
    async def get_profile_standard(self,member_by_token: Member = Depends(get_current_member_by_token)):
        print(member_by_token)
        print(member_by_token)
        print(member_by_token)
        print(member_by_token)
        member_by_token = jsonable_encoder(member_by_token.first())["Member"]
        id = member_by_token["email"]
        ext = await read_profile_ext(member_by_token)
        profile_path = os.path.join(STORAGE_DIR,"profiles",id,f"profile_standard{ext}")
        if os.path.isfile(profile_path):
            return FileResponse(profile_path)
        else:
            return BASIC_PROFILE_RESPONSES['standard']
    
    @profile_router.post(PROFILE_URL+"/origin", summary="프로필 이미지 조회 origin")
    async def get_profile_origin(self, member_by_token: Member = Depends(get_current_member_by_token)):
        member_by_token = jsonable_encoder(member_by_token.first())["Member"]
        id = member_by_token["email"]
        ext = await read_profile_ext(member_by_token)
        profile_path = os.path.join(STORAGE_DIR,"profiles",id,f"profile_origin{ext}")
        if os.path.isfile(profile_path):
            return FileResponse(profile_path)
        else:
            return BASIC_PROFILE_RESPONSES['origin']
    
    @profile_router.post(PROFILE_URL+"/delete", summary="프로필 이미지 삭제")
    async def delete_profile(self,background_tasks : BackgroundTasks, member_by_token: Member = Depends(get_current_member_by_token)):
        background_tasks.add_task(profile_image_delete,member_by_token)
        return BASIC_PROFILE_RESPONSES['standard']
    
    @profile_router.post(PROFILE_URL+"/update", summary="프로필 이미지 업데이트")
    async def update_profile(self, request: Request):
        await profile_image_save(request)
        return {"response":200}
    