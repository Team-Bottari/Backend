from pydantic import BaseModel

class ID(BaseModel):
    id:str

class ChattingRoomModel(BaseModel):
    posting_id :str
    host_id : str
    client_id : str
    
class ChattingRoomExit(BaseModel):
    posting_id :str
    host_id : str
    client_id : str
    request_client : str