from sqlalchemy import select
from sqlalchemy.orm import Session
from entities import Chat, User

async def try_assign_agent(chat: Chat, db: Session):
    chosen = db.scalars(select(User).where(User.role == "agent").where(User.isActive)).first()

    if chosen:
        chat.agent_id = chosen.id
        return True
    return False

def remove_pii(msg: str):
    pass