from uuid import UUID

from sqlalchemy import delete, exists, select, update
from sqlalchemy.engine import Result
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.api_v1.teams.models import Team
from src.api_v1.teams.schemas import TeamCreate, TeamUpdate
from src.utils.exceptions import custom_exc


async def check_exists_team(
    db_session: AsyncSession, by_field: str, by_value: str
) -> bool:
    stmt = select(exists().where(getattr(Team, by_field) == by_value))
    team_exists = await db_session.scalar(stmt)
    return team_exists


async def create_team(db_session: AsyncSession, team_data: TeamCreate) -> Team:
    team = Team(**team_data)
    db_session.add(team)
    await db_session.commit()
    await db_session.refresh(team)
    return team


async def get_teams(db_session: AsyncSession, projects: bool) -> list[Team]:  # noqa
    stmt = select(Team)
    options = []

    if projects:
        options.append(selectinload(Team.projects))

    if options:
        stmt = stmt.options(*options).order_by(Team.created_at)
    else:
        stmt = stmt.order_by(Team.created_at)
    result: Result = await db_session.execute(stmt)
    teams: list[Team] = result.scalars().all()
    if teams is None:
        raise custom_exc.not_found(entity_name=Team.__name__)
    return list(teams)


async def get_team(  # noqa
    db_session: AsyncSession, team_id: UUID, projects: bool
) -> Team:
    stmt = select(Team)
    options = []

    if projects:
        options.append(selectinload(Team.projects))

    if options:
        stmt = stmt.options(*options).where(Team.id == team_id)
    else:
        stmt = stmt.where(Team.id == team_id)

    try:
        team: Team = await db_session.scalar(stmt)
    except NoResultFound:
        raise custom_exc.not_found(entity_name=Team.__name__)
    return team


async def update_team(
    db_session: AsyncSession, team_id: UUID, update_data: TeamUpdate
) -> Team:
    stmt = (
        update(Team)
        .returning(Team)
        .where(Team.id == team_id)
        .values(**update_data.model_dump())
    )

    result: Result = await db_session.execute(stmt)
    upd_team: Team = result.scalar()
    await db_session.commit()
    return upd_team


async def delete_team(db_session: AsyncSession, team_id: UUID) -> UUID:
    stmt = delete(Team).returning(Team.id).where(Team.id == team_id)
    result: Result = await db_session.execute(stmt)
    team_id: UUID | None = result.scalar()
    if team_id is None:
        raise custom_exc.not_found(entity_name=Team.__name__)
    await db_session.commit()
    return team_id
