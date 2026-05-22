from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base


class MatchCache(Base):
    __tablename__ = "matches_cache"

    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, unique=True, index=True, nullable=False)
    data = Column(Text, nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
