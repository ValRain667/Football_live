from fastapi import APIRouter, Depends
from typing import List, Optional
from app.schemas.team import TeamOut
from app.services.football_data import get_teams, get_team_by_id
from app.api.deps import get_optional_user

router = APIRouter()


@router.get("/", response_model=List[TeamOut])
async def list_teams(search: Optional[str] = None, user=Depends(get_optional_user)):
    return await get_teams(search=search)


@router.get("/{team_id}", response_model=TeamOut)
async def team_detail(team_id: int, user=Depends(get_optional_user)):
    return await get_team_by_id(team_id)
