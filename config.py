from settings import VERSION
from pathlib import Path
import os

MAIN_DIR = str(Path(__file__).parent)
MAIN_URL = "/api"+f"/{VERSION}"

MEMBER_URL = MAIN_URL+"/member"


EMAILS = [
    {
        "email":"kimsuhyun72@naver.com",
        "password":"94a07s02d*fg",
        "smtp":"smtp.naver.com",
        "port":587
    }
]


