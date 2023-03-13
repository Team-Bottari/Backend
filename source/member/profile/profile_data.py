from pydantic import BaseModel,EmailStr

class Member_upload(BaseModel):
    id : EmailStr