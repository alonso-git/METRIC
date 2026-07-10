from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from passlib.context import CryptContext
from passlib.exc import UnknownHashError

from entities.user import user_login_response
from database import db
from entities import User

from models.auth.AuthDtos import LoginDto
from services import AuthService

auth = APIRouter(
    prefix="/auth",
    tags=["Users Authentication"]
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@auth.post("/login")
def login(credentials: LoginDto, db: Session = Depends(db)) ->  user_login_response:
    stmt = select(User).where(User.email == credentials.email)

    user = db.scalars(stmt).one_or_none()

    if user:
        try:
            if pwd_context.verify(credentials.password, user.password_hash):
                AuthService.mark_user_active(user.id, db)
                db.commit()
                return user_login_response(
                    access_token = AuthService.create_access_token(user.id, user.role),
                    token_type = "bearer",
                    user = user
                )
        except UnknownHashError:
            pass
            
    
    raise HTTPException(401, "Incorrect email or password")

@auth.get("/my-profile")
def get_profile(db: Session = Depends(db), user: dict = Depends(AuthService.verify_user_token)):
    AuthService.mark_user_active(user["user_id"], db)

    db_user = db.scalars(select(User).where(User.id == user["user_id"])).one_or_none()

    if user["role"] == "agent":
        agent_chat = None
        for c in (db_user.agent_chats or []):
            if c.status != "closed":
                agent_chat = {"id": c.id, "status": c.status, "client_id": c.client_id}
                break
        db.commit()
        return {
            "message": f"Hello user {user['user_id']}, your role is {user['role']}",
            "agent_chat": agent_chat,
        }

    client_chat = None
    for c in (db_user.client_chats or []):
        if c.status != "closed":
            client_chat = {"id": c.id, "status": c.status, "agent_id": c.agent_id}
            break

    db.commit()
    return {
        "message": f"Hello user {user['user_id']}, your role is {user['role']}",
        "client_chat": client_chat,
    }
