from datetime import datetime
from config import STORAGE_DIR
import shutil
import os

def get_image_name(posting_id,image_id,target="mini"):
    path = os.path.join(STORAGE_DIR,"postings",str(posting_id).zfill(10),str(image_id).zfill(2),)
    image_name = list(filter(lambda x : target in x,os.listdir(path)))[0]
    return os.path.join(path,image_name)

def get_image_path(posting_id,target="mini"):
    posting_id = str(posting_id).zfill(10)
    posting_path = os.path.join(STORAGE_DIR,"postings",posting_id)
    if len(os.listdir(posting_path))>0:
        return get_image_name(posting_id,1,target=target)
    else:
        return None

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
    return posting

def posting_update_data(posting,new_posting):
    now = datetime.now()
    now = datetime(now.year,now.month,now.day,now.hour,now.minute,now.second)
    posting.update(new_posting)
    posting["update_at"]=now
    return posting

def dic2image_indexes(dic):
    posting_id = str(dic["posting_id"]).zfill(10)
    dic["posting_images"] = sorted([ int(index) for index in os.listdir(os.path.join(STORAGE_DIR,"postings",posting_id))])
    return dic

def posting2summaries(list_item):
    posting_summaries = ["posting_id", "title",'price','update_at','like','views']
    results = [ { key:item["Posting"][key] for key in posting_summaries} for item in list_item]
    return list(map(dic2image_indexes,results))

def delete_none_in_posting(posting):
    return { key:posting[key] for key in posting if posting[key] is not None}

def create_posting_dir(posting_id):
    path = os.path.join(STORAGE_DIR,"postings",str(posting_id).zfill(10))
    if not os.path.isdir(path):
        os.mkdir(path)
        
def delete_posting_dir(posting_id):
    path = os.path.join(STORAGE_DIR,"postings",str(posting_id).zfill(10))
    shutil.rmtree(path)

def add_images_list(posting):
    target_path = os.path.join(STORAGE_DIR,"postings",posting["posting_id"])
    posting["posting_images"] = sorted([ path for path in os.listdir(target_path)])
    return posting