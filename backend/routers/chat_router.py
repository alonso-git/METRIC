from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from services.AiService import run_message_analysis
from services.ChatService import set_recommendations, try_assign_agent
from entities.chat import chat_response
from services.AuthService import verify_user_is_client, verify_user_token, mark_user_active
from entities import message_post, Chat, Message
from database import db

chat = APIRouter(
    prefix="/chat",
    tags=["Chat Handling"]
)

@chat.post("/")
async def post_message(msg: message_post, db: Session = Depends(db), user: dict = Depends(verify_user_token)):
    chat_obj: Chat | None = None
    mark_user_active(user["user_id"], db)

    try:
        if msg.chat_id is None and user["role"] == "client":
            chat_obj = Chat(
                client_id = user["user_id"],
                agent_id = None
            )
            db.add(chat_obj)
            db.flush()
            msg.chat_id = chat_obj.id

            assigned = await try_assign_agent(chat_obj, db)
            if assigned:
                chat_obj.status = "in_progress"
            else:
                chat_obj.status = "pending_assignment"
        else:
            chat_obj = db.scalar(select(Chat).where(Chat.id == msg.chat_id))

        if chat_obj is None:
            raise HTTPException(404, "Chat not found")

        new_message: Message = Message(
            sender_id = user["user_id"],
            chat_id = chat_obj.id,
            raw = msg.raw
        )
        db.add(new_message)
        db.flush()

        analysis = await run_message_analysis(new_message, db)
        if analysis:
            chat_obj.overall_intent = analysis.intent
            chat_obj.recommendations = analysis.recommendations

        if user["role"] == "client":
            chat_obj.unread_agent = True
        else:
            chat_obj.unread_client = True

        db.commit()
        return {"ok": True, "chat_id": chat_obj.id}

    except IntegrityError:
        db.rollback()
        raise HTTPException(401, "Session invalid, please re-login")


@chat.get("/{chat_id}")
def get_chat_by_id(chat_id: int, db: Session = Depends(db), user: dict = Depends(verify_user_token)) -> chat_response | None:
    mark_user_active(user["user_id"], db)
    chat_obj = db.scalar(select(Chat).where(Chat.id == chat_id))

    if chat_obj is None or chat_obj.status == "closed":
        raise HTTPException(404, "Chat not found")

    is_agent = user["role"] == "agent"
    is_owner = (
        (is_agent and chat_obj.agent_id == user["user_id"])
        or (not is_agent and chat_obj.client_id == user["user_id"])
    )

    if not is_owner:
        raise HTTPException(403, "Chat does not belong to this user")

    set_recommendations(chat_obj, db)

    if is_agent:
        chat_obj.unread_agent = False
    else:
        chat_obj.unread_client = False

    db.commit()
    return chat_obj


@chat.patch("/close/{chat_id}")
def close_chat_by_id(chat_id: int, db: Session = Depends(db), user: dict = Depends(verify_user_is_client)):
    chat_obj = db.get(Chat, chat_id)
    if not chat_obj:
        raise HTTPException(404, "Chat not found")

    chat_obj.status = "closed"
    chat_obj.unread_agent = False
    chat_obj.unread_client = False
    db.commit()
