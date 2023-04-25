import os
import numpy as np
import time
import cv2
import shutil
import aiofiles
from pathlib import Path
from io import BytesIO
from config import STORAGE_DIR
from PIL import Image
from utils import write_image

def make_path(posting_id,image_id):
    return os.path.join(STORAGE_DIR,"postings",str(posting_id).zfill(10),str(image_id).zfill(2))

def get_specific_path(posting_id,image_id,tag):
    path = make_path(posting_id,image_id)
    image_names = os.listdir(path)
    filename = list(filter(lambda x : tag in x,image_names))[0]
    return os.path.join(path,filename)

async def uploadfile2array(uploadfile,return_ext=False):
    name = "_".join(str(time.time()).split("."))+str(Path(uploadfile.filename).suffix)
    print("사이즈 : " , uploadfile.size)
    async with aiofiles.open(name,"wb+") as f:
        await f.write( uploadfile.file.read())
    image = cv2.imread(name)
    # os.remove(name)
    print(image)
    return image

def clear_path(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    os.makedirs(path)

def color_convert(image,ext):
    if ext.lower()==".jpg" or ext.lower()==".jpeg":
        return cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    elif ext.lower()==".png":
        return cv2.cvtColor(image,cv2.COLOR_BGRA2RGBA)
    else:
        return cv2.cvtColor(image,cv2.COLOR_BGR2RGB)

async def create_posting_image(posting_id,image_id,uploadfile):
    path = make_path(posting_id,image_id)
    
    origin = await uploadfile2array(uploadfile)
    ext = str(Path(uploadfile.filename).suffix)
    print(ext)
    print(type(origin))
    origin = color_convert(origin,ext)
    mini = cv2.resize(origin,(100,100))
    standard = cv2.resize(origin,(640,640))
    clear_path(path)
    await write_image(mini,path+"/mini"+ext,ext)
    await write_image(standard,path+"/standard"+ext,ext)
    await write_image(origin,path+"/origin"+ext,ext)
    index_sort(path)
    
async def update_posting_image(posting_id,image_id,uploadfile):
    path = make_path(posting_id,image_id)
    origin = await uploadfile2array(uploadfile)
    ext = str(Path(uploadfile.filename).suffix)
    origin = color_convert(origin,ext)
    mini = cv2.resize(origin,(100,100))
    standard = cv2.resize(origin,(640,640))
    clear_path(path)
    await write_image(mini,path+"/mini"+ext,ext)
    await write_image(standard,path+"/standard"+ext,ext)
    await write_image(origin,path+"/origin"+ext,ext)
    index_sort(path)

def index_sort(path):
    ppath = str(Path(path).parent)
    image_ids = sorted(os.listdir(ppath))
    count=1
    for id in image_ids:
        if str(count).zfill(2)==id:
            pass
        else:
            os.rename(os.path.join(ppath,id),os.path.join(ppath,str(count).zfill(2)))
        count+=1
        
def delete_posting_image(posting_id,image_id):
    path = make_path(posting_id,image_id)
    shutil.rmtree(path)
    ppath = str(Path(path).parent)
    image_ids = sorted(os.listdir(ppath))
    count=1
    for id in image_ids:
        if str(count).zfill(2)==id:
            pass
        else:
            os.rename(os.path.join(ppath,id),os.path.join(ppath,str(count).zfill(2)))
        count+=1
    
