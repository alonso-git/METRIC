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
                return user_login_response(
                    access_token = AuthService.create_access_token(user.id, user.role),
                    token_type = "bearer",
                    user = user
                )
        except UnknownHashError:
            pass
            
    
    raise HTTPException(401, "Incorrect email or password")

@auth.get("/my-profile")
def get_profile(current_user: dict = Depends(AuthService.verify_user_token)):
    # You already have the role and user_id here!
    return {"message": f"Hello user {current_user['user_id']}, your role is {current_user['role']}"}