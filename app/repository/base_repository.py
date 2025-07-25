from abc import ABC, abstractmethod
from app.model.models import BaseModel
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Generic, TypeVar
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
            .where(self.model.id == id))
        
        if not result:
            return None
        return result.scalar_one_or_none()


    async def get_all(self, skip: int = 0, limit: int = 100) -> list[T]:
        result = await self.session.execute(
            select(self.model)
            .offset(skip)
            .limit(limit))
        
        return result.scalars().all()
    

    async def get_many_by_filters(self, skip: int = 0, limit: int = 100, **filters) -> list[T]:
        result = await self.session.execute(
            select(self.model)
            .filter_by(**filters)
            .offset(skip)
            .limit(limit))
        
        return result.scalars().all()


    async def get_one_by_filters(self, **filters) -> T | None:
        """Возвращает первое совпадение."""
        result = await self.session.execute(
            select(self.model)
            .filter_by(**filters))

        return result.scalars().first()
    

    async def update(self, id: UUID, data: dict) -> T | None:
        await self.session.execute(
            update(self.model)
            .where(self.model.id == id)
            .values(**data))
        
        return await self.get_by_id(id)
    

    async def delete(self, id: UUID) -> None:
        await self.session.execute(
            delete(self.model).where(self.model.id == id))
