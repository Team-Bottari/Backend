import os
from pathlib import Path
os.system(f"pip3 install -r {Path(__file__).parent/'requirements.txt'}")
from settings import DOCS_URL,REDOC_URL
from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from source.member import member_router
from source.verification import verification_router
from fastapi_utils.tasks import repeat_every
from loguru import logger
from db import engine
from admin import MyBackend
from sqladmin import Admin
from db import Member_Admin
from utils import request_parse,response_parse,make_log,make_run_bash


origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
    "http://wisixicidi.iptime.org",
    "http://wisixicidi.iptime.org:10000",
    "http://wisixicidi.iptime.org:30000",
    "https://gym-bottari.suveloper.com"
]



app = FastAPI(docs_url=DOCS_URL,redoc_url=REDOC_URL,title = "GYM-Bottari")
authentication_backend = MyBackend(secret_key="...")
admin = Admin(app ,engine.engine ,title="회원 관리자 페이지",authentication_backend=authentication_backend)
admin.add_view(Member_Admin)


app.include_router(member_router)
app.include_router(verification_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)





@app.on_event("startup")
async def init():
    logger.add("log/BackendServer_{time:YYYY-MM-DD}.log",format="<green>{time:YYYY-MM-DD HH:mm:ss}</green>\n<blue>{message}</blue>\n",rotation="1 days",enqueue=True)

# @app.middleware("http")
async def watch_log(request: Request, call_next,):
    start_log,start_time = await request_parse(request)
    response = await call_next(request)
    end_log,end_time = await response_parse(response)
    log = make_log(start_log,end_log,start_time,end_time)
    logger.info(log,)
    return response

@app.on_event("startup")
@repeat_every(seconds=24*60*60)
async def repeat_task():
    return

if __name__=="__main__":
    run_scripts = make_run_bash()
    os.system(run_scripts)