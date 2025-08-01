from typing import Any
from app.repository import PostRepository
from app.schemas.post.post_request import PostScheme
from uuid import UUID
from app.model.models import Post


class PostService():
    def __init__(self, repository: PostRepository):
        self.repository = repository

    async def get_user_posts(self, user_id: UUID, skip: int = 0, limit: int = 10) -> list[Post]:
        return await self.repository.get_many_by_filters(skip=skip, limit=limit, user_id=user_id)


    async def get_all_posts(self, skip: int = 0, limit: int = 10) -> list[Post]:
        return await self.repository.get_many_by_filters(skip=skip, limit=limit)
    

    async def get_one_post(self, post_id: UUID) -> Post:
        return await self.repository.get_by_id(post_id)


    async def create_post(self, post: PostScheme, user_id: UUID) -> Post:
        post_data = post.model_dump()
        post_data['user_id'] = user_id
        try:
            post = await self.repository.create(post_data) 
            await self.repository.session.commit()
        except Exception as e:
            await self.repository.session.rollback()
            raise e
        return post
        

    async def update_post(self, post_id: UUID, user_id: UUID, post: PostScheme) -> Post:
        post_data = post.model_dump()
        post_data["user_id"] = user_id 
        try:
            post = await self.repository.update_one_by_id(id=post_id, data=post_data)
            await self.repository.session.commit()
        except Exception as e:
            await self.repository.session.rollback()
            raise e
        return post
    

    async def update_attr(self, id: UUID, column: str, value: Any) -> Post:
        try:
            post = await self.repository.update_attr(id, column, value)
            await self.repository.session.commit()
        except Exception as e:
            await self.repository.session.rollback()
            raise e
        return post
    
    
    async def _update_post_disable_attr(self, post_id: UUID, user_id: UUID, value: bool) -> None:
        try:
            await self.repository.update_disabled_attr(id=post_id, value=value, user_id=user_id)
            await self.repository.session.commit()
        except Exception as e:
            await self.repository.session.rollback()
            raise e 
        
    
    async def delete_post(self, post_id: UUID, user_id: UUID) -> None:
        await self._update_post_disable_attr(post_id, user_id, True)

    
    async def restore_post(self, post_id: UUID, user_id: UUID) -> None:
        await self._update_post_disable_attr(post_id, user_id, False)