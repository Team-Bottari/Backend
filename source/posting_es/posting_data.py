from pydantic import BaseModel,EmailStr
from typing import Any
class Posting_create(BaseModel):
    title:str
    content:str
    price:int
    email :EmailStr # example@google.com
    category:str
    can_discount:bool

class Posting_update(BaseModel):
    title:str = None
    content:str = None
    price:int = None
    category:str = None
    can_discount:bool = None

class Member_id_check(BaseModel):
    member_id:Any