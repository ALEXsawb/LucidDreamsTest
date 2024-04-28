from app.services.auth.jwt import AuthJWT
from fastapi import Depends, HTTPException
from starlette import status

from app.db import AsyncSessionLocal


async def get_db_session():
    async with AsyncSessionLocal() as session:
        yield session

