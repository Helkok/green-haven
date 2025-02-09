import asyncio
from typing import List, Dict

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from starlette.requests import Request
from starlette.websockets import WebSocket, WebSocketDisconnect

from app.utils.user import current_user
from app.DAO.base import MessageDAO

router = APIRouter()


class MessageRead(BaseModel):
    user_from: int = Field(..., description="ID отправителя сообщения")
    user_to: int = Field(..., description="ID получателя сообщения")
    message: str = Field(..., description="Содержимое сообщения")


class MessageCreate(BaseModel):
    user_to: int = Field(..., description="ID получателя сообщения")
    message: str = Field(..., description="Содержимое сообщения")


@router.get("/messages/{user_id}", response_model=List[MessageRead])
async def get_messages(user_id: int, current_user: current_user, request: Request):
    return await MessageDAO.get_messages_between_users(user_id_1=user_id, user_id_2=current_user.id,
                                                       session=request.state.db) or []


@router.post("/messages", response_model=MessageCreate)
async def send_message(message: MessageCreate, curr_user: current_user, request: Request):
    # Добавляем новое сообщение в базу данных
    await MessageDAO.add(
        user_from=curr_user.id,
        message=message.message,
        user_to=message.user_to,
        session=request.state.db
    )

    # Подготавливаем данные для отправки сообщения
    message_data = {
        'user_from': curr_user.id,
        'user_to': message.user_to,
        'message': message.message,
    }

    # Уведомляем получателя и отправителя через WebSocket
    await notify_user(message.user_to, message_data)
    await notify_user(curr_user.id, message_data)

    # Возвращаем подтверждение сохранения сообщения
    return {'user_to': message.user_to, 'message': message.message, 'status': 'ok', 'msg': 'Message saved!'}


active_connections: Dict[int, WebSocket] = {}


async def notify_user(user_id: int, message: dict):
    """Отправить сообщение пользователю, если он подключен."""
    if user_id in active_connections:
        websocket = active_connections[user_id]
        try:
            # Отправляем сообщение в формате JSON
            await websocket.send_json(message)
        except Exception as e:
            print(f"Error sending message to {user_id}: {e}")


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    """Обрабатывает подключение WebSocket пользователя."""
    await websocket.accept()
    active_connections[user_id] = websocket
    try:
        while True:
            await asyncio.sleep(1)  # Поддерживаем соединение
    except WebSocketDisconnect:
        # Удаляем пользователя из активных соединений при отключении
        active_connections.pop(user_id, None)
        print(f"User {user_id} disconnected.")
