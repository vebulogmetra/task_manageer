import asyncio
import random
import secrets
from datetime import datetime, timedelta

import names

from quick_tests.creators import AddToEntity, Creator
from quick_tests.getters import GetEntity, GetEntityWithRelations
from src.api_v1.projects.models import Project
from src.api_v1.tasks.models import Task, TaskComment
from src.api_v1.teams.models import Team
from src.api_v1.users.models import User
from src.core.config import settings
from src.utils.database import db_manager


async def create_users(creator: Creator, users_data: list[dict]) -> list[User]:
    created_users = []
    for ud in users_data:
        user = await creator.create_user(
            username=ud.get("username"), email=ud.get("email"), password="123"
        )
        created_users.append(user)
    return created_users


async def create_profiles(creator: Creator, users: list[User]):
    for u in users:
        if u.username == "none":
            continue
        await creator.create_user_profile(
            user_id=u.id, first_name=u.username, last_name=names.get_last_name()
        )


async def create_projects(creator: Creator, users: list[User]) -> list[Project]:
    created_projects = []
    for u in users:
        project = await creator.create_project(
            name=secrets.token_hex(8),
            description=secrets.token_hex(16),
            creator_id=u.id,
        )
        created_projects.append(project)
    return created_projects


async def create_tasks(creator: Creator, projects: list[Project]) -> list[Task]:
    created_tasks = []
    for p in projects:
        task = await creator.create_task(
            creator_id=p.creator_id,
            project_id=p.id,
            title=secrets.token_hex(8),
            description=f"Add {secrets.token_urlsafe(32)}",
            status="created",  # created, in_work, complete
            priority="high",  # low, medium, high
            due_date=datetime.now().replace(microsecond=0)
            + timedelta(days=secrets.randbelow(20)),
        )
        created_tasks.append(task)
    return created_tasks


async def create_task_comments(
    creator: Creator, users: list[User], tasks: list[TaskComment]
):
    user_ids = [u.id for u in users]
    comments = []
    for idx, t in enumerate(tasks):
        comment1 = await creator.create_task_comment(
            user_id=user_ids[idx], task_id=t.id, content=secrets.token_hex(16)
        )
        comment2 = await creator.create_task_comment(
            user_id=user_ids[idx], task_id=t.id, content=secrets.token_hex(16)
        )
        comments.append(comment1)
        comments.append(comment2)
    return comments


async def create_teams(creator: Creator, users: list[User], count: int = 3) -> list[Team]:
    user_ids = [u.id for u in users]
    created_teams = []
    for i in range(count):
        team = await creator.create_team(
            creator_id=user_ids[i], title=secrets.token_hex(8)
        )
        created_teams.append(team)
    return created_teams


async def add_users_to_project_(
    executor: AddToEntity, users: list[User], projects: list[Project]
):
    for idx, p in enumerate(projects):
        await executor.add_users_to_project(project_id=p.id, users=[users[idx]])


async def add_users_to_task_(executor: AddToEntity, users: list[User], tasks: list[Task]):
    for idx, t in enumerate(tasks):
        await executor.add_users_to_task(task_id=t.id, users=[users[idx]])


async def add_users_to_team_(executor: AddToEntity, users: list[User], teams: list[Team]):
    for idx, te in enumerate(teams):
        await executor.add_users_to_team(team_id=te.id, users=[users[idx]])


def _generate_user_data(count: int = 10) -> list[dict]:
    users_data = []
    for _ in range(count - 1):
        uname = f"{names.get_first_name()}_{random.randint(10,20)}"
        ud = {"username": uname, "email": f"{uname}@gmail.com"}
        users_data.append(ud)
    return users_data


async def create_all():
    db_manager.init(connection_url=settings.db_alchemy_url, echo=settings.debug_database)
    async with db_manager.scoped_session_dependency() as session:
        creator: Creator = Creator(session)
        users_data = _generate_user_data(count=10)
        users_data.append({"username": "none", "email": "none@gmail.com"})
        users: list[User] = await create_users(creator=creator, users_data=users_data)
        await create_profiles(creator=creator, users=users)
        projects: list[Project] = await create_projects(creator=creator, users=users)
        tasks: list[Task] = await create_tasks(creator=creator, projects=projects)
        task_comments: list[TaskComment] = await create_task_comments(
            creator=creator, users=users, tasks=tasks
        )
        teams: list[Team] = await create_teams(creator=creator, users=users, count=5)

        add_executor: AddToEntity = AddToEntity(session)

        await add_users_to_project_(executor=add_executor, users=users, projects=projects)
        await add_users_to_task_(executor=add_executor, users=users, tasks=tasks)
        await add_users_to_team_(executor=add_executor, users=users, teams=teams)
        print("*" * 30)
        print("*" * 30)
        print(users)
        print("*" * 30)
        print(projects)
        print("*" * 30)
        print(tasks)
        print("*" * 30)
        print(task_comments)
        print("*" * 30)
        print(teams)
        print("*" * 30)
        print("*" * 30)


async def get_all():
    db_manager.init(connection_url=settings.db_alchemy_url, echo=settings.debug_database)
    async with db_manager.scoped_session_dependency() as session:
        getter_with: GetEntityWithRelations = GetEntityWithRelations(session)

        await getter_with.get_users_with_profiles()
        users: list[User] = await getter_with.get_users_with_all()
        projects: list[Project] = await getter_with.get_projects_with_all()
        tasks: list[Task] = await getter_with.get_tasks_with_all()
        teams: list[Team] = await getter_with.get_teams_with_all()

        user_ids = [u.id for u in users]
        project_ids = [p.id for p in projects]
        task_ids = [t.id for t in tasks]
        team_ids = [te.id for te in teams]

        # getter: GetEntity = GetEntity(session)
        # await getter.get_user_by_id(user_id=random.choice(user_ids))
        # await getter.get_project_by_id(project_id=random.choice(project_ids))
        # await getter.get_task_by_id(task_id=random.choice(task_ids))
        # await getter.get_team_by_id(team_id=random.choice(team_ids))
        # await getter.get_task_comment_by_task_id(task_id=random.choice(task_ids))
        # await getter.get_user_profile_by_user_id(user_id=random.choice(user_ids))


if __name__ == "__main__":
    # asyncio.run(create_all())
    asyncio.run(get_all())
