from settings import DOCS_URL,REDOC_URL
from fastapi import FastAPI,Request
from source.member import member_router
from loguru import logger
from utils import request_parse,response_parse,make_log,make_run_bash
import os

app = FastAPI(docs_url=DOCS_URL,redoc_url=REDOC_URL,title = "GYM-Bottari")
app.include_router(member_router)




@app.on_event("startup")
async def init():
    logger.add("log/BackendServer_{time:YYYY-MM-DD}.log",format="<green>{time:YYYY-MM-DD HH:mm:ss}</green>\n<blue>{message}</blue>\n",rotation="1 days",enqueue=True)
    
    

@app.middleware("http")
async def watch_log(request: Request, call_next,):
    start_log,start_time = await request_parse(request)
    response = await call_next(request)
    end_log,end_time = await response_parse(response)
    log = make_log(start_log,end_log,start_time,end_time)
    logger.info(log,)
    return response

if __name__=="__main__":
    run_scripts = make_run_bash()
    os.system(run_scripts)