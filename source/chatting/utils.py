from fastapi import WebSocket
from typing import List


"""
1. 채팅방 클래스에는 무조건 2명이 포함된다.
2. 채팅방은 게시글에 종속적
3. 

"""


class ChattingRoom:
    def __init__(self) -> None:
        self.active_connections: List[WebSocket] = []
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)
            

class ChattingRoomManager:
    def __init__(self) -> None:
        self.active_root: List[ChattingRoom] = []
    
            

