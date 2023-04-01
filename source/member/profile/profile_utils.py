import os
import numpy as np
import ujson
import cv2
import base64
import aiofiles
from utils import write_image
from config import STORAGE_DIR
from io import BytesIO
from PIL import Image

async def uploadfile2array(uploadfile):
    return np.array(Image.open(BytesIO(await uploadfile.read())))

async def profile_image_save(uploadfile,member_info,ext):
    image_ = await uploadfile2array(uploadfile)
    member_info = ujson.loads(member_info)
    try:
        h,w,c = image_.shape
        if c==4:
            image = cv2.cvtColor(image_,cv2.COLOR_BGRA2RGBA)
        else:
            image = image_[:,:,::-1]
    except:
        error = image_.shape
        print(error)
        exit()
    try:
        os.makedirs(os.path.join(STORAGE_DIR,member_info['id'],))
    except:
        pass
    thumbnail_image = cv2.resize(image,(100,int(h*(100/w))))
    await write_profile_ext(member_info,ext)
    await write_image(thumbnail_image,os.path.join(STORAGE_DIR,member_info['id'],f"profile_mini{ext}"))
    standard_image = cv2.resize(image,(640,int(h*(640/w))))
    await write_image(standard_image,os.path.join(STORAGE_DIR,member_info['id'],f"profile_standard{ext}"))
    await write_image(image,os.path.join(STORAGE_DIR,member_info['id'],f"profile_origin{ext}"))

async def profile_image_save(request):
    request_list = await request.form()
    header,image_base64 = str(request_list["upload_file"]).split(",")
    image_bytes = base64.b64decode(image_base64)
    image_ = cv2.imdecode(np.fromstring(image_bytes,np.uint8),cv2.IMREAD_COLOR)
    ext = "."+header[header.find("/")+1:header.find(";")]
    member_info = ujson.loads(request_list["member_info"])
    try:
        h,w,c = image_.shape
        if c==4:
            image = cv2.cvtColor(image_,cv2.COLOR_BGRA2RGBA)
        else:
            image = image_[:,:,:]
    except:
        error = image_.shape
        print(error)
        exit()
    try:
        os.makedirs(os.path.join(STORAGE_DIR,"profiles",member_info["email"],))
    except:
        pass
    thumbnail_image = cv2.resize(image,(100,int(h*(100/w))))
    await write_profile_ext(member_info,ext)
    await write_image(thumbnail_image,os.path.join(STORAGE_DIR,"profiles",member_info["email"],f"profile_mini{ext}"),ext)
    standard_image = cv2.resize(image,(640,int(h*(640/w))))
    await write_image(standard_image,os.path.join(STORAGE_DIR,"profiles",member_info["email"],f"profile_standard{ext}"),ext)
    await write_image(image,os.path.join(STORAGE_DIR,"profiles",member_info["email"],f"profile_origin{ext}"),ext)
    
    
async def profile_image_delete(member_info):
    ext = await read_profile_ext(member_info)
    os.remove(os.path.join(STORAGE_DIR,"profiles",member_info["email"],f'profile_mini{ext}'))
    os.remove(os.path.join(STORAGE_DIR,"profiles",member_info["email"],f'profile_standard{ext}'))
    os.remove(os.path.join(STORAGE_DIR,"profiles",member_info["email"],f'profile_origin{ext}'))
    os.remove(os.path.join(STORAGE_DIR,"profiles",member_info["email"],'profile_ext.txt'))
    
async def read_profile_ext(member_info):
    try:
        async with aiofiles.open(os.path.join(STORAGE_DIR,"profiles",member_info["email"],"profile_ext.txt"), "r") as f:
            result = await f.readlines()
        return result[0].strip()
    except:
        return None

async def write_profile_ext(member_info,ext):
    async with aiofiles.open(os.path.join(STORAGE_DIR,"profiles",member_info["email"],"profile_ext.txt"),"w") as f:
        await f.write(ext)