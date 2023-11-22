from datetime import datetime

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError

from src.config import settings
from src.domain.authentication import TokenPayload
from src.domain.users import UserFlat, UsersRepository
from src.infrastructure.application import AuthenticationError
from src.infrastructure.database import transaction

__all__ = ("get_current_user",)

oauth2_oauth = OAuth2PasswordBearer(
    tokenUrl="/auth/openapi",
    scheme_name=settings.authentication.scheme,
)


async def get_current_user(token: str = Depends(oauth2_oauth)) -> UserFlat:
    try:
        payload = jwt.decode(
            token,
            settings.authentication.access_token.secret_key,
            algorithms=[settings.authentication.algorithm],
        )
        token_payload = TokenPayload(**payload)

        if datetime.fromtimestamp(token_payload.exp) < datetime.now():
            raise AuthenticationError
    except (JWTError, ValidationError) as err:
        raise AuthenticationError from err

    async with transaction():
        user = await UsersRepository().get(id_=token_payload.sub)

    # TODO: Check if the token is in the blacklist

    return user
