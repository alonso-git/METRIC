from pydantic import BaseModel

class SigninDto(BaseModel):
    name: str
    email: str
    password: str

class LoginDto(BaseModel):
    email: str
    password: str