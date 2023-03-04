from settings import DOCS_URL,REDOC_URL
from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from source.member import member_router
from source.verification import verification_router
from loguru import logger
from db import engine
from sqladmin import Admin
from db import Member_Admin
from utils import request_parse,response_parse,make_log,make_run_bash
import os


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
admin = Admin(app ,engine.engine ,title="회원 관리자 페이지")


app.include_router(member_router)
app.include_router(verification_router)
admin.add_view(Member_Admin)

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