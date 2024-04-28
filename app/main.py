from fastapi import FastAPI, HTTPException
from starlette import status
from starlette.middleware.cors import CORSMiddleware

from app.controllers import auth_router, user_router, post_router
from app.db import create_tables

app = FastAPI()
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(post_router)


origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(ValueError)
async def view_exception_NOT_FOUND(request, exc):
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@app.on_event('startup')
async def connect_and_config_db():
    await create_tables()

