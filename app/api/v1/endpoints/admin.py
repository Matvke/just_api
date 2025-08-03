from fastapi import APIRouter, Path, Query
from app.core.enums import RoleEnum
from app.dependencies.auth_dependencies import GetCurrAdminDep
from app.dependencies.service_dependencies import UserServiceDep
from typing import Annotated
from uuid import UUID
from app.schemas import OkResponse


router = APIRouter(
    prefix='/admin',
    tags=['Admin']
)

@router.post('/role/{user_id}/', response_model=OkResponse)
async def set_role(
    service: UserServiceDep,
    current_admin: GetCurrAdminDep,
    user_id: Annotated[UUID, Path()],
    role: Annotated[RoleEnum, Query()]
):
    await service.set_role(id=user_id, role=role)
    return OkResponse(ok=True)


@router.delete('/{user_id}', response_model=OkResponse)
async def soft_delete_user(
    service: UserServiceDep,
    current_admin: GetCurrAdminDep,
    user_id: Annotated[UUID, Path()]
):
    await service.soft_delete_user(user_id)
    return OkResponse(ok=True)


@router.patch('/{user_id}', response_model=OkResponse)
async def restore_user(
    service: UserServiceDep,
    current_admin: GetCurrAdminDep,
    user_id: Annotated[UUID, Path()]
):
    await service.restore_user(user_id)
    return OkResponse(ok=True)