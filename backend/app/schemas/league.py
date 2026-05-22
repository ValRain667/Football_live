from pydantic import BaseModel
from typing import Optional, List


class LeagueOut(BaseModel):
    id: int
    name: str
    country: Optional[str] = None
    logo: Optional[str] = None
    season: Optional[str] = None
    standings: Optional[List[dict]] = []
    top_scorers: Optional[List[dict]] = []
    top_assists: Optional[List[dict]] = []

    class Config:
        from_attributes = True
