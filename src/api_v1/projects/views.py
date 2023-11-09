from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.auth.schemas import TokenUserData
from src.api_v1.auth.service import get_current_user
from src.api_v1.base.schemas import StatusMsg
from src.api_v1.projects import crud
from src.api_v1.projects.schemas import (
    AddUserToProject,
    ProjectCreate,
    ProjectGet,
    ProjectUpdate,
)
from src.utils.database import get_db

router = APIRouter()


@router.post("/create", response_model=ProjectGet)
async def create_project_handler(
    project_data: ProjectCreate,
    session: AsyncSession = Depends(get_db),
    current_user: TokenUserData = Depends(get_current_user),
):
    if project_data.creator_id is None:
        project_data.creator_id = current_user.id
    return await crud.create_project(db_session=session, project_data=project_data)


@router.post("/add_user", response_model=StatusMsg)
async def add_user_to_project_handler(
    data: AddUserToProject,
    session: AsyncSession = Depends(get_db),
    current_user: TokenUserData = Depends(get_current_user),
):
    if data.user_id is None:
        data.user_id = current_user.id
    await crud.add_user_to_project(db_session=session, data=data)
    return StatusMsg(
        status="ok",
        detail=f"User {data.user_id} added in project {data.project_id}",
    )


@router.get("/projects", response_model=list[ProjectGet])
async def get_projects_handler(
    limit: Optional[int] = 100,
    offset: Optional[int] = 0,
    session: AsyncSession = Depends(get_db),
):
    return await crud.get_projects(db_session=session, limit=limit, offset=offset)


@router.get("/projects_by_owner", response_model=list[ProjectGet])
async def get_projects_by_owner_handler(
    owner_id: Optional[str] = None,
    session: AsyncSession = Depends(get_db),
    current_user: TokenUserData = Depends(get_current_user),
):
    if owner_id is None:
        owner_id = current_user.id
    return await crud.get_projects_by_owner(db_session=session, owner_id=owner_id)


@router.get("/project", response_model=ProjectGet)
async def get_project_by_id_handler(
    project_id: str,
    session: AsyncSession = Depends(get_db),
    current_user: TokenUserData = Depends(get_current_user),
):
    project = await crud.get_project(db_session=session, project_id=project_id)
    return project


@router.put(
    "/update",
    response_model=ProjectGet,
)
async def update_project_handler(
    project_id: str,
    update_data: ProjectUpdate,
    session: AsyncSession = Depends(get_db),
):
    upd_project = await crud.update_project(
        db_session=session, project_id=project_id, update_data=update_data
    )
    return upd_project


@router.delete("/delete", response_model=StatusMsg)
async def delete_project_handler(
    project_id: str,
    session: AsyncSession = Depends(get_db),
):
    deleted_project_id: UUID = await crud.delete_project(
        db_session=session, project_id=project_id
    )
    return StatusMsg(detail=f"Deleted project_id: {deleted_project_id}")
