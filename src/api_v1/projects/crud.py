from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.api_v1.associates.models import UserProject
from src.api_v1.projects.models import Project
from src.api_v1.projects.schemas import ProjectCreate, ProjectUpdate
from src.utils.exceptions import custom_exc


async def create_project(
    db_session: AsyncSession, project_data: ProjectCreate
) -> Project:
    project = Project(**project_data.model_dump())
    db_session.add(project)
    await db_session.commit()
    await db_session.refresh(project)  # Если на стороне БД генертся данные
    return project


async def add_user_to_project(db_session: AsyncSession, project_id: UUID, user_id: UUID):
    user_project = UserProject(user_id=user_id, project_id=project_id)
    db_session.add(user_project)
    await db_session.commit()


async def get_projects(db_session: AsyncSession, users: bool) -> list[Project]:
    stmt = select(Project).order_by(Project.created_at)
    options = []
    if users:
        options.append(joinedload(Project.users))
        stmt = stmt.options(*options)

    result: Result = await db_session.execute(stmt)
    projects: list[Project] = result.scalars().unique()
    if projects is None:
        raise custom_exc.not_found(entity_name=f"{Project.__name__}s")
    return list(projects)


async def get_projects_by_owner(
    db_session: AsyncSession, owner_id: UUID
) -> list[Project]:
    stmt = (
        select(Project).where(Project.creator_id == owner_id).order_by(Project.created_at)
    )
    result: Result = await db_session.execute(stmt)
    projects: list[Project] = result.scalars().all()
    if projects is None:
        raise custom_exc.not_found(entity_name=f"{Project.__name__}s")
    return list(projects)


async def get_project(
    db_session: AsyncSession, project_id: UUID, include_users: bool
) -> Project | None:
    stmt = (
        select(Project).options(joinedload(Project.users)).where(Project.id == project_id)
    )
    result: Result = await db_session.execute(stmt)
    project = result.scalar()
    if project is None:
        raise custom_exc.not_found(entity_name=Project.__name__)
    return project


async def update_project(
    db_session: AsyncSession, project_id: UUID, update_data: ProjectUpdate
) -> Project:
    stmt = (
        update(Project)
        .returning(Project)
        .where(Project.id == project_id)
        .values(**update_data.model_dump())
    )
    result: Result = await db_session.execute(stmt)
    upd_project: Project = result.scalar()
    db_session.commit()
    return upd_project


async def delete_project(db_session: AsyncSession, project_id: UUID) -> UUID:
    stmt = delete(Project).returning(Project.id).where(Project.id == project_id)
    project_id: UUID | None = await db_session.scalar(stmt)
    if project_id is None:
        raise custom_exc.not_found(entity_name=Project.__name__)
    return project_id
