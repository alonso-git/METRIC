from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

from pydantic import BaseModel, ConfigDict

from typing import TYPE_CHECKING
if TYPE_CHECKING: # Allows type-checking but avoids circular dependencies
    from entities import User, Chat, AnalysisResult

class Message(Base):
    __tablename__ = "message"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    time: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)
    sender_id: Mapped[int] = mapped_column(ForeignKey("user.id"), index=True, nullable=False)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chat.id"), index=True, nullable=False)
    raw: Mapped[str] = mapped_column(nullable=False)

    sender: Mapped[User] = relationship(back_populates="messages")
    chat: Mapped[Chat] = relationship(back_populates="messages")

    analysis: Mapped[AnalysisResult] = relationship(back_populates="message")
class message_response(BaseModel):
    id:int
    time: datetime
    sender_id: int
    chat_id: int

    raw:str

    model_config = ConfigDict(from_attributes=True) 

class message_post(BaseModel):
    chat_id: int | None = None
    raw: str