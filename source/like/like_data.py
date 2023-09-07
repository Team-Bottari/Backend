from pydantic import BaseModel


class Like_create(BaseModel):
    posting_id:str
    member_id:int
    
class Cancle_like_create(BaseModel):
    posting_id:str
    member_id:int

class Like_list(BaseModel):
    member_id:int