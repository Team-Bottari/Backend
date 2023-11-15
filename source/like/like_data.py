from pydantic import BaseModel


class Like_create(BaseModel):
    posting_id:str
    
class Cancle_like_create(BaseModel):
    posting_id:str
