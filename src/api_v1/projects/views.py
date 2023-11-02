from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.base.schemas import StatusMsg
from src.api_v1.projects import crud
from src.api_v1.projects.schemas import ProjectCreate, ProjectGet, ProjectUpdate
from src.utils.database import get_db

router = APIRouter()


@router.post("/create", response_model=ProjectGet)
async def create_project_handler(
    project_data: ProjectCreate,
    session: AsyncSession = Depends(get_db),
):
    return await crud.create_project(db_session=session, project_data=project_data)


@router.post("/add_user", response_model=StatusMsg)
async def add_user_to_project_handler(
    project_id: str, user_id: str, session: AsyncSession = Depends(get_db)
):
    await crud.add_user_to_project(
        db_session=session, project_id=project_id, user_id=user_id
    )
    return StatusMsg(status="ok", detail=f"User {user_id} added in project {project_id}")


@router.get("/projects", response_model=list[ProjectGet])
async def get_projects_handler(
    session: AsyncSession = Depends(get_db),
):
    return await crud.get_projects(db_session=session)


@router.get("/project/{project_id}", response_model=ProjectGet)
async def get_project_by_id_handler(
    project_id: str,
    session: AsyncSession = Depends(get_db),
):
    project = await crud.get_project(db_session=session, project_id=project_id)
    return project


@router.put("/update/{project_id}", response_model=ProjectGet)
async def update_project_handler(
    project_id: str,
    update_data: ProjectUpdate,
    session: AsyncSession = Depends(get_db),
):
    upd_project: ProjectGet = await crud.update_project(
        db_session=session, project_id=project_id, update_data=update_data
    )
    return upd_project


@router.delete("/delete/{project_id}", response_model=StatusMsg)
async def delete_project_handler(
    project_id: str,
    session: AsyncSession = Depends(get_db),
):
    deleted_project_id: UUID = await crud.delete_project(
        db_session=session, project_id=project_id
    )
    return StatusMsg(detail=f"Deleted project_id: {deleted_project_id}")
