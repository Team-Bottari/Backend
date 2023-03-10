import time
import ujson
import random
import smtplib
from settings import DEPLOY_MODE,HOST,PORT,RELOAD,WORKERS,DDNS,VERSION
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from starlette.concurrency import iterate_in_threadpool
from config import EMAILS
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

CHARSETS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def make_random_value():
    result = ""
    for i in range(16):
        result+=CHARSETS[random.randint(0,len(CHARSETS)-1)]
    return result


def make_run_bash():
    if DEPLOY_MODE:
        run_scripts = f"pip3 install -r requirements.txt\ngunicorn run:app\
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
        <p>요청에 동의하시면 아래 버튼을 눌러주세요.</p>
        <form action="http://{DDNS}:{PORT}/api/{VERSION}/verification/{key}",method="get">
            <button type>인증에 동의합니다.</button>
        </form>
    </body>
    </html>"""
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
    