from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select

from project.schemas.customers import CustomersSchema, CustomersCreateSchema

from project.infrastructure.postgres.models import Customers

from project.core.config import settings


class CustomerRepository:
    _collection: Type[Customers] = Customers

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_customers(
        self,
        session: AsyncSession,
    ) -> list[CustomersSchema]:
        query = f"select * from {settings.POSTGRES_SCHEMA}.customers;"

        customers = await session.execute(text(query))

        return [CustomersSchema.model_validate(obj=user) for user in customers.mappings().all()]

    async def add_customer(self, customer: CustomersCreateSchema, session: AsyncSession) -> CustomersSchema:
        # Создание нового клиента
        new_cust = self._collection(**customer.dict())
        session.add(new_cust)
        await session.commit()
        await session.refresh(new_cust)
        return CustomersSchema.model_validate(new_cust)

    async def delete_customer(self, customer_id: int, session: AsyncSession) -> bool:
        query = select(self._collection).where(self._collection.id == customer_id)
        result = await session.execute(query)
        client = result.scalar_one_or_none()
        await session.delete(client)
        await session.commit()
        return True

    async def get_customer_by_id(self, customer_id: int, session: AsyncSession) -> CustomersSchema:
        query = select(self._collection).where(self._collection.id == customer_id)
        result = await session.execute(query)

        customer = result.scalar_one_or_none()

        return CustomersSchema.model_validate(customer)

