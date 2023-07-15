import os

# Hyper-Params
DEPLOY_MODE = True
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

# ElasticSearchURL
ES_URL = "http://192.168.0.33:9200"
ES_USER = "elastic"
ES_PASSWORD = "94a07s02d*fg"
ES_SIZE = 20

# Admin Params
ADMIN_ID = "관리자"
ADMIN_PASSWORD = "rlatngusrladmstjqkrthdusdlskarud"

# Docs Params
DOCS_URL = "/docs" # None if DEPLOY_MODE else "/docs"
REDOC_URL =  "/redoc" # None if DEPLOY_MODE else "/redoc"

# token
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
SECRET_KEY = "3b04c2d18ca6b79c0c8c74a09ab6f26a5b278ff38feca16bf7744fa9b6ab9cfa"
ALGORITHM = "HS256"