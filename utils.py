import time
import ujson
from settings import DEPLOY_MODE,HOST,PORT,RELOAD,WORKERS
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from starlette.concurrency import iterate_in_threadpool


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
    return f"\t응답코드 : {response.status_code}\n\t결과타입 : {response.headers['content-type']}\n\t결과JSON : \n{body_string}",time.time()

def make_log(start_log,end_log,start_time,end_time):
    return start_log+"\n"+end_log+f"\n\t처리시간 : {str(end_time-start_time)[:7]}"