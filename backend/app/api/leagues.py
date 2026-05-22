from fastapi import APIRouter, Depends
from typing import List
from app.schemas.league import LeagueOut
from app.services.football_data import get_leagues, get_league_by_id
from app.api.deps import get_optional_user

router = APIRouter()


@router.get("/", response_model=List[LeagueOut])
async def list_leagues(user=Depends(get_optional_user)):
    return await get_leagues()


@router.get("/{league_id}", response_model=LeagueOut)
async def league_detail(league_id: int, user=Depends(get_optional_user)):
    return await get_league_by_id(league_id)
