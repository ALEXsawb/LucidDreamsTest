from pydantic import BaseSettings


class Settings(BaseSettings):
    JWT_PUBLIC_KEY: str
    JWT_PRIVATE_KEY: str
    REFRESH_TOKEN_EXPIRES_IN: int
    ACCESS_TOKEN_EXPIRES_IN: int
    JWT_ALGORITHM: str

    SECRET_KEY: str

    MYSQL_DATABASE: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_ROOT_PASSWORD: str
    DATABASE_URL: str

    class Config:
        env_file = '../.env'


settings = Settings()
