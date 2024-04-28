from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.schemas.post import PostSchema
from app.services.dependencies import get_db_session
from app.services.auth.jwt import require_user_id
from app.services.post import get_user_posts

user_router = APIRouter(prefix='/user')


@user_router.get('/posts', response_model=List[PostSchema], status_code=status.HTTP_200_OK)
async def user_posts(session: AsyncSession = Depends(get_db_session), user_id: int = Depends(require_user_id)):
    posts = await get_user_posts(session=session, user_id=user_id)
    print(posts)
    return posts
