from pydantic import BaseModel, EmailStr, Field


class SignUpRequest(BaseModel):
    username: str = Field(min_length=2, max_length=40)
    email: EmailStr
    password: str = Field(min_length=8, max_length=40)
