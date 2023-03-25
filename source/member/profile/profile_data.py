from pydantic import BaseModel,EmailStr

class Member_upload(BaseModel):
    email : EmailStr