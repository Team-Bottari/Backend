import time
from settings import DEPLOY_MODE,HOST,PORT,RELOAD,WORKERS

def make_run_bash():
    if DEPLOY_MODE:
        with open("run.sh","w") as f:
            f.write("#!/bin/bash\n")
            f.write(f"gunicorn run:app --workers {WORKERS} --worker-class uvicorn.workers.UvicornWorker --bind {HOST}:{PORT}")
    else:
        with open("run.sh","w") as f:
            f.write("#!/bin/bash\n")
            f.write(f"uvicorn run:app --host={HOST} --port={PORT}")



def request_parse(request):
    return f"\tMethod : {request.method}\n\t여기에서 : {request.client.host}:{request.client.port}\n\t여기로 : {request.url}",time.time()

def response_parse(response):
    return f"\t응답코드 : {response.status_code}\n\t결과타입 : {response.headers['content-type']}",time.time()

def make_log(start_log,end_log,start_time,end_time):
    return start_log+"\n"+end_log+f"\n\t처리시간 : {str(end_time-start_time)[:7]}"