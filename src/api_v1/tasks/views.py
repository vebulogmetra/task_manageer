from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.base.schemas import StatusMsg
from src.api_v1.tasks import crud
from src.api_v1.tasks.schemas import (
    TaskCommentCreate,
    TaskCommentGet,
    TaskCreate,
    TaskGet,
    TaskUpdate,
)
from src.core.utils.database import db_helper

router = APIRouter()


@router.post("/create", response_model=TaskGet)
async def create_task_handler(
    task_data: TaskCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_task(db_session=session, task_data=task_data)


@router.get("/tasks", response_model=list[TaskGet])
async def get_tasks_handler(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_tasks(db_session=session)


@router.get("/task/{task_id}", response_model=TaskGet)
async def get_task_by_id_handler(
    task_id: str,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    task = crud.get_task(db_session=session, task_id=task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found!"
        )


@router.put("/update/{task_id}", response_model=TaskGet)
async def update_task_handler(
    task_id: str,
    update_data: TaskUpdate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    upd_task: TaskGet = await crud.update_task(
        db_session=session, task_id=task_id, update_data=update_data
    )
    return upd_task


@router.delete("/delete/{task_id}", response_model=StatusMsg)
async def delete_task_handler(
    task_id: str,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    deleted_task_id: UUID = await crud.delete_task(db_session=session, task_id=task_id)
    return StatusMsg(detail=f"Deleted task_id: {deleted_task_id}")
