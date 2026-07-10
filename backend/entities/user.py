from typing import TypedDict
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from entities.chat import chat_response
from database import Base

from pydantic import BaseModel, ConfigDict, Field

from typing import TYPE_CHECKING
if TYPE_CHECKING: # Allows type-checking but avoids circular dependencies
    from entities import Chat, Message

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(index=True)
    email: Mapped[str] = mapped_column(unique=True,index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(default="client", nullable=False)

    last_active: Mapped[datetime | None] = mapped_column(default=None, nullable=True)

    client_chats: Mapped[list[Chat]] = relationship(foreign_keys="[Chat.client_id]", back_populates="client") #type: ignore
    agent_chats: Mapped[list[Chat]] = relationship(foreign_keys="[Chat.agent_id]", back_populates="agent") #type: ignore

    messages: Mapped[Message] = relationship(back_populates="sender") #type: ignore
class user_response(BaseModel):
    id: int
    name: str
    email: str
    role: str

    client_chats: list[chat_response] = Field(default=[])
    agent_chats: list[chat_response] = Field(default=[])


    model_config = ConfigDict(from_attributes=True)

class user_login_response(BaseModel):
    access_token: str
    token_type: str
    user: user_response