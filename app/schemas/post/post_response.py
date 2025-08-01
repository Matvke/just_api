from pydantic import BaseModel, ConfigDict, UUID4


class PostResponse(BaseModel):
    id: UUID4
    title: str
    content: str
    user_id: UUID4

    model_config = ConfigDict(from_attributes=True)


class OkResponse(BaseModel):
    ok: bool