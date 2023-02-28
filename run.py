from settings import HOST,PORT,RELOAD,WORKERS,DOCS_URL,REDOC_URL
from fastapi import FastAPI,Request
from source.member import member_router
from loguru import logger
from utils import request_parse,response_parse,make_log,make_run_bash
import asyncio
import os
import uvicorn

app = FastAPI(docs_url=DOCS_URL,redoc_url=REDOC_URL)
app.include_router(member_router)

@app.on_event("startup")
async def init():
    logger.add("log/BackendServer_{time:YYYY-MM-DD}.log",format="<green>{time:YYYY-MM-DD HH:mm:ss}</green>\n<blue>{message}</blue>\n",rotation="1 days",enqueue=True)
    
    

@app.middleware("http")
async def watch_log(request: Request, call_next,):
    start_log,start_time = request_parse(request)
    response = await call_next(request)
    end_log,end_time = response_parse(response)
    log = make_log(start_log,end_log,start_time,end_time)
    logger.info(log,)
    return response

if __name__=="__main__":
    make_run_bash()
    os.system("bash run.sh")
#     asyncio.run(uvicorn.run(
#         "run:app",
#         host=HOST,
#         port=PORT,
#         workers=WORKERS,
#         reload=RELOAD,
#         ))