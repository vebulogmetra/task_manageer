from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.api_v1.tasks.models import Task, TaskComment
from src.api_v1.tasks.schemas import TaskCommentCreate, TaskCreate, TaskUpdate
from src.api_v1.users.models import User
from src.utils.exceptions import custom_exc


async def create_task(db_session: AsyncSession, task_data: TaskCreate) -> Task:
    task = Task(**task_data.model_dump())
    db_session.add(task)
    await db_session.commit()
    await db_session.refresh(task)  # Если на стороне БД генертся данные
    return task


async def add_user_to_task(db_session: AsyncSession, task_id: UUID, user_id: UUID):
    task = await db_session.scalar(
        select(Task)
        .where(Task.id == task_id)
        .options(
            selectinload(Task.users),
        ),
    )
    user = await db_session.scalar(select(User).where(User.id == user_id))
    task.users.append(user)
    await db_session.commit()


async def add_comment_to_task(db_session: AsyncSession, comment_data: TaskCommentCreate):
    comment = TaskComment(**comment_data.model_dump())
    db_session.add(comment)
    await db_session.commit()

    task = await db_session.scalar(
        select(Task)
        .where(Task.id == comment_data.task_id)
        .options(
            selectinload(Task.comments),
        ),
    )
    task.comments.append(comment)
    await db_session.commit()


async def get_tasks(  # noqa
    db_session: AsyncSession, users: bool, comments: bool
) -> list[Task]:
    stmt = select(Task)

    options = []

    if users:
        options.append(selectinload(Task.users))
    if comments:
        options.append(selectinload(Task.comments))

    if options:
        stmt = stmt.options(*options).order_by(Task.created_at)
    else:
        stmt = stmt.order_by(Task.created_at)

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
