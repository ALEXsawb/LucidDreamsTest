from fastapi import HTTPException
from cachetools import TTLCache
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.models.post import Post
from app.models.user import User


posts_cache = TTLCache(maxsize=1000, ttl=300)


def get_cache_key(user_id: int):
    return f"user_posts_{user_id}"


async def create_post(user: User, text: str, session: AsyncSession) -> Post:
    new_post = Post(text=text, user=user)
    session.add(new_post)
    await session.commit()
    await session.refresh(new_post)
    return new_post


async def delete_post(user_id: int, post_id: int, session: AsyncSession) -> None:
    result = await session.execute(delete(Post).where(Post.id == post_id, Post.user_id == user_id))
    await session.commit()
    if not result.rowcount:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Post by specified id does not exist or has another owner.')


async def get_user_posts(user_id: int, session: AsyncSession):
    cache_key = get_cache_key(user_id)
    if cache_key in posts_cache:
        if posts_cache[cache_key]:
            return posts_cache[cache_key]

    result = await session.execute(select(Post).where(Post.user_id == user_id))
    posts = result.scalars().all()
    if not posts:
        raise HTTPException(status_code=404, detail="No posts found for this user")

    posts_cache[cache_key] = [{'id': post.id, 'text': post.text} for post in posts]
    return posts
