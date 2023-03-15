from fastapi.responses import FileResponse
from fastapi import Body
from fastapi_utils.cbv import cbv
from fastapi import UploadFile
from fastapi.background import BackgroundTasks
from fastapi.encoders import jsonable_encoder
from config import PROFILE_URL
from fastapi_utils.inferring_router import InferringRouter
from utils import profile_image_save,profile_image_delete,read_profile_ext
from .profile_data import Member_upload
from config import STORAGE_DIR,MAIN_DIR
from pathlib import Path
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
    async def upload_profile(self,background_tasks : BackgroundTasks, upload_file :UploadFile,member_info=Body(...)):
        member_info = jsonable_encoder(member_info)
        ext = Path(str(upload_file.filename)).suffix
        background_tasks.add_task(profile_image_save,upload_file,member_info,ext)
        return {"response":200}
    
    @profile_router.post(PROFILE_URL+"/mini", summary="프로필 이미지 조회 mini")
    async def get_profile_mini(self,member_info:Member_upload=Body(...)):
        member_info = jsonable_encoder(member_info)
        id = member_info["id"]
        ext = await read_profile_ext(member_info)
        profile_path = os.path.join(STORAGE_DIR,id,f"profile_mini{ext}")
        if os.path.isfile(profile_path):
            return FileResponse(profile_path)
        else:
            return BASIC_PROFILE_RESPONSES['mini']
    
    @profile_router.post(PROFILE_URL+"/standard", summary="프로필 이미지 조회 standard")
    async def get_profile_standard(self,member_info:Member_upload=Body(...)):
        member_info = jsonable_encoder(member_info)
        id = member_info["id"]
        ext = await read_profile_ext(member_info)
        profile_path = os.path.join(STORAGE_DIR,id,f"profile_standard{ext}")
        if os.path.isfile(profile_path):
            return FileResponse(profile_path)
        else:
            return BASIC_PROFILE_RESPONSES['standard']
    
    @profile_router.post(PROFILE_URL+"/origin", summary="프로필 이미지 조회 origin")
    async def get_profile_origin(self,member_info:Member_upload=Body(...)):
        member_info = jsonable_encoder(member_info)
        id = member_info["id"]
        ext = await read_profile_ext(member_info)
        profile_path = os.path.join(STORAGE_DIR,id,f"profile_origin{ext}")
        if os.path.isfile(profile_path):
            return FileResponse(profile_path)
        else:
            return BASIC_PROFILE_RESPONSES['origin']
    
    @profile_router.post(PROFILE_URL+"/update", summary="프로필 이미지 업데이트")
    async def update_profile(self,background_tasks : BackgroundTasks, upload_file :UploadFile | None=None,member_info=Body(...)):
        member_info = jsonable_encoder(member_info)
        ext = Path(str(upload_file.filename)).suffix
        background_tasks.add_task(profile_image_delete,member_info)
        background_tasks.add_task(profile_image_save,upload_file,member_info,ext)
        return {"response":200}
    
    @profile_router.post(PROFILE_URL+"/delete", summary="프로필 이미지 삭제")
    async def delete_profile(self,background_tasks : BackgroundTasks,member_info:Member_upload=Body(...)):
        member_info = jsonable_encoder(member_info)
        background_tasks.add_task(profile_image_delete,member_info)
        return {"response":200}
    