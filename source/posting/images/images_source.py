from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from fastapi import UploadFile,File
from fastapi.responses import FileResponse
from fastapi.background import BackgroundTasks
from .images_utils import create_posting_image,update_posting_image,delete_posting_image,get_specific_path
from config import POSTING_IMAGES_URL
import os

posting_images_router = InferringRouter()

@cbv(posting_images_router)
class Images:
    @posting_images_router.posting(POSTING_IMAGES_URL+"/{posting_id}/{image_id}/upload")
    async def create_image(self,background_task:BackgroundTasks,posting_id:str=None,image_id:str=None,upload_file:UploadFile=File(...)):
        await create_posting_image(posting_id,image_id,upload_file)
        return {"response":200}
    @posting_images_router.posting(POSTING_IMAGES_URL+"/{posting_id}/{image_id}/mini")
    async def read_mini_image(self,background_task:BackgroundTasks,posting_id:str,image_id:str):
        path = get_specific_path(posting_id,image_id,tag="mini")
        return FileResponse(path)
    @posting_images_router.posting(POSTING_IMAGES_URL+"/{posting_id}/{image_id}/standard")
    async def read_standard_image(self,background_task:BackgroundTasks,posting_id:str,image_id:str):
        path = get_specific_path(posting_id,image_id,tag="standard")
        return FileResponse(path)
    @posting_images_router.posting(POSTING_IMAGES_URL+"/{posting_id}/{image_id}/origin")
    async def read_origin_image(self,posting_id:str,image_id:str):
        path = get_specific_path(posting_id,image_id,tag="origin")
        return FileResponse(path)
    ############################################# 밑에는 만들어야함 ######################################################################
    @posting_images_router.posting(POSTING_IMAGES_URL+"/{posting_id}/{image_id}/update")
    async def update_image(self,background_task:BackgroundTasks,posting_id:str,image_id:str,upload_file:UploadFile=File(...)):
        await update_posting_image(posting_id,image_id,upload_file)
        return {"response":200}
    @posting_images_router.posting(POSTING_IMAGES_URL+"/{posting_id}/{image_id}/delete")
    async def delete_image(self,background_task:BackgroundTasks,posting_id:str,image_id:str):
        background_task.add(delete_posting_image,posting_id,image_id)
        return {"response":200}
    