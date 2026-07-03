from fastapi import HTTPException
from sqlalchemy import desc, select
from sqlalchemy.orm import Session, joinedload
from entities import Chat, User, Message
import re

async def try_assign_agent(chat: Chat, db: Session):
    chosen = db.scalars(select(User).where(User.role == "agent").where(User.isActive)).first()

    if chosen:
        chat.agent_id = chosen.id
        return True
    return False

def remove_pii(msg: str):
    re_email = r'.@.\..'
    

def set_recommendations(chat: Chat, db: Session):
    latest_message = db.scalars(
        select(Message)
        .options(joinedload(Message.analysis))
        .where(Message.chat_id == chat.id)
        .order_by(desc(Message.time))
    ).first()

    if not latest_message:
        raise HTTPException(404, "Chat not found")
    else:
        analysis = latest_message.analysis
        chat.overall_intent = analysis.intent
        chat.recommendations = analysis.recommendations