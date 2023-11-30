from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.auth.schemas import TokenUserData
from src.api_v1.auth.service import get_current_user
from src.api_v1.base.schemas import StatusMsg
from src.api_v1.teams import crud
from src.api_v1.teams.schemas import AddUserToTeam, TeamCreate, TeamGet, TeamUpdate
from src.utils.database import get_db

router = APIRouter()


@router.post("/create", response_model=TeamGet)
async def create_team_handler(
    team_data: TeamCreate,
    session: AsyncSession = Depends(get_db),
    current_user: TokenUserData = Depends(get_current_user),
):
    team_data: dict = team_data.model_dump()
    team_data.update({"creator_id": current_user.id})
    return await crud.create_team(db_session=session, team_data=team_data)


@router.post("/add_user", response_model=StatusMsg)
async def add_user_to_team_handler(
    data: AddUserToTeam,
    session: AsyncSession = Depends(get_db),
    current_user: TokenUserData = Depends(get_current_user),
):
    if data.user_id is None:
        data.user_id = current_user.id
    await crud.add_user_to_team(db_session=session, data=data)
    return StatusMsg(
        status="ok", detail=f"User {data.user_id} added in team {data.team_id}"
    )


@router.get("/total_count")
async def get_total_teams_count_handler(session: AsyncSession = Depends(get_db)):
    total_teams: int = await crud.get_total_teams(db_session=session)
    return total_teams


@router.get("/get_all", response_model=list[TeamGet])
async def get_teams_handler(
    limit: Optional[int] = 100,
    offset: Optional[int] = 0,
    session: AsyncSession = Depends(get_db),
):
    return await crud.get_teams(db_session=session, limit=limit, offset=offset)


@router.get("/team", response_model=TeamGet)
async def get_team_handler(
    team_id: str,
    session: AsyncSession = Depends(get_db),
    current_user: TokenUserData = Depends(get_current_user),
):
    team: TeamGet = await crud.get_team(db_session=session, team_id=team_id)
    return team


@router.put("/update", response_model=TeamGet)
async def update_team_handler(
    team_id: str,
    update_data: TeamUpdate,
    session: AsyncSession = Depends(get_db),
):
    upd_team: TeamGet = await crud.update_team(
        db_session=session, team_id=team_id, update_data=update_data
    )
    return upd_team


@router.delete("/delete", response_model=StatusMsg)
async def delete_team_handler(
    team_id: str,
    session: AsyncSession = Depends(get_db),
):
    deleted_team_id: UUID | None = await crud.delete_team(
        db_session=session, team_id=team_id
    )
    return StatusMsg(detail=f"Deleted team_id: {deleted_team_id}")
