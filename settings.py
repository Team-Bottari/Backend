# Hyper-Params
DEPLOY_MODE = False
HOST = '192.168.0.32' if DEPLOY_MODE else '127.0.0.1'
PORT = 30000 if DEPLOY_MODE else 8000
VERSION = 'v1.0.0'
RELOAD = False if DEPLOY_MODE else True
WORKERS = 8 if DEPLOY_MODE else 1

DB_USER = 'root'
DB_PASSWORD = 'rlatngusdlskarud'
DB_PORT = 3307
DATABASE = 'gym'