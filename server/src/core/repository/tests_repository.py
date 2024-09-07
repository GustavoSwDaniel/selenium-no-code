from typing import Dict
from infrastructure.database.entities.tests import Tests
from infrastructure.database.repositories.repository import SqlRepository
from sqlalchemy import select, update, func
from sqlalchemy.orm import selectinload, load_only


class TestsRepository(SqlRepository):
    model = Tests

    async def get_all_test_paginated(self, params: Dict):
        async with self.session_factory() as session:
            query = select(self.model).options(selectinload(self.model.image_tests)).limit(params.get('limit')).offset(params.get('offset'))

            total_query = select(func.count(self.model.id))
            total_result = await session.execute(total_query)
            total = total_result.scalar()

            results = await session.execute(query)

        return results.scalars().all(), total

    async def get_test_by_id(self, id):
        async with self.session_factory() as session:
            result = await session.execute(
                select(self.model).where(self.model.id == id).options(selectinload(self.model.image_tests)))
            result = result.scalars().first()

            return result
