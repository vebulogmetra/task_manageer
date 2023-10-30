from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.base.schemas import StatusMsg
from src.api_v1.projects import crud
from src.api_v1.projects.schemas import ProjectCreate, ProjectGet, ProjectUpdate
from src.core.utils.database import get_db

router = APIRouter()


@router.post("/create", response_model=ProjectGet)
async def create_project_handler(
    project_data: ProjectCreate,
    session: AsyncSession = Depends(get_db),
):
    return await crud.create_project(db_session=session, project_data=project_data)


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
    project = crud.get_project(db_session=session, project_id=project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found!")


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
    deleted_project_id: UUID = await crud.delete_project(db_session=session, project_id=project_id)
    return StatusMsg(detail=f"Deleted project_id: {deleted_project_id}")
