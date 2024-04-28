from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.models.user import User
from app.schemas.user import UserCreateSchema
from app.services.auth.password import hash_password, verify_password
from app.services.exceptions import UserDoesNotExist


async def get_user_by_email(session: AsyncSession, email: str) -> User:
    result = await session.execute(select(User).where(User.email == email))
    user = result.scalars().first()
    if not user:
        raise UserDoesNotExist('User by specified email does not exist.')
    return user


async def create_user(user_data: UserCreateSchema, session: AsyncSession) -> User:
    hashed_password = hash_password(user_data.password)
    user = User(email=user_data.email.lower(), password=hashed_password)
    try:
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
    except IntegrityError:
        raise HTTPException(status_code=400, detail="User with specified email already exists.")


async def get_user_by_credentials(email: str, password: str, session: AsyncSession) -> User:
    try:
        user = await get_user_by_email(email=email, session=session)
        if not verify_password(plain_password=password, hashed_password=user.password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Specified invalid password.')
        return user
    except UserDoesNotExist as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


async def get_user_by_id(user_id: int, session: AsyncSession) -> User:
    result = await session.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=404, detail="User with specified id does not exist.")
    return user
