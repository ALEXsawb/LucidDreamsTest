import base64
from typing import List

from fastapi import Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from starlette import status

from app.services.settings import settings


class Settings(BaseModel):
    authjwt_algorithm: str = settings.JWT_ALGORITHM
    authjwt_decode_algorithms: List[str] = [settings.JWT_ALGORITHM]
    authjwt_token_location: set = {'cookies', 'headers'}
    authjwt_access_cookie_key: str = 'access_token'
    authjwt_refresh_cookie_key: str = 'refresh_token'
    authjwt_cookie_csrf_protect: bool = False
    authjwt_public_key: str = base64.b64decode(settings.JWT_PUBLIC_KEY).decode('utf-8')
    authjwt_private_key: str = base64.b64decode(settings.JWT_PRIVATE_KEY).decode('utf-8')


@AuthJWT.load_config
def get_config():
    return Settings()


async def require_user_id(Authorize: AuthJWT = Depends()) -> int:
    try:
        Authorize.jwt_required()
        user_id = Authorize.get_jwt_subject()

        if not user_id:
            raise Exception('Your token subject don\'t correct. You need a re-login')

        return int(user_id)
    except Exception as e:
        error = e.__class__.__name__
        if error == 'MissingTokenError':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='You are not logged in')
        if error.__str__() == 'User no longer exist':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='User no longer exist')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is invalid or has expired')
