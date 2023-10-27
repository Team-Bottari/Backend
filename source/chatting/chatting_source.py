from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from config import CHATTING_URL
from fastapi.encoders import jsonable_encoder
from fastapi import WebSocket,WebSocketDisconnect
from .chatting_data import ChattingRoomModel,ID,ChattingRoomExit
from settings import DDNS,PORT
from .utils import ChattingRoomManager
import asyncio
import ujson
import aiohttp
import random
from fastapi import WebSocket, WebSocketDisconnect, status
from typing import Optional,Any


chatting_router = InferringRouter()

@cbv(chatting_router)
class Chatting:
    @chatting_router.post(CHATTING_URL+"/list")
    async def get_chatting_room_list(self,ID:ID):
        ID = jsonable_encoder(ID)
        session = aiohttp.ClientSession()
        async with session.get(f"http://192.168.0.33:{30001+random.randint(0,9)}/chatting-list/{ID['id']}") as response:
            chatting_list = await response.json()
        return {"response":200,"chatting_list":chatting_list["chatting_list"]}

    
    @chatting_router.post(CHATTING_URL+"/connect-chatting")
    async def check_chatting_room(self,IDs:ChattingRoomModel):
        IDs = jsonable_encoder(IDs)
        posting_id = IDs["posting_id"]
        host_id = IDs["host_id"]
        client_id = IDs["client_id"]
        WEBSOCKET_PORT = PORT+int(str(int(host_id)+int(client_id))[-1])+1
        return {"response":200,"url":f"ws://{DDNS}:{WEBSOCKET_PORT}/chatting-socket/{posting_id}/{host_id}/{client_id}"}
    
    @chatting_router.post(CHATTING_URL+"/exiting-chatting")
    async def exit_chatting_room(self,IDs:ChattingRoomExit):
        IDs = jsonable_encoder(IDs)
        posting_id = IDs["posting_id"]
        host_id = IDs["host_id"]
        client_id = IDs["client_id"]
        request_client = IDs["request_client"]
        session = aiohttp.ClientSession()
        WEBSOCKET_PORT = PORT+int(str(int(host_id)+int(client_id))[-1])+1
        async with session.delete(f"http://192.168.0.33:{WEBSOCKET_PORT}/chatting-exit/{posting_id}/{host_id}/{client_id}/{request_client}") as response:
            resp = await response.json()
        return {"response":200}
    
    
    
    
    