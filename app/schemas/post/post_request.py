from pydantic import BaseModel, Field


class PostScheme(BaseModel):
    title: str = Field(max_length=255)
    content: str = Field(max_length=1023)
