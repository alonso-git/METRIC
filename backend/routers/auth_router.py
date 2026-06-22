from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from passlib.context import CryptContext
from passlib.exc import UnknownHashError

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
def login(credentials: LoginDto, db: Session = Depends(db)):
    stmt = select(User).where(User.email == credentials.email)

    user = db.scalars(stmt).one_or_none()

    print(f"DEBUG: Password length: {len(credentials.password)}")
    print(f"DEBUG: Hash length: {len(user.password_hash)}")

    if user:
        
        try:
            if pwd_context.verify(credentials.password, user.password_hash):
                return {
                    "access_token": AuthService.create_access_token(user.id, user.role),
                    "token_type": "bearer"
                }
        except UnknownHashError:
            pass
            
    
    raise HTTPException(401, "Incorect email or password")

            