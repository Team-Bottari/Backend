import time
import ujson
import random
import numpy as np
import aiofiles
import cv2
import os
from settings import DEPLOY_MODE,HOST,PORT,WORKERS
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from starlette.concurrency import iterate_in_threadpool
from config import STORAGE_DIR
from datetime import datetime
import base64

CHARSETS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
def make_random_value():
    result = ""
    for i in range(16):
        result+=CHARSETS[random.randint(0,len(CHARSETS)-1)]
    return result


def make_run_bash():
    if DEPLOY_MODE:
        run_scripts = f"gunicorn run:app\
            --workers {WORKERS}\
            --worker-class uvicorn.workers.UvicornWorker\
            --threads {WORKERS*3}\
            --bind {HOST}:{PORT}\
            --access-logfile -\
            --error-logfile -\
            --keep-alive 5"
    else:
        run_scripts = f"uvicorn run:app --host={HOST} --port={PORT} --reload"
    return run_scripts

async def set_body(request: Request, body: bytes):
    async def receive():
        return {'type': 'http.request', 'body': body}
    request._receive = receive

async def request_parse(request):
    req_body = await request.body()
    await set_body(request, req_body)
    try:
        body = ujson.loads(jsonable_encoder(req_body))
        body_string = "\n".join([ f"\t\t{key} : {body[key]}" for key in body])
        
    except:
        body_string = ""
    return f"\tMethod : {request.method}\n\t여기에서 : {request.client.host}:{request.client.port}\n\t여기로 : {request.url}\n\t요청JSON : \n{body_string}",time.time()

async def response_parse(response):
    response_body = [chunk async for chunk in response.body_iterator]
    response.body_iterator = iterate_in_threadpool(iter(response_body))
    try:
        body = ujson.loads(response_body[0].decode())
        body_string = "\n".join([ f"\t\t{key} : {body[key]}" for key in body])
    except:
        body_string=""
    if not hasattr(response.headers,"content-type"):
        content_type="else"
    else:
        content_type=response.headers["content-type"]
    return f"\t응답코드 : {response.status_code}\n\t결과타입 : {content_type}\n\t결과JSON : \n{body_string}",time.time()

def make_log(start_log,end_log,start_time,end_time):
    return start_log+"\n"+end_log+f"\n\t처리시간 : {str(end_time-start_time)[:7]}"


async def write_image(image,full_path):
    image_bytes = cv2.imencode(".jpg",image[:,:,:])[1].tobytes()
    async with aiofiles.open(full_path,"wb") as f:
        await f.write(image_bytes)
        
async def read_image(full_path):
    async with aiofiles.open("full_path","rb") as f:
        image_bytes = await f.read()
    return cv2.imdecode(np.fromstring(image_bytes,dtype=np.uint8),cv2.IMREAD_COLOR)

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
    ext = header[header.find("/")+1:header.find(";")]
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
        os.makedirs(os.path.join(STORAGE_DIR,member_info['id'],))
    except:
        pass
    thumbnail_image = cv2.resize(image,(100,int(h*(100/w))))
    await write_profile_ext(member_info,ext)
    await write_image(thumbnail_image,os.path.join(STORAGE_DIR,member_info['id'],f"profile_mini{ext}"))
    standard_image = cv2.resize(image,(640,int(h*(640/w))))
    await write_image(standard_image,os.path.join(STORAGE_DIR,member_info['id'],f"profile_standard{ext}"))
    await write_image(image,os.path.join(STORAGE_DIR,member_info['id'],f"profile_origin{ext}"))
    
    
async def profile_image_delete(member_info):
    ext = await read_profile_ext(member_info)
    os.remove(os.path.join(STORAGE_DIR,member_info['id'],f'profile_mini{ext}'))
    os.remove(os.path.join(STORAGE_DIR,member_info['id'],f'profile_standard{ext}'))
    os.remove(os.path.join(STORAGE_DIR,member_info['id'],f'profile_origin{ext}'))
    os.remove(os.path.join(STORAGE_DIR,member_info['id'],'profile_ext.txt'))
    
async def read_profile_ext(member_info):
    try:
        async with aiofiles.open(os.path.join(STORAGE_DIR,member_info['id'],"profile_ext.txt"), "r") as f:
            result = await f.readlines()
        return result[0].strip()
    except:
        return None

async def write_profile_ext(member_info,ext):
    async with aiofiles.open(os.path.join(STORAGE_DIR,member_info['id'],"profile_ext.txt"),"w") as f:
        await f.write(ext)


async def update_poting_create(posting,member_id):
    posting["create_at"] = datetime.now()
    posting["views"]=0
    posting["like"]=0
    posting["update_nums"]=0
    posting["sold_out"]=False
    posting["update_date"]=datetime.now()
    posting["member_id"]=member_id
    return posting