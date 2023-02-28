from pydantic import BaseModel,EmailStr,Field
class Member_signup(BaseModel):
    id : EmailStr
    pw : str
    nick_name : str = Field(min_length=1,max_length=20)
    name : str
    phone : str = Field(min_length=11,max_length=11)
    birth : str = Field(min_length=10,max_length=10)
    status : bool=True
    credit_rating : int=100
