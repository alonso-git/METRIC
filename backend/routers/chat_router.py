from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from entities.chat import chat_response
from services.AuthService import verify_user_is_agent, verify_user_token
from entities import message_post, Chat, Message
from database import db

chat = APIRouter(
    prefix="/chat",
    tags=["Chat Handling"]
)

@chat.post("/")
def post_message(msg: message_post, db: Session = Depends(db), user: dict = Depends(verify_user_token)):
    chat: Chat | None = None

    if msg.chat_id is None and user["role"] == "client":
        chat = Chat(
            client_id = msg.sender_id,
            agent_id = None
        )
        db.add(chat)
        db.flush()
        msg.chat_id = chat.id
    elif msg.chat_id is not None:
        chat = db.scalar(select(Chat).where(Chat.id == msg.chat_id))

    if chat is None:
        raise HTTPException(404, "No chat assigned to the agent")

    new_message: Message = Message(
        sender_id = msg.sender_id,
        chat_id = chat.id,
        raw = msg.raw
    )

    db.add(new_message)

    chat.unread_agent = True if user["role"] == "client" else False
    chat.unread_client = True if user["role"] == "agent" else False
    chat.status = "open"

    db.commit()

@chat.get("/{chat_id}")
def get_message_by_id(chat_id: int, db: Session = Depends(db), user: dict = Depends(verify_user_token)) -> chat_response:
    chat = db.scalar(select(Chat).where(Chat.id == chat_id))

    if chat is None:
        raise HTTPException(404, "Chat not found")

    if user["role"] == "agent" and chat.agent_id == user["user_id"]:
        return chat
    
    if user["role"] == "client" and chat.client_id == user["user_id"]:
        return chat

    raise HTTPException(403, "No chat with that id belongs to the user")