from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from entities.message import message_response
from database import Base

from pydantic import BaseModel, ConfigDict

class Chat(Base):
    __tablename__ = "chat"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("user.id"), index=True, nullable=False)
    agent_id: Mapped[int | None] = mapped_column(ForeignKey("user.id"), default=None, index=True, nullable=True)
    time: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)
    status: Mapped[str] = mapped_column(default="open", nullable=False)
    unread_client: Mapped[bool] = mapped_column(default=True)
    unread_agent: Mapped[bool] = mapped_column(default=True)
    overall_intent: Mapped[str] = mapped_column(default="neutral", nullable=False)
    recommendations: Mapped[str] = mapped_column(default="Esperando mensajes...", nullable=False)

    client: Mapped["User"] = relationship(foreign_keys=[client_id], back_populates="client_chats") #type: ignore
    agent: Mapped["User"] = relationship(foreign_keys=[agent_id], back_populates="agent_chats") #type: ignore

    messages: Mapped[list["Message"]] = relationship(back_populates="chat") #type: ignore

class chat_response(BaseModel):
    id:int
    client_id: int
    agent_id: int
    time: datetime
    status: str
    overall_intent: str
    recommendations: str | None

    messages: list[message_response]

    model_config = ConfigDict(from_attributes=True)