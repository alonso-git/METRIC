from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from services.AiService import run_message_analysis
from services.ChatService import set_recommendations, try_assign_agent
from entities.chat import chat_response
from services.AuthService import verify_user_is_client, verify_user_token
from entities import message_post, Chat, Message
from database import db

from config import settings

chat = APIRouter(
    prefix="/chat",
    tags=["Chat Handling"]
)

@chat.post("/")
async def post_message(msg: message_post, db: Session = Depends(db), user: dict = Depends(verify_user_token)):
    chat: Chat | None = None
    print("pura vrg")

    if msg.chat_id is None and user["role"] == "client":
        chat = Chat(
            client_id = user["user_id"],
            agent_id = None
        )
        db.add(chat)
        db.flush()
        msg.chat_id = chat.id

        assigned = await try_assign_agent(chat, db)

        if assigned:
            chat.status = "in_progress"
        else:
            chat.status = "pending_assignment"
    else:
        chat = db.scalar(select(Chat).where(Chat.id == msg.chat_id))

    if chat is None:
        raise HTTPException(404, "No chat assigned to the agent")

    new_message: Message = Message(
        sender_id = user["user_id"],
        chat_id = chat.id,
        raw = msg.raw
    )

    db.add(new_message)
    db.flush()

    analysis = await run_message_analysis(new_message, db)
    if analysis:
        chat.overall_intent = analysis.intent
        chat.recommendations = analysis.recommendations

    if user["role"] == "client":
        chat.unread_agent = True
    else:
        chat.unread_client = True

    db.commit()

@chat.get("/{chat_id}")
def get_chat_by_id(chat_id: int, db: Session = Depends(db), user: dict = Depends(verify_user_token)) -> chat_response | None:
    chat = db.scalar(select(Chat).where(Chat.id == chat_id))
    print("oh que la vrg")

    if chat is None or chat.status == "closed":
        raise HTTPException(404, "Chat not found")
    
    if user["role"] == "agent" and chat.agent_id == user["user_id"]:
        if chat.unread_agent:
            set_recommendations(chat, db)
            chat.unread_agent = False
            db.commit()
            return chat
        else:
            return None
    
    if user["role"] == "client" and chat.client_id == user["user_id"] and chat.unread_client:
        if chat.unread_client:
            set_recommendations(chat, db)
            chat.unread_client = False
            db.commit()
            return chat
        else:
            return None

    raise HTTPException(403, "No chat with that id belongs to the user")

@chat.patch("/close/{chat_id}")
def close_chat_by_id(chat_id: int, db: Session = Depends(db), user: dict = Depends(verify_user_is_client)):
    chat = db.get(Chat, chat_id)

    if chat:
        chat.status = "closed"
        chat.unread_agent = False
        chat.unread_client = False
        db.commit()
    else:
        HTTPException(404, "Chat not found")