from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from config import settings

import jwt
from datetime import datetime, timedelta, timezone
    
def create_access_token(user_id: int, role: str):
    payload = {
        "sub" : str(user_id),
        "role" : role,
        "exp" : datetime.now(timezone.utc) + timedelta(minutes=30)
    }

    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

security = HTTPBearer()

def verify_user_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])

        user_id = payload.get("sub")
        user_role = payload.get("role")

        if user_id is None:
            raise HTTPException(401, "Invalid token")
        
        return {"user_id": int(user_id), "role": user_role}
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(403, "Token has expired")
    
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid token")
    
def verify_user_is_agent(user: dict = Depends(verify_user_token)):
    if user["role"] == "agent":
        return user
    
    raise HTTPException(403, "Not an agent")

def verify_user_is_client(user: dict = Depends(verify_user_token)):
    if user["role"] == "client":
        return user
    
    raise HTTPException(403, "Not a client")