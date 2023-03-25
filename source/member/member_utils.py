from settings import DDNS,PORT,VERSION
from config import EMAILS
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import smtplib


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