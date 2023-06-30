from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from config import CHATTING_URL
from fastapi.encoders import jsonable_encoder
from fastapi import WebSocket
from typing import List

chatting_router = InferringRouter()

"""
1. 한사람과 여러개의 채팅바잉 만들어질수있다. (게시글과 맵핑시켜야함)
2. 
"""


            



@cbv(chatting_router)
class Chatting:
    @chatting_router.get(CHATTING_URL+"/list")
    async def get_chatting_room_list(self,):
        return
    
    @chatting_router.post(CHATTING_URL)
    async def create_chatting_room(self,):
        return
    
    @chatting_router.get(CHATTING_URL)
    async def connect_chatting_root(self,):
        return
    
    
    
    
    
    