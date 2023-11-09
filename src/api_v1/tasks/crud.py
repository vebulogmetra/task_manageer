from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.associates.models import UserTask
from src.api_v1.base.utils import is_valid_uuid
from src.api_v1.tasks.models import Task, TaskComment
from src.api_v1.tasks.schemas import (
    AddUserToTask,
    TaskCommentCreate,
    TaskCreate,
    TaskUpdate,
)
from src.utils.exceptions import custom_exc


async def create_task(db_session: AsyncSession, task_data: TaskCreate) -> Task:
    task = Task(**task_data)
    db_session.add(task)
    await db_session.commit()
    await db_session.refresh(task)
    return task


async def add_user_to_task(db_session: AsyncSession, data: AddUserToTask):
    user_task = UserTask(**data.model_dump())
    db_session.add(user_task)
    await db_session.commit()


async def add_comment_to_task(db_session: AsyncSession, comment_data: TaskCommentCreate):
    comment = TaskComment(**comment_data.model_dump())
    db_session.add(comment)
    await db_session.commit()


async def get_tasks(db_session: AsyncSession, limit: int, offset: int) -> list[Task]:
    stmt = select(Task).limit(limit).offset(offset).order_by(Task.created_at)

    result: Result = await db_session.execute(stmt)
    tasks: list[Task] = result.scalars().unique()
    if tasks is None:
        raise custom_exc.not_found(entity_name=Task.__name__)
    return list(tasks)


async def get_tasks_by_owner(db_session: AsyncSession, owner_id: UUID) -> list[Task]:
    stmt = select(Task).where(Task.creator_id == owner_id).order_by(Task.created_at)
    result: Result = await db_session.execute(stmt)
    tasks: list[Task] = result.scalars().unique()
    if tasks is None:
        raise custom_exc.not_found(entity_name=f"{Task.__name__}s")
    return list(tasks)


async def get_task(db_session: AsyncSession, task_id: UUID) -> Task:
    is_uuid: bool = is_valid_uuid(value=task_id)
    if is_uuid is False:
        raise custom_exc.invalid_input(detail="task id must by valid type UUID4")
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
        .values(**update_data.model_dump(exclude_none=True))
    )
    result: Result = await db_session.execute(stmt)
    upd_task = result.scalar()
    await db_session.commit()
    await db_session.refresh(upd_task)
    return upd_task


async def delete_task(db_session: AsyncSession, task_id: UUID) -> UUID:
    stmt = delete(Task).returning(Task.id).where(Task.id == task_id)
    task_id: UUID | None = await db_session.scalar(stmt)
    if task_id is None:
        raise custom_exc.not_found(entity_name=Task.__name__)
    await db_session.commit()
    return task_id
