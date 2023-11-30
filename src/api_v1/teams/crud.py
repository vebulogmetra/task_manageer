from uuid import UUID

from sqlalchemy import delete, exists, func, select, update
from sqlalchemy.engine import Result
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.associates.models import UserTeam
from src.api_v1.base.utils import is_valid_uuid
from src.api_v1.teams.models import Team
from src.api_v1.teams.schemas import AddUserToTeam, TeamCreate, TeamGet, TeamUpdate
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


async def add_user_to_team(db_session: AsyncSession, data: AddUserToTeam):
    user_team = UserTeam(**data.model_dump())
    db_session.add(user_team)
    await db_session.commit()


async def get_total_teams(db_session: AsyncSession) -> int:
    total_teams: int = await db_session.scalar(select(func.count(Team.id)))
    return total_teams


async def get_teams(db_session: AsyncSession, limit: int, offset: int) -> list[TeamGet]:
    stmt = select(Team).limit(limit).offset(offset).order_by(Team.created_at)

    result: Result = await db_session.execute(stmt)
    teams: list[Team] = result.scalars().unique()
    if teams is None:
        raise custom_exc.not_found(entity_name=Team.__name__)
    teams_dto: list[TeamGet] = [
        TeamGet.model_validate(t, from_attributes=True) for t in teams
    ]
    return teams_dto


async def get_team(db_session: AsyncSession, team_id: UUID) -> Team:
    is_uuid: bool = is_valid_uuid(value=team_id)
    if is_uuid is False:
        raise custom_exc.invalid_input(detail="team id must by valid type UUID4")
    stmt = select(Team).where(Team.id == team_id)
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
        .values(**update_data.model_dump(exclude_none=True))
    )

    result: Result = await db_session.execute(stmt)
    upd_team = result.scalar()
    await db_session.commit()
    await db_session.refresh(upd_team)
    return upd_team


async def delete_team(db_session: AsyncSession, team_id: UUID) -> UUID:
    stmt = delete(Team).returning(Team.id).where(Team.id == team_id)
    result: Result = await db_session.execute(stmt)
    team_id: UUID | None = result.scalar()
    if team_id is None:
        raise custom_exc.not_found(entity_name=Team.__name__)
    await db_session.commit()
    return team_id
