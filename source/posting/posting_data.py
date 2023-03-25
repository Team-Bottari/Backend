from pydantic import BaseModel

class Posting_create(BaseModel):
    title:str
    content:str
    price:int
    email :str # example@google.com
    category:str
    can_discount:bool
    