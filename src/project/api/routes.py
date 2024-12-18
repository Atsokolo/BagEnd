from fastapi import APIRouter, HTTPException

from project.infrastructure.postgres.repository.customer_repo import CustomerRepository
from project.infrastructure.postgres.database import PostgresDatabase
from project.schemas.customers import CustomersSchema, CustomersCreateSchema


router = APIRouter()

@router.get("/all_customers", response_model=list[CustomersSchema])
async def get_allcustomers() -> list[CustomersSchema]:
    cust_repo = CustomerRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await cust_repo.check_connection(session=session)
        all_cutomers = await cust_repo.get_all_customers(session=session)

    return all_cutomers

@router.get("/customer/{customer_id}", response_model=CustomersSchema)
async def get_customer_by_id(customer_id: int) -> CustomersSchema:
    customer_repo = CustomerRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await customer_repo.check_connection(session=session)
        customer = await customer_repo.get_customer_by_id(customer_id=customer_id, session=session)

        if customer is None:
            raise HTTPException(status_code=404, detail="Customer  not found")

    return customer

@router.post("/add_customer", response_model=CustomersSchema)
async def add_customer(customer: CustomersCreateSchema) -> CustomersSchema:
    customer_repo = CustomerRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await customer_repo.check_connection(session=session)
        new_customer = await customer_repo.add_customer(customer=customer, session=session)

    return new_customer
