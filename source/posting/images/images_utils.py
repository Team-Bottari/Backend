import os
import numpy as np
import cv2
import shutil
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

async def uploadfile2array(uploadfile):
    return np.array(Image.open(BytesIO(await uploadfile.read())))

async def create_posting_image(posting_id,image_id,uploadfile):
    path = make_path(posting_id,image_id)
    origin = await uploadfile2array(uploadfile)
    mini = cv2.resize(origin,(100,100))
    standard = cv2.resize(origin,(640,640))
    os.makedirs(path)
    ext = str(Path(uploadfile.filename).suffix)
    await write_image(mini,path+"/mini"+ext,ext)
    await write_image(standard,path+"/standard"+ext,ext)
    await write_image(origin,path+"/origin"+ext,ext)

async def update_posting_image(posting_id,image_id,uploadfile):
    path = make_path(posting_id,image_id)
    image_names = os.listdir(path)
    map(lambda name : os.remove(os.path.join(path,name)),image_names)
    origin = await uploadfile2array(uploadfile)
    mini = cv2.resize(origin,(100,100))
    standard = cv2.resize(origin,(640,640))
    ext = str(Path(uploadfile.filename).suffix)
    await write_image(mini,path+"/mini"+ext,ext)
    await write_image(standard,path+"/standard"+ext,ext)
    await write_image(origin,path+"/origin"+ext,ext)

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
    
