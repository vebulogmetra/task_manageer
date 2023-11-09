from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.auth.schemas import TokenUserData
from src.api_v1.auth.service import get_current_user
from src.api_v1.base.schemas import StatusMsg
from src.api_v1.tasks import crud
from src.api_v1.tasks.schemas import (
    AddUserToTask,
    TaskCommentCreate,
    TaskCreate,
    TaskGet,
    TaskUpdate,
)
from src.utils.database import get_db

router = APIRouter()


@router.post("/create", response_model=TaskGet)
async def create_task_handler(
    task_data: TaskCreate,
    session: AsyncSession = Depends(get_db),
    current_user: TokenUserData = Depends(get_current_user),
):
    task_data: dict = task_data.model_dump()
    task_data.update({"creator_id": current_user.id})
    return await crud.create_task(db_session=session, task_data=task_data)


@router.post("/add_user", response_model=StatusMsg)
async def add_user_to_task_handler(
    data: AddUserToTask,
    session: AsyncSession = Depends(get_db),
    current_user: TokenUserData = Depends(get_current_user),
):
    if data.user_id is None:
        data.user_id = current_user.id
    await crud.add_user_to_task(db_session=session, data=data)
    return StatusMsg(
        status="ok", detail=f"User {data.user_id} added in task {data.task_id}"
    )


@router.post("/add_comment", response_model=StatusMsg)
async def add_comment_to_task_handler(
    comment_data: TaskCommentCreate,
    session: AsyncSession = Depends(get_db),
    current_user: TokenUserData = Depends(get_current_user),
):
    if comment_data.user_id is None:
        comment_data.user_id = current_user.id
    await crud.add_comment_to_task(db_session=session, comment_data=comment_data)
    return StatusMsg(
        status="ok",
        detail=f"Comment {comment_data.content} added in task {comment_data.task_id}",
    )


@router.get("/tasks", response_model=list[TaskGet])
async def get_tasks_handler(
    limit: Optional[int] = 100,
    offset: Optional[int] = 0,
    session: AsyncSession = Depends(get_db),
):
    return await crud.get_tasks(db_session=session, limit=limit, offset=offset)


@router.get("/tasks_by_owner", response_model=list[TaskGet])
async def get_tasks_by_owner_handler(
    owner_id: Optional[str] = None,
    session: AsyncSession = Depends(get_db),
    current_user: TokenUserData = Depends(get_current_user),
):
    if owner_id is None:
        owner_id = current_user.id
    return await crud.get_tasks_by_owner(db_session=session, owner_id=owner_id)


@router.get("/task", response_model=TaskGet)
async def get_task_by_id_handler(
    task_id: str,
    session: AsyncSession = Depends(get_db),
    current_user: TokenUserData = Depends(get_current_user),
):
    task = await crud.get_task(db_session=session, task_id=task_id)
    return task


@router.put("/update", response_model=TaskGet)
async def update_task_handler(
    task_id: str,
    update_data: TaskUpdate,
    session: AsyncSession = Depends(get_db),
):
    upd_task = await crud.update_task(
        db_session=session,
        task_id=task_id,
        update_data=update_data,
    )
    return upd_task


@router.delete("/delete", response_model=StatusMsg)
async def delete_task_handler(
    task_id: str,
    session: AsyncSession = Depends(get_db),
):
    deleted_task_id: UUID = await crud.delete_task(db_session=session, task_id=task_id)
    return StatusMsg(detail=f"Deleted task_id: {deleted_task_id}")
