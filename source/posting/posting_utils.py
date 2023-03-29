from datetime import datetime
from config import STORAGE_DIR
import shutil
import os

async def posting_create(posting,member_id):
    now = datetime.now()
    now = datetime(now.year,now.month,now.day,now.hour,now.minute,now.second)
    posting["create_at"] = now
    posting["views"]=0
    posting["like"]=0
    posting["update_nums"]=0
    posting["sold_out"]=False
    posting['remove']=False
    posting["update_at"]=now
    posting["member_id"]=member_id
    del posting["email"]
    return posting

def posting_update_at(posting):
    now = datetime.now()
    now = datetime(now.year,now.month,now.day,now.hour,now.minute,now.second)
    posting["update_at"]=now
    return posting

def posting2summaries(list_item):
    posting_summaries = ["posting_id", "title",'price','update_at','like','views']
    return [ { key:item["Posting"][key] for key in posting_summaries} for item in list_item]

def delete_none_in_posting(posting):
    return { key:posting[key] for key in posting if posting[key] is not None}

def create_posting_dir(posting_id):
    path = os.path.join(STORAGE_DIR,"postings",str(posting_id).zfill(10))
    if not os.path.isdir(path):
        os.mkdir(path)
        
def delete_posting_dir(posting_id):
    path = os.path.join(STORAGE_DIR,"postings",str(posting_id).zfill(10))
    shutil.rmtree(path)
    