from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.base.schemas import StatusMsg
from src.api_v1.teams import crud
from src.api_v1.teams.schemas import TeamCreate, TeamGet, TeamUpdate
from src.utils.database import get_db

router = APIRouter()


@router.post("/create", response_model=TeamGet)
async def create_team_handler(
    team_data: TeamCreate,
    session: AsyncSession = Depends(get_db),
):
    return await crud.create_team(db_session=session, team_data=team_data)


@router.get("/teams", response_model=list[TeamGet])
async def get_teams_handler(
    projects: Optional[bool] = False,
    session: AsyncSession = Depends(get_db),
):
    teams = await crud.get_teams(db_session=session, projects=projects)
    return teams


@router.get("/team/{team_id}", response_model=TeamGet)
async def get_team_handler(
    by_value: Optional[str] = None,
    by_field: Optional[str] = None,
    session: AsyncSession = Depends(get_db),
):
    team: TeamGet = await crud.get_team(
        db_session=session, by_field=by_field, by_value=by_value
    )
    return team


@router.put("/update/{team_id}", response_model=TeamGet)
async def update_team_handler(
    team_id: str,
    update_data: TeamUpdate,
    session: AsyncSession = Depends(get_db),
):
    upd_team: TeamGet = await crud.update_team(
        db_session=session, team_id=team_id, update_data=update_data
    )
    return upd_team


@router.delete("/delete/{team_id}", response_model=StatusMsg)
async def delete_team_handler(
    team_id: str,
    session: AsyncSession = Depends(get_db),
):
    deleted_team_id: UUID | None = await crud.delete_team(
        db_session=session, team_id=team_id
    )
    return StatusMsg(detail=f"Deleted team_id: {deleted_team_id}")
