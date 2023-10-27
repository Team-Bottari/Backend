import time
import ujson
import random
import numpy as np
import aiofiles
import cv2
from settings import DEPLOY_MODE,HOST,PORT,WORKERS
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from starlette.concurrency import iterate_in_threadpool

CHARSETS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
def make_random_value():
    result = ""
    for i in range(16):
        result+=CHARSETS[random.randint(0,len(CHARSETS)-1)]
    return result

def make_run_bash():
    if DEPLOY_MODE:
        run_scripts = f"gunicorn run:app --workers {WORKERS} --worker-class uvicorn.workers.UvicornWorker --threads {WORKERS*2} --bind {HOST}:{PORT} --access-logfile - --error-logfile - --keep-alive 5"
        # run_scripts = f"uvicorn run:app --host={HOST} --port={PORT} --workers {WORKERS}"
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


async def write_image(image,full_path,ext):
    print(image.shape,ext,full_path)
    image_bytes = cv2.imencode(ext,image)[1].tobytes()
    async with aiofiles.open(full_path,"wb") as f:
        await f.write(image_bytes)
        
async def read_image(full_path):
    async with aiofiles.open(full_path,"rb") as f:
        image_bytes = await f.read()
    return cv2.imdecode(np.fromstring(image_bytes,dtype=np.uint8),cv2.IMREAD_COLOR)

async def write_json(json_object,path):
    json_object = ujson.dumps(json_object,indent=2)
    async with aiofiles.open(path,"w") as f:
        await f.write(json_object)
        
async def read_json(path):
    async with aiofiles.open(path) as f:
        return ujson.loads(await f.read())
