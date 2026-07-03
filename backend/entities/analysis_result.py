from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

from pydantic import BaseModel, ConfigDict

from typing import TYPE_CHECKING
if TYPE_CHECKING: # Allows type-checking but avoids circular dependencies
    from entities import Message

class AnalysisResult(Base):
    __tablename__ = "analysis_result"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    message_id: Mapped[int] = mapped_column(ForeignKey("message.id"), index=True, nullable=False)
    time: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)
    intent: Mapped[str] = mapped_column(default="neutral", nullable=False)
    recommendations: Mapped[str] = mapped_column(default="Waiting messages", nullable=False)

    message: Mapped[Message] = relationship(back_populates="analysis")

class analysis_result_ai_response(BaseModel):
    intent: str
    recommendations: str

    model_config = ConfigDict(from_attributes=True)