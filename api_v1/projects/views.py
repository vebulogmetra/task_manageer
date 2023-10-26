from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.projects import crud
from api_v1.projects.schemas import ProjectCreate, ProjectGet
from src.core.utils.database import db_helper

router = APIRouter()


@router.post("/create", response_model=ProjectGet)
async def create_project_handler(
    project_data: ProjectCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_project(db_session=session, project_data=project_data)


@router.get("/projects", response_model=list[ProjectGet])
async def get_projects_handler(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_projects(db_session=session)


@router.get("/project/{project_id}/", response_model=ProjectGet)
async def get_project_by_id_handler(
    project_id: str,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    project = crud.get_project(db_session=session, project_id=project_id)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found!"
        )


@router.put("/update/{project_id}/")
async def update_project_handler(
    updated_data: dict,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    pass


@router.delete("/delete/{project_id}/")
async def delete_project_handler(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    pass
