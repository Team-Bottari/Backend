from pydantic import BaseModel,EmailStr,Field

class Member_override(BaseModel):
    email : EmailStr

class Member_withdrawal(BaseModel):
    pw : str = Field(min_length=10,max_length=20)

class Member_signup(BaseModel):
    email : EmailStr
    pw : str = Field(min_length=10,max_length=20)
    nick_name : str = Field(min_length=2,max_length=20)
    name : str = Field(min_length=2,max_length=20)
    phone : str = Field(min_length=11,max_length=11)
    birth : str = Field(min_length=10,max_length=10)
    credit_rating : int = 100

class Member_login(BaseModel):
    email : EmailStr
    pw : str = Field(min_length=10,max_length=20)
    
class Member_findemail(BaseModel):
    name : str = Field(min_length=2,max_length=20)
    birth : str = Field(min_length=10,max_length=10)
    phone : str = Field(min_length=11,max_length=11)
    
class Member_findpw(BaseModel):
    email : EmailStr
    name : str = Field(min_length=2,max_length=20)
    birth : str = Field(min_length=10,max_length=10)
    
class Member_changepw(BaseModel):
    before_pw : str = Field(min_length=10,max_length=20)
    new_pw : str = Field(min_length=10,max_length=20)

class Member_checkpw(BaseModel):
    pw : str = Field(min_length=10,max_length=20)

class Member_update_info(BaseModel):
    nick_name : str = Field(min_length=2,max_length=20)
    name : str = Field(min_length=2,max_length=20)
    phone : str = Field(min_length=11,max_length=11)
    
class Token(BaseModel):
    access_token: str
    token_type: str
    email: str
    nick_name: str

    