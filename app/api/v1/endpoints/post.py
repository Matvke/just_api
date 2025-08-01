from fastapi import APIRouter, Query, Path, status, HTTPException
from app.schemas import PostResponse, PostScheme, OkResponse
from app.dependencies.service_dependencies import PostServiceDep
from app.dependencies.auth_dependencies import GetCurrUserDep
from uuid import UUID
from typing import Annotated


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get(path="", response_model=list[PostResponse], summary="Get a list of posts")
async def get_posts(
    service: PostServiceDep,
    current_user: GetCurrUserDep,
    skip: Annotated[int, Query()] = 0,
    limit: Annotated[int, Query()] = 10
    ) -> PostResponse:

    posts = await service.get_all_posts(skip, limit)
    return [PostResponse.model_validate(p) for p in posts]


@router.get(path="/{id}", response_model=PostResponse, summary="Get a single post by ID")
async def get_post(
    service: PostServiceDep,
    current_user: GetCurrUserDep,
    id: Annotated[UUID, Path()]
    ) -> PostResponse:

    post = await service.get_one_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} not found")
    return PostResponse.model_validate(post)


@router.get(path="/my/", tags=['Users'], summary="Get current user's posts")
async def get_my_posts(
    service: PostServiceDep,
    current_user: GetCurrUserDep,
    skip: Annotated[int, Query()] = 0,
    limit: Annotated[int, Query()] = 10
    ) -> list[PostResponse]:

    posts = await service.get_user_posts(user_id=current_user.id, skip=skip, limit=limit)
    return [PostResponse.model_validate(p) for p in posts]


@router.get(path="", summary="Get posts from selected user")
async def get_user_posts(
    service: PostServiceDep,
    current_user: GetCurrUserDep,
    user_id: Annotated[UUID, Query()],
    skip: Annotated[int, Query()] = 0,
    limit: Annotated[int, Query()] = 10
    ) -> list[PostResponse]:

    posts = await service.get_user_posts(user_id=user_id, skip=skip, limit=limit)
    return [PostResponse.model_validate(p) for p in posts]


@router.post(path="", response_model=PostResponse, status_code=status.HTTP_201_CREATED, summary="Create a new post")
async def create_post(
    service: PostServiceDep,
    current_user: GetCurrUserDep,
    post_data: PostScheme
    ) -> PostResponse:

    post = await service.create_post(post_data, current_user.id)
    return PostResponse.model_validate(post)


@router.put(path="/{id}/", response_model=PostResponse, summary="Update post information")
async def update_post(
    service: PostServiceDep,
    current_user: GetCurrUserDep,
    post_data: PostScheme,
    id: Annotated[UUID, Path()]
    ) -> PostResponse:
    post = await service.update_post(post_id=id, user_id=current_user.id, post=post_data)
    return PostResponse.model_validate(post)


@router.delete(path="/{id}", response_model=OkResponse, summary="Soft delete post")
async def delete_post(
    service: PostServiceDep,
    current_user: GetCurrUserDep,
    id: Annotated[UUID, Path()]
):
    await service.delete_post(post_id=id, user_id=current_user.id)
    return OkResponse(ok=True)


@router.patch(path="/{id}/restore", response_model=OkResponse, summary="Restore post")
async def restore_post(
    service: PostServiceDep,
    current_user: GetCurrUserDep,
    id: Annotated[UUID, Path()]
):
    await service.restore_post(post_id=id, user_id=current_user.id)
    return OkResponse(ok=True)