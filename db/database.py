from settings import HOST, DB_USER, DB_PASSWORD, DB_PORT, DATABASE
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

DB_URL = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{HOST}:{DB_PORT}/{DATABASE}'

class engineconn:
    def __init__(self):
        self.engine = create_engine(DB_URL, pool_recycle = 500)

    def sessionmaker(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        return session

    def connection(self):
        conn = self.engine.connect()
        return conn
    
engine = engineconn()
session = engine.sessionmaker()