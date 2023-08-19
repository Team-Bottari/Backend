from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from config import CHATTING_URL
from fastapi.encoders import jsonable_encoder
from fastapi import WebSocket,WebSocketDisconnect
from .chatting_data import ChattingRoomModel
from settings import DDNS,PORT
from .utils import ChattingRoomManager
import asyncio
import ujson

chatting_router = InferringRouter()


@cbv(chatting_router)
class Chatting:
    chatting_room_manager = ChattingRoomManager()
    @chatting_router.post(CHATTING_URL+"/list")
    async def get_chatting_room_list(self,IDs:ChattingRoomModel):
        IDs = jsonable_encoder(IDs)
        return {"response":200,"chatting_list":[]}

    
    @chatting_router.post(CHATTING_URL+"/connect-chatting")
    async def check_chatting_room(self,IDs:ChattingRoomModel):
        IDs = jsonable_encoder(IDs)
        posting_id = IDs["posting_id"]
        host_id = IDs["host_id"]
        client_id = IDs["client_id"]
        # chatting_room_index = self.chatting_room_manager.is_active([posting_id,host_id,client_id])
        # if chatting_room_index<0:
        #     self.chatting_room_manager.activate_chatting_room([posting_id,host_id,client_id])
        return {"response":200,"url":f"ws://{DDNS}:{PORT}{CHATTING_URL}/{posting_id}/{host_id}/{client_id}"}
    
    @chatting_router.websocket(CHATTING_URL+"/{posting_id}/{host_id}/{client_id}")
    async def connecting_chatting_room(self,websocket:WebSocket,posting_id:str,host_id:str,client_id:str):
        index = await self.chatting_room_manager.activate_chatting_room([posting_id,host_id,client_id])
        p,h,c,chatting_room = self.chatting_room_manager.get_chatting_room(index)
        await chatting_room.connect(websocket)
        try:
            while True:
                data = await websocket.receive_text()
                data = ujson.loads(data)
                await chatting_room.broadcast(str(data))
        except:
            chatting_room.disconnect(websocket)
    
    
    @chatting_router.post(CHATTING_URL+"/disconnect-chatting")
    async def disconnecting_chatting_room(self,):
        IDs = jsonable_encoder(IDs)
        return
    
    @chatting_router.delete(CHATTING_URL+"/exiting-chatting")
    async def exit_chatting_room(self,):
        IDs = jsonable_encoder(IDs)
        return
    
    
    
    
    
    