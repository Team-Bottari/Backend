from pydantic import BaseModel

class Posting_create(BaseModel):
    title:str
    content:str
    price:int
    member_id :str # example@google.com
    category:str
    can_discount:bool
    