from pydantic import BaseModel

class Member_signup(BaseModel):
    id : str
    pw : str
    nick_name : str
    name : str
    phone : str
    birth : str
    status : bool=True
    credit_rating : int=100
