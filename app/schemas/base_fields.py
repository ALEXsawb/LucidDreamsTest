from pydantic import Field, EmailStr, BaseModel


class IdField:
    id: int = Field(..., gt=0)


class TextField:
    text: str = Field(..., max_length=500)


class ModeOnORM:
    class Config:
        orm_mode = True
