from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.auth.schemas import TokensPair
from src.api_v1.users import crud as user_crud
from src.api_v1.users.models import User
from src.utils.auth import jwt_helper, pwd_helper
from src.utils.exceptions import custom_exc


async def authenticate(
    db_session: AsyncSession, auth_data: OAuth2PasswordRequestForm
) -> TokensPair:
    email: str = auth_data.username
    password: str = auth_data.password

    user_exists: bool = await user_crud.check_exists_user(
        db_session=db_session, by_field="email", by_value=email
    )
    if not user_exists:
        raise custom_exc.unauthorized(detail="Invalid email")

    user: User = await user_crud.get_user_by_email(db_session=db_session, email=email)
    if user is None:
        raise custom_exc.not_found(entity_name="User")

    pwd_helper.verify_password(
        plain_password=password, hashed_password=user.hashed_password
    )

    userdata_in_token = {
        "id": user.id,
        "email": user.email,
    }

    access_token: str = jwt_helper.create_token(data=userdata_in_token, type="access")
    refresh_token: str = jwt_helper.create_token(data=userdata_in_token, type="refresh")

    return TokensPair(access=access_token, refresh=refresh_token)
