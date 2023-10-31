from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.tasks.schemas import TaskCreate, TaskUpdate
from src.core.models.task import Task
from src.core.utils.exceptions import custom_exc


async def create_task(db_session: AsyncSession, task_data: TaskCreate) -> Task:
    task = Task(**task_data.model_dump())
    db_session.add(task)
    await db_session.commit()
    await db_session.refresh(task)  # Если на стороне БД генертся данные
    return task


async def get_tasks(db_session: AsyncSession) -> list[Task]:
    stmt = select(Task).order_by(Task.created_at)
    result: Result = await db_session.execute(stmt)
    tasks: list[Task] = result.scalars().all()
    if tasks is None:
        raise custom_exc.not_found(entity_name=Task.__name__)
    return list(tasks)


async def get_task(db_session: AsyncSession, task_id: UUID) -> Task:
    task: Task = await db_session.get(Task, task_id)
    if task is None:
        raise custom_exc.not_found(entity_name=Task.__name__)
    return task


async def update_task(
    db_session: AsyncSession, task_id: UUID, update_data: TaskUpdate
) -> Task:
    stmt = (
        update(Task)
        .returning(Task)
        .where(Task.id == task_id)
        .values(**update_data.model_dump())
    )
    result: Result = await db_session.execute(stmt)
    upd_task: Task = result.scalar()
    db_session.commit()
    return upd_task


async def delete_task(db_session: AsyncSession, task_id: UUID) -> UUID:
    stmt = delete(Task).returning(Task.id).where(Task.id == task_id)
    task_id: UUID | None = await db_session.scalar(stmt)
    if task_id is None:
        raise custom_exc.not_found(entity_name=Task.__name__)
    return task_id
