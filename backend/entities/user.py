from sqlalchemy.orm import Mapped, mapped_column
from database import Base

from pydantic import BaseModel, ConfigDict

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(index=True)
    email: Mapped[str] = mapped_column(unique=True,index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(default="client", nullable=False)

class User_response(BaseModel):
    id:int
    name: str
    email: str
    role: str

    model_config = ConfigDict(from_attributes=True)