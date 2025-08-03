from abc import ABC, abstractmethod
from app.model.models import BaseModel
from sqlalchemy import and_, not_, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Generic, TypeVar
from uuid import UUID

T = TypeVar("T", bound=BaseModel)

class BaseRepository(ABC, Generic[T]):
    def __init__(self, session: AsyncSession):
        self.session = session

    @property
    @abstractmethod
    def model(self) -> type[T]:
        raise NotImplementedError

    async def create(self, data: dict) -> T:
        instance = self.model(**data)
        self.session.add(instance)
        await self.session.flush()
        await self.session.refresh(instance)
        return instance
    

    async def get_by_id(self, id: UUID) -> T | None:
        result = await self.session.execute(
            select(self.model)
            .where(
                and_(self.model.id == id,
                not_(self.model.disabled))))
        return result.scalar_one_or_none()

    
    async def get_many_by_filters(self, skip: int = 0, limit: int = 100, **filters) -> list[T]:
        result = await self.session.execute(
            select(self.model)
            .where(not_(self.model.disabled))
            .filter_by(**filters)
            .offset(skip)
            .limit(limit))
        
        return result.scalars().all()


    async def get_one_by_filters(self, include_disabled: bool = False, **filters) -> T | None:
        query = select(self.model).filter_by(**filters)
        if not include_disabled:
            query = query.where(not_(self.model.disabled))

        result = await self.session.execute(query)

        return result.scalar_one_or_none()
    

    async def update_one_by_id(self, id: UUID, data: dict) -> T | None:
        await self.session.execute(
            update(self.model)
            .where(
                and_(self.model.id == id,
                not_(self.model.disabled)))
            .values(**data))
        
        return await self.get_by_id(id)
    

    async def update_attr(self, id: UUID, column: str, value: Any) -> T:
        await self.session.execute(
            update(self.model)
            .where(
                and_(self.model.id == id,
                not_(self.model.disabled)))
            .values(**{column: value})
        )

        return await self.get_by_id(id)


    async def update_disabled_attr(self, value: bool, **filters) -> None:
        await self.session.execute(
            update(self.model)
            .filter_by(**filters)
            .values(disabled = value)
        )

    
    async def soft_delete(self, **filters) -> None:
        await self.update_disabled_attr(value=True, **filters)

    
    async def restore(self, **filters) -> None:
        await self.update_disabled_attr(value=False, **filters)


    async def hard_delete_one_by_id(self, id: UUID) -> None:
        await self.session.execute(
            delete(self.model).where(self.model.id == id))
