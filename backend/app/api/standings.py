from fastapi import APIRouter, Depends
from typing import List
from app.api.deps import get_optional_user
from app.services.football_data import get_standings

router = APIRouter()


@router.get("/{league_id}")
async def league_standings(league_id: int, season: str = "2024", user=Depends(get_optional_user)):
    return await get_standings(league_id, season)
