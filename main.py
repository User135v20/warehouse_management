from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from domain.models import Product
from domain.services import WarehouseService
from infrastructure.orm import Base
from infrastructure.repositories import SqlAlchemyProductRepository, SqlAlchemyOrderRepository
from infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from infrastructure.database import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionFactory=sessionmaker(bind=engine)
Base.metadata.create_all(engine)

def main():
    session = SessionFactory()
    product_repo = SqlAlchemyProductRepository(session)
    order_repo = SqlAlchemyOrderRepository(session)

    uow = SqlAlchemyUnitOfWork(session)

    warehouse_service = WarehouseService(product_repo, order_repo)
    with uow:
        new_product = warehouse_service.create_product(name="test1", quantity=1, price=100)
        uow.commit()
        list_product = warehouse_service.list_product()
        print(list_product)

        warehouse_service.get_product(1)

        print(f"create product: {new_product}")
        # todo add some actions


        new_product2 = warehouse_service.create_product(name="test123", quantity=1, price=101)
        uow.commit()
        print(warehouse_service.list_product())
        #new_product2 = warehouse_service.create_product(name="test123", quantity=1, price=100)
        uow.commit()
        list_product = warehouse_service.list_product()
        print(list_product)
        warehouse_service.create_order(products=list([warehouse_service.get_product(1), warehouse_service.get_product(2)]))
        #warehouse_service.create_order(products=list([warehouse_service.get_product(1), Product(id=10, name="test",quantity=1,price=100)]))
        print(warehouse_service.list_orders())
        print(warehouse_service.get_order(111))


if __name__ == "__main__":
    main()
