from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from src.api_v1.projects.models import Project
from src.api_v1.projects.schemas import ProjectCreate, ProjectUpdate
from src.api_v1.users.models import User
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
    project = await db_session.scalar(
        select(Project)
        .where(Project.id == project_id)
        .options(
            selectinload(Project.users),
        ),
    )
    user = await db_session.scalar(select(User).where(User.id == user_id))
    project.users.append(user)
    await db_session.commit()


async def get_projects(  # noqa
    db_session: AsyncSession, users: bool, tasks: bool
) -> list[Project]:
    stmt = select(Project)

    options = []

    if users:
        options.append(selectinload(Project.users))
    if tasks:
        options.append(selectinload(Project.tasks))

    if options:
        stmt = stmt.options(*options).order_by(Project.created_at)
    else:
        stmt = stmt.order_by(Project.created_at)

    result: Result = await db_session.execute(stmt)
    projects: list[Project] = result.scalars().all()
    if projects is None:
        raise custom_exc.not_found(entity_name=Project.__name__)
    return list(projects)


async def get_project(db_session: AsyncSession, project_id: UUID) -> Project | None:
    project: Project = await db_session.get(
        Project, project_id, options=(joinedload(Project.users),)
    )
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
