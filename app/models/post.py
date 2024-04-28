from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from app.db import Base
from app.models.base_fields import IdField
from app.services.validators import validate_not_null_field_of_table, validate_max_length_string_field_of_table


class Post(IdField, Base):
    __tablename__ = 'Post'
    text: Mapped[str] = mapped_column(String(500), nullable=False)
    user: Mapped['User'] = relationship()
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('User.id'))

    @validates('text')
    def validate_text(self, key, text):
        validate_not_null_field_of_table(table=self, field_name=key, field_value=text)
        validate_max_length_string_field_of_table(table=self, field_name=key, field_value=text)
        return text
