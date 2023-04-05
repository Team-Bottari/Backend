from settings import VERSION
from pathlib import Path

MAIN_DIR = str(Path(__file__).parent)
MAIN_URL = "/api"+f"/{VERSION}"

MEMBER_URL = MAIN_URL+"/member"
PROFILE_URL = MEMBER_URL+"/profile"
VERIFICATION_URL = MAIN_URL+"/verification/{random_value}"

POSTING_URL = MAIN_URL+"/posting"
POSTING_IMAGES_URL = MAIN_URL+"/images"
LIKE_URL = MAIN_URL + '/like'
EMAILS = [
    {
        "email":"kimsuhyun72@naver.com",
        "password":"94a07s02d*fg",
        "smtp":"smtp.naver.com",
        "port":587
    }
]

STORAGE_DIR = "/home/hdd_0"

