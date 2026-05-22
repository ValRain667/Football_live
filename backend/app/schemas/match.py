from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class MatchEvent(BaseModel):
    time: str
    type: str
    player: Optional[str] = None
    team: str


class MatchTeam(BaseModel):
    id: int
    name: str
    logo: Optional[str] = None
    score: Optional[int] = None


class MatchOut(BaseModel):
    id: int
    home_team: MatchTeam
    away_team: MatchTeam
    league: str
    league_logo: Optional[str] = None
    status: str
    minute: Optional[int] = None
    date: datetime
    events: List[MatchEvent] = []
    possession: Optional[dict] = None
    statistics: Optional[dict] = None

    class Config:
        from_attributes = True
