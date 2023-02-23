from pydantic import BaseModel
# from typing import Any
class Member(BaseModel):
    id : str
    pw : str=None
    nickname : str=None
    name : str=None
    phone : str=None
    birth : str=None
