from fastapi import APIRouter, Response, status, Depends, HTTPException

from app.services.auth.cookies import set_access_token_in_cookies, set_logged_in_cookies
from app.services.auth.jwt import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import UserCreateSchema, UserLoginSchema, CreatedUserSchema
from app.services.auth.tokens import get_access_token
from app.services.dependencies import get_db_session
from app.services.settings import settings
from app.services.user import create_user, get_user_by_credentials

auth_router = APIRouter()


@auth_router.post('/singup', status_code=status.HTTP_201_CREATED, response_model=CreatedUserSchema)
async def create_user_endpoint(user_data: UserCreateSchema, session: AsyncSession = Depends(get_db_session)):
    return await create_user(user_data=user_data, session=session)


@auth_router.post('/login', status_code=status.HTTP_200_OK)
async def login(user_data: UserLoginSchema, response: Response, Authorize: AuthJWT = Depends(),
                session: AsyncSession = Depends(get_db_session)):
    user = await get_user_by_credentials(email=user_data.email, password=user_data.password, session=session)
    access_token = get_access_token(settings.ACCESS_TOKEN_EXPIRES_IN, authorize=Authorize, user_id=str(user.id))
    set_access_token_in_cookies(response, access_token, settings.ACCESS_TOKEN_EXPIRES_IN)
    set_logged_in_cookies(response, settings.ACCESS_TOKEN_EXPIRES_IN)
    return {'access_token': access_token}
