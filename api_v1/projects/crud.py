from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.projects.schemas import ProjectCreate
from src.core.models.project import Project


async def get_projects(db_session: AsyncSession) -> list[Project]:
    stmt = select(Project).order_by(Project.created_at)
    result: Result = await db_session.execute(stmt)
    projects: list[Project] = result.scalars().all()
    return list(projects)


async def get_project(db_session: AsyncSession, project_id: UUID) -> Project | None:
    return await db_session.get(Project, project_id)


async def create_project(
    db_session: AsyncSession, project_data: ProjectCreate
) -> Project:
    project = Project(**project_data.model_dump())
    db_session.add(project)
    await db_session.commit()
    await db_session.refresh(project)  # Если на стороне БД генертся данные
    return project
