from fastapi import WebSocket
from typing import List,Union
from pathlib import Path
from asyncinit import asyncinit
from config import CHATTINGROOM_DIR
from db import session, Member
from sqlalchemy import select, update
from fastapi.encoders import jsonable_encoder
from utils import write_json,read_json
import aiofiles
import os
import ujson


"""
1. 채팅방 클래스에는 무조건 2명이 포함된다.
2. 채팅방은 게시글에 종속적
3. 채팅내역은 Json으로 저장
{
    "chatting_room_id":~~~~~~~~,
    "posting_id":~~~~~~~~~~~,
    "host_id":~~~~~~~~~,
    "host_name":~~~~~~~~~~,
    "client_id":~~~~~~~~~~,
    "client_name":~~~~~~~~~~,
    "host_exit":false,
    "client_exit":false,
    "hosting_chatting_num":135,
    "client_chatting_num":246,
    "last-chatting_time":datetime.now(),
    "messages":[
        "host":{
            contents:"sdfsdfsdfsdfsdfsdfsdf",
            time:datetime~~~~~,
            'read':true/false
    ]
}

"""

@asyncinit
class ChattingRoom:
    async def __init__(self,posting_id:str,host_id:str,client_id:str,) -> None:
        self.posting_id = posting_id
        self.host_id = host_id
        self.client_id = client_id
        await self.load_chatting_room()
        self.active_connections: List[WebSocket] = []
        
        
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def get_last_ten(self):
        return self.chatting_data["chatting_list"][0:10]
        
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
        
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)
            
    def __del__(self,):
        pass
    
    async def create_chatting_room(self,path):
        host_query = select(Member).where(Member.member_id==self.host_id, Member.withdrawal == False, Member.certificate_status == True)
        host_result = await session.execute(host_query)
        client_query = select(Member).where(Member.member_id==self.client_id, Member.withdrawal == False, Member.certificate_status == True)
        client_result = await session.execute(client_query)
        host_info = host_result.first()
        host_info = jsonable_encoder(host_info[0])
        client_info = client_result.first()
        client_info = jsonable_encoder(client_info[0])
        chatting_data = {
            "posting_id":str(self.posting_id),
            "host_id":str(self.host_id),
            "host_name":str(host_info["nick_name"]),
            "client_id":str(self.client_id),
            "client_name":str(client_info["nick_name"]),
            "host_exit":False,
            "client_exit":False,
            "chatting_list":[]
        }
        await write_json(chatting_data,path)
    
    async def load_chatting_room(self):
        self.chattingroom_path = os.path.join(CHATTINGROOM_DIR,f"{self.posting_id}___{self.host_id}___{self.client_id}.json")
        if os.path.isfile(self.chattingroom_path):
            self.chatting_data = await read_json(self.chattingroom_path)
        else:
            await self.create_chatting_room(os.path.join(CHATTINGROOM_DIR,f"{self.posting_id}___{self.host_id}___{self.client_id}.json"))
            self.chatting_data = await read_json(self.chattingroom_path)




class ChattingRoomManager:
    def __init__(self):
        self.active_room = []
        
    def append(self,chattingroom:ChattingRoom):
        self.active_room.append(chattingroom)
        
    def remove(self,ids : List[str]):
        for index,room in enumerate(self.active_room):
            if (room[0]==ids[0]) and (room[1]==ids[1]) and (room[2]==ids[2]):
                del self.active_room[index]
            else:
                continue
    
    def is_active(self,ids : List[str]):
        for index,room in enumerate(self.active_room):
            if (room[0]==ids[0]) and (room[1]==ids[1]) and (room[2]==ids[2]):
                return index
            else:
                continue
        return -1
    
    async def activate_chatting_room(self,ids : List[str]):
        ids_list = [ [posting_id,host_id,client_id] for posting_id,host_id,client_id,_ in self.active_room]
        if  ids not in ids_list:
            self.append([ids[0],ids[1],ids[2],await ChattingRoom(ids[0],ids[1],ids[2])])
            return len(self.active_room)-1
        else:
            return ids_list.index(ids)
    
    def get_chatting_room(self,index):
        return self.active_room[index]


