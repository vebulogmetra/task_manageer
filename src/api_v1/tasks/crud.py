from uuid import UUID

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.tasks.schemas import TaskCreate
from src.core.models.task import Task, TaskComment


async def get_tasks(db_session: AsyncSession) -> list[Task]:
    stmt = select(Task).order_by(Task.created_at)
    result: Result = await db_session.execute(stmt)
    tasks: list[Task] = result.scalars().all()
    return list(tasks)


async def get_task(db_session: AsyncSession, task_id: UUID) -> Task | None:
    return await db_session.get(Task, task_id)


async def create_task(db_session: AsyncSession, task_data: TaskCreate) -> Task:
    task = Task(**task_data.model_dump())
    db_session.add(task)
    await db_session.commit()
    await db_session.refresh(task)  # Если на стороне БД генертся данные
    return task
