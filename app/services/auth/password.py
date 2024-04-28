from passlib.context import CryptContext

from app.services.settings import settings

pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    deprecated="auto",
    pbkdf2_sha256__default_rounds=29000,
    pbkdf2_sha256__salt_size=16,
)


def hash_password(password: str):
    return pwd_context.hash(password + settings.SECRET_KEY)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password + settings.SECRET_KEY, hashed_password)
