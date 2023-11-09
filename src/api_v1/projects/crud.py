from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.api_v1.associates.models import UserProject
from src.api_v1.base.utils import is_valid_uuid
from src.api_v1.projects.models import Project
from src.api_v1.projects.schemas import AddUserToProject, ProjectCreate, ProjectUpdate
from src.utils.exceptions import custom_exc


async def create_project(
    db_session: AsyncSession, project_data: ProjectCreate
) -> Project:
    project = Project(**project_data.model_dump())
    db_session.add(project)
    await db_session.commit()
    await db_session.refresh(project)
    return project


async def add_user_to_project(db_session: AsyncSession, data: AddUserToProject):
    user_project = UserProject(**data.model_dump())
    db_session.add(user_project)
    await db_session.commit()


async def get_projects(
    db_session: AsyncSession, limit: int, offset: int
) -> list[Project]:
    stmt = (
        select(Project)
        .options(joinedload(Project.users))
        .limit(limit)
        .offset(offset)
        .order_by(Project.created_at)
    )
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
    projects: list[Project] = result.scalars().unique()
    if projects is None:
        raise custom_exc.not_found(entity_name=f"{Project.__name__}s")
    return list(projects)


async def get_project(db_session: AsyncSession, project_id: UUID) -> Project | None:
    is_uuid: bool = is_valid_uuid(value=project_id)
    if is_uuid is False:
        raise custom_exc.invalid_input(detail="project id must by valid type UUID4")
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
        .values(**update_data.model_dump(exclude_none=True))
    )
    result: Result = await db_session.execute(stmt)
    updated_project = result.scalar()
    await db_session.commit()
    await db_session.refresh(updated_project)
    return updated_project


async def delete_project(db_session: AsyncSession, project_id: UUID) -> UUID:
    stmt = delete(Project).returning(Project.id).where(Project.id == project_id)
    project_id: UUID | None = await db_session.scalar(stmt)
    if project_id is None:
        raise custom_exc.not_found(entity_name=Project.__name__)
    await db_session.commit()
    return project_id
