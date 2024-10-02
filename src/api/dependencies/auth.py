import logging
from datetime import datetime, UTC
from uuid import UUID

from fastapi import HTTPException, Security, status
from fastapi_jwt import JwtAuthorizationCredentials
from jose import JWTError
from pydantic import ValidationError
from tortoise.exceptions import DoesNotExist

from constants.auth import USER_ONLINE_DURATION_MINUTES
from models import User
from schemas.token import TokenPayload
from security.token import access_security


async def get_current_user(
    credentials: JwtAuthorizationCredentials = Security(access_security),
) -> User:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )
    try:
        token_user = TokenPayload(**credentials.subject)
    except (JWTError, ValidationError) as ex:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        ) from ex
    return await get_user(user_uid=token_user.uid)


async def get_user(user_uid: UUID) -> User:
    try:
        user = await User.get(uid=user_uid)
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    try:
        await update_last_visited_at(user=user)
    except Exception as ex:
        logging.exception(ex)  # noqa: TRY401
    return user


async def update_last_visited_at(user: User) -> None:
    current_time = datetime.now(UTC)
    if not user.last_visited_at:
        user.last_visited_at = current_time
        await user.save()
        return

    seconds_from_last_online = current_time - user.last_visited_at
    minutes_from_last_online = seconds_from_last_online.total_seconds() / 60

    if minutes_from_last_online > USER_ONLINE_DURATION_MINUTES:
        user.last_visited_at = current_time
        await user.save()
