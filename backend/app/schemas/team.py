from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class TeamOut(BaseModel):
    id: int
    name: str
    logo: Optional[str] = None
    country: Optional[str] = None
    founded: Optional[int] = None
    stadium: Optional[str] = None
    coach: Optional[str] = None
    squad: Optional[List[dict]] = []
    recent_matches: Optional[List[dict]] = []
    stats: Optional[dict] = None

    class Config:
        from_attributes = True
