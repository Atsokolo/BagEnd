# src/project/infrastructure/postgres/repository/DiscountList_repo.py
from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from src.project.infrastructure.postgres.models import Supplier
from src.project.schemas.supplierSchema import SupplierSchema


class SupplierRepository:
    _collection: Type[Supplier] = Supplier

    async def check_connection(
            self,
            session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_supplier(
            self,
            session: AsyncSession
    ) -> list[SupplierSchema]:

        query = "SELECT * FROM supplier;"
        result = await session.execute(text(query))

        return [
            SupplierSchema.model_validate(dict(DiscountList))
            for DiscountList in result.mappings().all()
        ]

    async def get_supplier_by_id(
            self,
            session: AsyncSession,
            id_DiscountList: int
    ) -> SupplierSchema | None:

        query = text("SELECT * FROM supplier WHERE id = :id;")
        result = await session.execute(query, {"id": id_DiscountList})

        DiscountList_row = result.mappings().first()

        if DiscountList_row:
            return SupplierSchema.model_validate(dict(DiscountList_row))

        return None

    async def insert_supplier(
            self,
            session: AsyncSession,
            id: int,
            name: str,
            address: str,
            phone_number: str,
            email: str
    ) -> SupplierSchema | None:

        query = text("""
            INSERT INTO supplier (name, address, phone_number, email) 
            VALUES (:name, :address, :phone_number, :email)
            RETURNING id, name, address, phone_number, email;
        """)

        result = await session.execute(query, {
            "name": name,
            "address": address,
            "phone_number": phone_number,
            "email": email
        })

        DiscountList_row = result.mappings().first()

        if DiscountList_row:
            return SupplierSchema.model_validate(dict(DiscountList_row))

        return None

    async def update_supplier_by_id(
            self,
            session: AsyncSession,
            id: int,
            name: str,
            address: str,
            phone_number: str,
            email: str
    ) -> SupplierSchema | None:

        query = text("""
            UPDATE supplier 
            SET name = :name, address = :address, phone_number = :phone_number, email = :email 
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
            return SupplierSchema.model_validate(dict(updated_row))

        return None

    async def delete_supplier_by_id(
            self,
            session: AsyncSession,
            id_DiscountList: int
    ) -> bool:

        query = text("DELETE FROM supplier WHERE id = :id RETURNING id;")
        result = await session.execute(query, {"id": id_DiscountList})

        deleted_row = result.fetchone()

        return deleted_row is not None
