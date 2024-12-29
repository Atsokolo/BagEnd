# src/project/infrastructure/postgres/repository/DiscountList_repo.py
from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from src.project.infrastructure.postgres.models import Publisher
from src.project.schemas.publisherSchema import PublisherSchema


class PublisherRepository:
    _collection: Type[Publisher] = Publisher

    async def check_connection(
            self,
            session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_Publisher(
            self,
            session: AsyncSession
    ) -> list[PublisherSchema]:

        query = "SELECT * FROM publisher;"
        result = await session.execute(text(query))

        return [
            PublisherSchema.model_validate(dict(value))
            for value in result.mappings().all()
        ]

    async def get_Publisher_by_id(
            self,
            session: AsyncSession,
            id: int
    ) -> PublisherSchema | None:

        query = text("SELECT * FROM publisher WHERE id = :id")
        result = await session.execute(query, {"id": id})

        rows = result.mappings().first()

        if rows:
            return PublisherSchema.model_validate(dict(rows))

        return None

    async def insert_Publisher(
            self,
            session: AsyncSession,
            id: int,
            name: str,
            address: int,
            phone_number: float,
            email: str
    ) -> PublisherSchema | None:

        query = text("""
            INSERT INTO publisher (name, address, phone_number, email) 
            VALUES (:name, :address, :phone_number, :email)
            RETURNING id, name, address, phone_number, email
        """)

        result = await session.execute(query, {
            "id": id,
            "name": name,
            "address": address,
            "phone_number": phone_number,
            "email": email
        })

        DiscountList_row = result.mappings().first()

        if DiscountList_row:
            return PublisherSchema.model_validate(dict(DiscountList_row))

        return None

    async def update_Publisher_by_id(
            self,
            session: AsyncSession,
            id: int,
            name: str,
            address: int,
            phone_number: float,
            email: str
    ) -> PublisherSchema | None:

        query = text("""
            UPDATE publisher 
            SET name = :name, address = :address, phone_number = :phone_number, email = :semail 
            WHERE id = :id 
            RETURNING id, name, address, phone_number, email;
        """)

        result = await session.execute(query, {
            "id": id,
            "name": name,
            "address": address,
            "phone_number": phone_number,
            "email": email
        })

        updated_row = result.mappings().first()

        if updated_row:
            return PublisherSchema.model_validate(dict(updated_row))

        return None

    async def delete_Publisher_by_id(
            self,
            session: AsyncSession,
            id_DiscountList: int
    ) -> bool:

        query = text("DELETE FROM publisher WHERE id = :id RETURNING id;")
        result = await session.execute(query, {"id": id_DiscountList})

        deleted_row = result.fetchone()

        return deleted_row is not None
