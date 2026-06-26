from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from passlib.context import CryptContext

from services.AuthService import verify_user_is_agent
from database import db
from entities import User, User_response

import models.auth.AuthDtos as auth

user = APIRouter(
    prefix="/users",
    tags=["Users Management"] # Groups these endpoints in the Swagger UI
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)

@user.post("/clients")
def create_client_user(user_data: auth.SigninDto, db: Session = Depends(db)) -> User_response:
    """
    Creates a new user with role "client"
    """

    new_user = User(
        name = user_data.name,
        email = user_data.email,
        password_hash = hash_password(user_data.password),
        role = "client"
    )

    db.add(new_user)

    db.commit()
    db.refresh(new_user)
    
    return new_user

@user.post("/agents")
def create_agent_user(
    user_data: auth.SigninDto,
    db: Session = Depends(db),
    user: dict = Depends(verify_user_is_agent)
) -> User_response:
    """
    Creates a new user with role "client"
    """

    new_user = User(
        name = user_data.name,
        email = user_data.email,
        password_hash =hash_password(user_data.password),
        role = "agent"
    )

    db.add(new_user)

    db.commit()
    db.refresh(new_user)
    
    return new_user

@user.get("/")
def get_users(db: Session = Depends(db), user: dict = Depends(verify_user_is_agent)):
    """Fetches a specific user by ID."""
    
    users = db.scalars(select(User)).all()
    
    return users