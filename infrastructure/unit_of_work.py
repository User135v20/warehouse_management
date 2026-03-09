from domain.unit_of_work import UnitOfWork
from infrastructure.repositories import SqlAlchemyOrderRepository, SqlAlchemyProductRepository


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session_factory):
        self.session_factory = session_factory
        self.session = None
        self.product_repo = None
        self.order_repo = None

    def __enter__(self):
        self.session = self.session_factory()
        self.product_repo = SqlAlchemyProductRepository(self.session)
        self.order_repo = SqlAlchemyOrderRepository(self.session)
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        if exception_type:
            self.rollback()
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
