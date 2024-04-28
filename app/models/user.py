from pydantic import validate_email
from pydantic_core import PydanticCustomError
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase, validates

from app.db import Base
from app.models.base_fields import IdField


class User(IdField, Base):
    __tablename__ = 'User'
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(String(100), nullable=False)

    @validates('email')
    def validate_email(self, key, email):
        try:
            email = validate_email(email)[1]
        except PydanticCustomError as e:
            raise ValueError(f"Invalid email: {email}")
        return email

    @validates('password')
    def validate_password(self, key, password):
        if not isinstance(password, str):
            raise ValueError(f"The '{key}' field must be a string")

        columns = self.__table__.c
        max_length_password_field = columns.password.type.length
        if len(password) > max_length_password_field:
            raise ValueError(f"The '{key}' field must be less than {max_length_password_field} characters")
        return password

