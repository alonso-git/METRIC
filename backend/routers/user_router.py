from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext

from services.AuthService import verify_user_is_agent
from database import db
from entities import User, user_response

import models.auth.AuthDtos as auth

user = APIRouter(
    prefix="/users",
    tags=["Users Management"]
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

@user.post("/clients")
def create_client_user(user_data: auth.SigninDto, db: Session = Depends(db)) -> user_response:
    """
    Creates a new user with role "client"
    """
    try:
        new_user = User(
            name=user_data.name,
            email=user_data.email,
            password_hash=hash_password(user_data.password),
            role="client"
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered. Please use a different email."
        )
    except Exception as e:
        db.rollback()
        print(f"ERROR en /clients: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@user.post("/agents")
def create_agent_user(
    user_data: auth.SigninDto,
    db: Session = Depends(db)
) -> user_response:
    """
    Creates a new user with role "agent"
    """
    try:
        new_user = User(
            name=user_data.name,
            email=user_data.email,
            password_hash=hash_password(user_data.password),
            role="agent"
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered. Please use a different email."
        )
    except Exception as e:
        db.rollback()
        print(f"ERROR en /agents: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@user.get("/")
def get_users(db: Session = Depends(db), user: dict = Depends(verify_user_is_agent)):
    """Fetches all users (only for agents)."""
    users = db.scalars(select(User)).all()
    return users