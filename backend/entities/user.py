from sqlalchemy.orm import Mapped, mapped_column, relationship
from entities.chat import chat_response
from database import Base
from pydantic import BaseModel, ConfigDict, Field

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(index=True)
    email: Mapped[str] = mapped_column(unique=True,index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(default="client", nullable=False)

    client_chats: Mapped[list["Chat"]] = relationship(foreign_keys="[Chat.client_id]", back_populates="client") #type: ignore
    agent_chats: Mapped[list["Chat"]] = relationship(foreign_keys="[Chat.agent_id]", back_populates="agent") #type: ignore

    messages: Mapped["Message"] = relationship(back_populates="sender") #type: ignore
class user_response(BaseModel):
    id:int
    name: str
    email: str
    role: str

    chats: list[chat_response] = Field(default=[])

    model_config = ConfigDict(from_attributes=True)