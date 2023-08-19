from pydantic import BaseModel

class ChattingRoomModel(BaseModel):
    posting_id :str
    host_id : str
    client_id : str