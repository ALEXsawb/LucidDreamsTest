from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

from app.models.post import Post
from app.schemas.post import PostSchema, PostCreateSchema
from app.services.dependencies import get_db_session
from app.services.auth.jwt import require_user_id
from app.services.post import create_post, delete_post
from app.services.user import get_user_by_id

post_router = APIRouter(prefix='/posts')


@post_router.post('/', status_code=status.HTTP_201_CREATED, response_model=PostSchema)
async def create_post_endpoint(request: Request, post_data: PostCreateSchema,
                               session: AsyncSession = Depends(get_db_session),
                               user_id: int = Depends(require_user_id)):
    user = await get_user_by_id(user_id=user_id, session=session)
    content_length = request.headers.get('content-length')
    if content_length is None or int(content_length) > 1_048_576:
        raise HTTPException(status_code=413, detail="Payload too large")
    return await create_post(user=user, text=post_data.text, session=session)


@post_router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post_endpoint(post_id: int, session: AsyncSession = Depends(get_db_session),
                               user_id: int = Depends(require_user_id)):
    await delete_post(user_id=user_id, post_id=post_id, session=session)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
