from datetime import timedelta

from fastapi_jwt_auth import AuthJWT


def get_access_token(expire_in_minute, authorize: AuthJWT, user_id: str) -> str:
    return authorize.create_access_token(subject=user_id, expires_time=timedelta(minutes=expire_in_minute))
