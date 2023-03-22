import time
import ujson
import random
import smtplib
import numpy as np
import aiofiles
import cv2
import os
import shutil
from settings import DEPLOY_MODE,HOST,PORT,WORKERS,DDNS,VERSION
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from starlette.concurrency import iterate_in_threadpool
from config import EMAILS,STORAGE_DIR,MAIN_DIR
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from io import BytesIO
from PIL import Image
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

def make_certificate_html(key):
    # <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    HTML = f"""
    <html>
    <head>
    <meta charset="utf-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <title>Page Title</title>
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <link rel="stylesheet" type="text/css" media="screen" href="main.css" />
    <script src="main.js"></script>
    </head>
    <body>
    <div style="
        border: 2px solid rgb(81, 13, 229);
        background-color: rgb(255, 255, 255);
        border-left: 0px;
        border-right: 0px;
        border-bottom: 1px dotted black;
        margin: auto;

        width: 500px;
        height: 500px;
        position: relative;
        top: 30px;
    ">
    <header style="line-height: 3px; text-align: center">
    <p style="margin:10px">Gym-bottari</p>

    <p style="
        color: rgb(81, 13, 229);
        font-size: 30px;
        line-height: 10px;
        font-weight: bold;
        margin:20px
        ">
        이메일 인증
    </p>
    </header>
    <p style="font-size: 20px; color: black">
    안녕하세요 GYM-Bottari 입니다.
    <br>

    메일 인증 요청에 동의하시면 아래 인증동의 버튼을 눌러 회원가입을
    진행해주세요.이용해주셔서 감사합니다.
    </p>

    <form
        action="http://{DDNS}:{PORT}/api/{VERSION}/verification/{key}"
        ,method="get"
    >
        <button
        style="
            color: rgb(81, 13, 229);

            background-color: rgb(81, 13, 229);
            color: white;
            border: rgb(81, 13, 229);
            height: 30px;
            width: 150px;
        "
        >
        인증동의
        </button>
    </form>
    </div>
    </body>
    </html>
    """
    return HTML

def make_passwd_html(key):
    HTML = f"""
    <html>
        <head>
            <meta charset='utf-8'>
            <meta http-equiv='X-UA-Compatible' content='IE=edge'>
            <title>Page Title</title>
            <meta name='viewport' content='width=device-width, initial-scale=1'>
            <link rel='stylesheet' type='text/css' media='screen' href='main.css'>
            <script src='main.js'></script>
        </head>
    <body>
        <div>
            <h3>안녕하세요 GYM-Bottari 입니다.</h3>
        </div>
        <p>새로운 비밀번호는 <b>{key}<b></p>
    </body>
    </html>"""
    return HTML

def send_certificate_email(recvEmail,key):
    sendEmail = EMAILS[0]["email"]
    password = EMAILS[0]["password"]
    smtpName = EMAILS[0]["smtp"]
    smtpPort = EMAILS[0]["port"]
    message = MIMEMultipart("alternative")
    message['Subject'] ="안녕하세요. GYM-Bottari 입니다."
    message['From'] = sendEmail
    message['To'] = recvEmail
    html = make_certificate_html(key)
    part = MIMEText(html , "html")
    message.attach(part)
    s=smtplib.SMTP( smtpName , smtpPort ) #메일 서버 연결
    s.starttls() #TLS 보안 처리
    s.login( sendEmail , password ) #로그인
    s.sendmail( sendEmail, recvEmail, message.as_string()) #메일 전송, 문자열로 변환하여 보냅니다.
    s.close() #smtp 서버 연결을 종료합니다.
    

def send_pw_mail(recvEmail,key):
    sendEmail = EMAILS[0]["email"]
    password = EMAILS[0]["password"]
    smtpName = EMAILS[0]["smtp"]
    smtpPort = EMAILS[0]["port"]
    message = MIMEMultipart("alternative")
    message['Subject'] ="안녕하세요. GYM-Bottari 입니다."
    message['From'] =  sendEmail
    message['To'] = recvEmail
    html = make_passwd_html(key)
    part = MIMEText(html , "html")
    message.attach(part)
    s=smtplib.SMTP( smtpName , smtpPort ) #메일 서버 연결
    s.starttls() #TLS 보안 처리
    s.login( sendEmail , password ) #로그인
    s.sendmail( sendEmail, recvEmail, message.as_string(),) #메일 전송, 문자열로 변환하여 보냅니다.
    s.close() #smtp 서버 연결을 종료합니다.
    
async def uploadfile2array(uploadfile):
    return np.array(Image.open(BytesIO(await uploadfile.read())))

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

async def init_fake_db():
    if os.path.isdir(os.path.join(MAIN_DIR,'fake-posting-db')):
        if os.path.isfile(os.path.join(MAIN_DIR,'fake-posting-db',"simples.json")):
            return
        else:
            await write_fake_simple_db([])
    else:
        os.mkdir(os.path.join(MAIN_DIR,'fake-posting-db'))
        await write_fake_simple_db([])

async def read_fake_simple_db(keyword=None):
    async with aiofiles.open(os.path.join(MAIN_DIR,"fake-posting-db","simples.json"),"r") as f:
        postings = ujson.loads( await f.read())
    if keyword is None:
        return postings
    return list(filter(lambda x:keyword in x['title'],postings))

def add_fake_simple_db(db,posting):
    del posting["content"]
    del posting["images"]
    db.append(posting)
    return db

async def write_fake_simple_db(json_object):
    async with aiofiles.open(os.path.join(MAIN_DIR,"fake-posting-db","simples.json"),"w") as f:
        await f.write(ujson.dumps(json_object,indent=2,ensure_ascii=False))

    