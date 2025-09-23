from sqlalchemy import Boolean, Column, Integer, String, DateTime
from .database import Base
from sqlalchemy.sql import func

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title=Column(String, index=True)
    is_completed=Column(Boolean, default=False, index=True)
    created_at=Column(DateTime, server_default=func.now())
    updated_at=Column(DateTime, server_default=func.now(),onupdate=func.now()) # updated_atにも初期値を与えないとレスポンスがnullになり、バリデーションエラー