from datetime import datetime

def delete_none_in_posting(posting):
    return { key:posting[key] for key in posting if posting[key] is not None}

def posting_update_data(posting,new_posting):
    now = datetime.now()
    now = datetime(now.year,now.month,now.day,now.hour,now.minute,now.second)
    posting.update(new_posting)
    posting["update_at"]=now
    return posting