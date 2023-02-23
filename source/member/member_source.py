from fastapi.responses import JSONResponse
from fastapi_utils.cbv import cbv
from fastapi import UploadFile, File
from fastapi.encoders import jsonable_encoder
from config import MEMBER_URL
from fastapi_utils.inferring_router import InferringRouter
from db.database import engineconn
import os
from data import Member
from db.models import Member as Member_db
member_router = InferringRouter()

engine = engineconn()
session = engine.sessionmaker()

@cbv(member_router)
class MemberSource:
    @member_router.post(MEMBER_URL+"/sign_up")
    def sign_up(self, member_info: Member):
        member_info = jsonable_encoder(member_info)
        example = session.query(Member_db).all()
        print(example[0].id, example[0].nick_name)
        return member_info
        # return JSONResponse({"value":f"Version : {VERSION}"})


    @member_router.post(MEMBER_URL+"/image_upload")
    def image_upload(self, profile_image: UploadFile=File()):
        print(profile_image)
        return profile_image



    