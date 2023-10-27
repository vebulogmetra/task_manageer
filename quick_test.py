import asyncio
import random
from datetime import datetime, timedelta
from pprint import pprint
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from src.core.models.project import Project
from src.core.models.task import Task
from src.core.models.user import User
from src.core.models.user_profile import UserProfile
from src.core.utils.database import db_helper


async def create_user(session: AsyncSession, username: str) -> User:
    user: User = User(username=username)
    session.add(user)
    await session.commit()
    pprint(f"New User: {user}")
    return user


async def create_user_profile(
    session: AsyncSession, user_id: str, first_name: str, last_name: str
) -> UserProfile:
    user_profile: UserProfile = UserProfile(
        user_id=user_id, first_name=first_name, last_name=last_name
    )
    session.add(user_profile)
    await session.commit()
    pprint(f"New User Profile: {user_profile}")
    return user_profile


async def create_project(
    session: AsyncSession, user_id: str, name: str, description: str
) -> Project:
    project: Project = Project(user_id=user_id, name=name, description=description)
    session.add(project)
    await session.commit()
    pprint(f"New Project: {project}")
    return project


async def create_task(
    session: AsyncSession,
    user_id: str,
    project_id: str,
    title: str,
    description: str,
    status: str,
    priority: str,
    due_date: datetime,
) -> Task:
    task: Task = Task(
        user_id=user_id,
        project_id=project_id,
        title=title,
        description=description,
        status=status,
        priority=priority,
        due_date=due_date,
    )
    session.add(task)
    await session.commit()
    pprint(f"New Task: {task}")
    return task


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    user: User | None = await session.scalar(stmt)
    pprint(f"Get User by username {username}: {user}")
    return user


async def get_user_profile_by_user_id(
    session: AsyncSession, user_id: str
) -> UserProfile | None:
    stmt = select(UserProfile).where(UserProfile.user_id == user_id)
    result: Result = await session.execute(stmt)
    user_profile: UserProfile | None = result.scalar_one_or_none()
    pprint(f"Get User Profile by user_id {user_id}: {user_profile}")
    return user_profile


async def get_project_by_name(session: AsyncSession, name: str) -> Project | None:
    stmt = select(Project).where(Project.name == name)
    result: Result = await session.execute(stmt)
    project: Project = result.scalar_one_or_none()
    pprint(f"Get Project by name {name}: {project}")
    return project


async def get_task_by_title(session: AsyncSession, title: str) -> Project | None:
    stmt = select(Task).where(Task.title == title)
    result: Result = await session.execute(stmt)
    task: Task = result.scalar_one_or_none()
    print(f"Get Task by title {title}: {task}")
    return task


async def create_more_projects(
    session: AsyncSession,
    user_id: str,
) -> list[Project]:
    generated_data: list[tuple] = []
    for _ in range(3):
        name = f"Projec Name {uuid4().hex}"
        description = f"Description {uuid4().hex}"
        generated_data.append((name, description))
    projects = [
        Project(user_id=user_id, name=name, description=descr)
        for name, descr in generated_data
    ]
    session.add_all(projects)
    await session.commit()
    print(f"Created projects: {projects}")
    return projects


async def create_more_tasks(
    session: AsyncSession,
    user_id: str,
    project_id: str,
) -> list[Task]:
    due_dates: list[datetime] = []
    for _ in range(5):
        due_dates.append(
            datetime.now().replace(microsecond=0) + timedelta(days=random.randint(1, 7))
        )
    tasks = [
        Task(user_id=user_id, project_id=project_id, due_date=dd) for dd in due_dates
    ]
    session.add_all(tasks)
    await session.commit()
    print(f"Created tasks: {tasks}")
    return tasks


async def get_users_with_tasks(session: AsyncSession) -> list[User]:
    stmt = select(User).options(selectinload(User.tasks)).order_by(User.id)
    result: Result = await session.execute(stmt)
    users: list[User] = result.scalars()
    for user in users:
        print(f"User: {user}")
        for ut in user.tasks:
            print("- ", f"User task title: {ut.title}")
    return users


async def get_tasks_with_users(session: AsyncSession) -> list[Task]:
    stmt = select(Task).options(joinedload(Task.user)).order_by(Task.id)
    result: Result = await session.execute(stmt)
    tasks: list[Task] = result.scalars()
    for task in tasks:
        print(f"Task: {task}")
        print(f"Task User: {task.user}")
    return tasks


async def get_users_with_profiles(session: AsyncSession) -> list[User]:
    stmt = select(User).options(joinedload(User.profile)).order_by(User.id)
    # stmt = select(User).options(selectinload(User.profile)).order_by(User.id)
    users = await session.scalars(stmt)
    for user in users:
        print(f"User: {user}")
        print(
            f"User profile first name: {user.profile.first_name if user.profile else None}"
        )
    return users


async def get_users_with_profiles_and_with_tasks(session: AsyncSession) -> list[User]:
    stmt = (
        select(User)
        .options(joinedload(User.profile), selectinload(User.tasks))
        .order_by(User.id)
    )
    result: Result = await session.execute(stmt)
    users: list[User] = result.scalars()
    for user in users:
        print(f"User: {user}")
        print(
            f"User profile first_name: {user.profile.first_name if user.profile else None}"
        )
        for ut in user.tasks:
            print("- ", f"User task title: {ut.title}")
    return users


async def run_without_create():
    async with db_helper.session_factory() as session:
        await get_user_by_username(session=session, username="string")  # Not exists
        await get_user_by_username(session=session, username="ivan")
        await get_user_by_username(session=session, username="viktor")
        await get_user_by_username(session=session, username="john")
        await get_project_by_name(session=session, name="IvanProject")
        await get_task_by_title(session=session, title="Task for John")

        _: list[User] = await get_users_with_tasks(session=session)
        _: list[Task] = await get_tasks_with_users(session=session)
        _: list[User] = await get_users_with_profiles_and_with_tasks(session=session)
        _: list[User] = await get_users_with_profiles(session=session)


async def run_create():
    async with db_helper.session_factory() as session:
        user_ivan: User = await create_user(session=session, username="ivan")
        user_viktor: User = await create_user(session=session, username="viktor")
        user_john: User = await create_user(session=session, username="john")
        await create_user_profile(
            session=session, user_id=user_ivan.id, first_name="Ivan", last_name="Jobs"
        )
        await create_user_profile(
            session=session, user_id=user_john.id, first_name="John", last_name="Doe"
        )
        project: Project = await create_project(
            session=session,
            user_id=user_ivan.id,
            name="IvanProject",
            description="lalala some description string lalala",
        )
        _: Task = await create_task(
            session=session,
            user_id=user_john.id,
            project_id=project.id,
            title="Task for John",
            description="Add product model in db, and create API",
            status="created",  # created, in_work, complete
            priority="high",  # low, medium, high
            due_date=datetime.now() + timedelta(weeks=2),
        )

        _: list[Task] = await create_more_tasks(
            session,
            user_john.id,
            project.id,
        )

        projects_ivan: list[Project] = await create_more_projects(session, user_ivan.id)
        projects_viktor: list[Project] = await create_more_projects(
            session, user_viktor.id
        )
        for pi in projects_ivan:
            user_id = random.choice([user_ivan.id, user_viktor.id, user_john.id])
            _: list[Task] = await create_more_tasks(
                session,
                user_id,
                pi.id,
            )
        for pv in projects_viktor:
            user_id = random.choice([user_ivan.id, user_viktor.id, user_john.id])
            _: list[Task] = await create_more_tasks(
                session,
                user_id,
                pv.id,
            )


if __name__ == "__main__":
    # asyncio.run(run_create())
    asyncio.run(run_without_create())
