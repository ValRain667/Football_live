from fastapi import APIRouter, Depends, Query
from typing import Optional, List
from app.schemas.match import MatchOut
from app.services.football_data import get_matches, get_live_matches, get_match_by_id
from app.api.deps import get_optional_user

router = APIRouter()


@router.get("/", response_model=List[MatchOut])
async def list_matches(
    date: Optional[str] = Query(None),
    league_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    user=Depends(get_optional_user),
):
    return await get_matches(date=date, league_id=league_id, status=status)


@router.get("/live", response_model=List[MatchOut])
async def live(user=Depends(get_optional_user)):
    return await get_live_matches()


@router.get("/{match_id}", response_model=MatchOut)
async def match_detail(match_id: int, user=Depends(get_optional_user)):
    return await get_match_by_id(match_id)
