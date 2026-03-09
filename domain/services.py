from typing import List

from .exceptions import *
from .models import Product, Order
from .repositories import ProductRepository, OrderRepository


class WarehouseService:
    def __init__(self, product_repo: ProductRepository, order_repo: OrderRepository):
        self.product_repo = product_repo
        self.order_repo = order_repo

    def create_product(self, name: str, quantity: int, price: float) -> Product:
        all_products = self.product_repo.list()
        existing_products = [product for product in all_products if name == product.name]
        if existing_products:
            raise ProductAlreadyExistsException(product_name=name)
        product = Product(id=None, name=name, quantity=quantity, price=price)
        self.product_repo.add(product)
        return product

    def get_product(self, product_id: int):
        try:
            return self.product_repo.get(product_id)
        except Exception as err:
            raise NotFoundProductException(product_id=product_id) from err

    def list_product(self):
        return self.product_repo.list()

    def create_order(self, products: List[Product]) -> Order:
        if not products:
            raise OrderNotCreatedException(
                message=f"An order can't be created. Product list is empty")

        list_unique_ids = set()
        list_ununique_products = []

        for product in products:
            if product.id in list_unique_ids:
                list_ununique_products.append(product)
            else:
                list_unique_ids.add(product.id)

        if list_ununique_products:
            raise OrderNotCreatedException(
                message=f"An order can't be created. These products {list_ununique_products} "
                        f"have been added more than once.")

        all_products = self.list_product()
        unavailable_products = [product for product in products if product not in all_products]
        if unavailable_products:
            raise OrderNotCreatedException(products=unavailable_products)
        order = Order(id=None, products=products)
        self.order_repo.add(order)
        return order

    def get_order(self, order_id: int):
        try:
            return self.order_repo.get(order_id)
        except Exception as err:
            raise NotFoundOrderException(order_id=order_id) from err

    def list_orders(self):
        return self.order_repo.list()
