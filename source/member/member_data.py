from pydantic import BaseModel,EmailStr,Field

class Member_override(BaseModel):
    id : EmailStr

class Member_info_check(BaseModel):
    id : EmailStr

class Member_info_

class Member_signup(BaseModel):
    id : EmailStr
    pw : str = Field(min_length=10,max_length=20)
    nick_name : str = Field(min_length=2,max_length=20)
    name : str = Field(min_length=2,max_length=20)
    phone : str = Field(min_length=11,max_length=11)
    birth : str = Field(min_length=10,max_length=10)
    status : bool = True
    credit_rating : int = 100

class Member_login(BaseModel):
    id : EmailStr
    pw : str = Field(min_length=10,max_length=20)
    
class Member_findemail(BaseModel):
    name : str = Field(min_length=2,max_length=20)
    birth : str = Field(min_length=10,max_length=10)
    
class Member_findpw(BaseModel):
    id : EmailStr
    name : str = Field(min_length=2,max_length=20)
    birth : str = Field(min_length=10,max_length=10)
    
class Member_changepw(BaseModel):
    id : EmailStr
    before_pw : str = Field(min_length=10,max_length=20)
    new_pw : str = Field(min_length=10,max_length=20)
