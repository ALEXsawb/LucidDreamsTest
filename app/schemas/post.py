from pydantic import BaseModel, Field

from app.schemas.base_fields import IdField, TextField


class PostCreateSchema(BaseModel):
    text: str = Field(..., max_length=500)


class PostSchema(BaseModel):
    id: int = Field(gt=0)
    text: str = Field(max_length=500)

    class Config:
        orm_mode = True
