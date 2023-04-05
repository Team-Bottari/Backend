from pydantic import BaseModel


class Like_create(BaseModel):
    posting_id:int
    member_id:int
    
class Cancle_like_create(BaseModel):
    posting_id:int
    member_id:int