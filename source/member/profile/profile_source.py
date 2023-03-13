from fastapi.responses import FileResponse
from fastapi import Body
from fastapi_utils.cbv import cbv
from fastapi import UploadFile
from fastapi.background import BackgroundTasks
from fastapi.encoders import jsonable_encoder
from config import PROFILE_URL
from fastapi_utils.inferring_router import InferringRouter
from utils import uploadfile2array,profile_image_save,profile_image_delete
from .profile_data import Member_upload
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
    async def upload_profile(background_tasks : BackgroundTasks, upload_file :UploadFile,member_info=Body(...)):
        member_info = jsonable_encoder(member_info)
        image = await uploadfile2array(upload_file)
        background_tasks.add_task(profile_image_save,image,member_info)
        return {"response":200}
    
    @profile_router.post(PROFILE_URL+"/mini", summary="프로필 이미지 조회 mini")
    async def get_profile_mini(self,member_info:Member_upload=Body(...)):
        member_info = jsonable_encoder(member_info)
        id = member_info["id"]
        profile_path = os.path.join(STORAGE_DIR,id,"profile_mini.jpg")
        if os.path.isfile(profile_path):
            return FileResponse(profile_path)
        else:
            return BASIC_PROFILE_RESPONSES['mini']
    
    @profile_router.post(PROFILE_URL+"/standard", summary="프로필 이미지 조회 standard")
    async def get_profile_standard(self,member_info:Member_upload=Body(...)):
        member_info = jsonable_encoder(member_info)
        id = member_info["id"]
        profile_path = os.path.join(STORAGE_DIR,id,"profile_standard.jpg")
        if os.path.isfile(profile_path):
            return FileResponse(profile_path)
        else:
            return BASIC_PROFILE_RESPONSES['standard']
    
    @profile_router.post(PROFILE_URL+"/origin", summary="프로필 이미지 조회 origin")
    async def get_profile_origin(self,member_info:Member_upload=Body(...)):
        member_info = jsonable_encoder(member_info)
        id = member_info["id"]
        profile_path = os.path.join(STORAGE_DIR,id,"profile_origin.jpg")
        if os.path.isfile(profile_path):
            return FileResponse(profile_path)
        else:
            return BASIC_PROFILE_RESPONSES['origin']
    
    @profile_router.post(PROFILE_URL+"/update", summary="프로필 이미지 업데이트")
    async def upload_profile(self,background_tasks : BackgroundTasks, upload_file :UploadFile | None=None,member_info=Body(...)):
        member_info = jsonable_encoder(member_info)
        image = await uploadfile2array(upload_file)
        background_tasks.add_task(profile_image_save,image,member_info)
        return {"response":200}
    
    @profile_router.post(PROFILE_URL+"/delete", summary="프로필 이미지 삭제")
    async def upload_profile(self,background_tasks : BackgroundTasks,member_info=Body(...)):
        member_info = jsonable_encoder(member_info)
        profile_image_delete(member_info)
        return {"response":200}
    