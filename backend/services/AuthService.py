from fastapi import Depends
from sqlalchemy import select
from database import db
from sqlalchemy.orm import Session

from entities.user import User
from models.auth.AuthDtos import LoginDto
from config import settings

import jwt
from datetime import datetime, timedelta, timezone

def verify_user_credentials(credentials: LoginDto, db: Session = Depends(db)) -> bool:

    stmt = select(User).where(User.email == credentials.email).where(User.password_hash == credentials.password)
    user = db.scalars(stmt).one_or_none()

    if (user):
        return True
    else:
        return False
    
def create_access_token(user_id: int, role: str):
    payload = {
        "sub" : str(user_id),
        "role" : role,
        "exp" : datetime.now(timezone.utc) + timedelta(minutes=30)
    }

    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

def decode_access_token(token: str):
    return jwt.decode(token, settings.jwt_secret_key, algorithms=settings.jwt_algorithm)