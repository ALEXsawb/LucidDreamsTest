from pydantic import EmailStr, BaseModel, Field

from app.schemas.base_fields import IdField


class UserBaseSchema(BaseModel):
    email: EmailStr
    password: str = Field(..., max_length=100)

    class Config:
        orm_mode = True


class UserCreateSchema(UserBaseSchema):
    pass


class UserLoginSchema(UserBaseSchema):
    pass


class UserSchema(IdField, UserCreateSchema):
    pass


class CreatedUserSchema(BaseModel):
    id: int = Field(..., gt=0)
    email: EmailStr

    class Config:
        orm_mode = True
