import os

# Hyper-Params
DEPLOY_MODE = False
HOST = '192.168.0.32' if DEPLOY_MODE else '127.0.0.1'
PORT = 30000 if DEPLOY_MODE else 8000
VERSION = 'v1.0.0'
RELOAD = False if DEPLOY_MODE else True
WORKERS = os.cpu_count()*2 if DEPLOY_MODE else 1
DDNS = "wisixicidi.iptime.org" if DEPLOY_MODE else "localhost"

# DB Params
DB_USER = 'root'
DB_PASSWORD = 'rlatngusdlskarud'
DB_HOST = "192.168.0.32"
DB_PORT = 3307
DATABASE = 'gym'


# Docs Params
DOCS_URL = None if DEPLOY_MODE else "/docs"
REDOC_URL = None if DEPLOY_MODE else "/redoc"
