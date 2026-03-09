from unittest import mock
from unittest.mock import MagicMock

import pytest
from sqlalchemy.exc import NoResultFound

from domain.exceptions import *
from domain.models import *
from domain.repositories import OrderRepository, ProductRepository
from domain.services import WarehouseService
from infrastructure.repositories import SqlAlchemyProductRepository

product_list = [
    Product(id=1, name="test_1", quantity=1, price=1),
    Product(id=2, name="test_2", quantity=1, price=2),
    Product(id=3, name="test_3", quantity=1, price=2),
]


@pytest.mark.parametrize(
    "should_raise, product_id, returned_value, correct_value, side_effect",
    [
        (False, 0, product_list[0], product_list[0], None),
        (False, 1, product_list[1], product_list[1], None),
        (True, 10, None, None, NotFoundProductException(product_id=10)),
    ],
)
def test_get_product(should_raise, product_id, returned_value, correct_value, side_effect):
    product_repo = ProductRepository
    order_repo = MagicMock()
    service = WarehouseService(product_repo, order_repo)
    with mock.patch.object(ProductRepository, "get", return_value=returned_value, side_effect=side_effect):
        if should_raise:
            with pytest.raises(NotFoundProductException):
                service.get_product(product_id)
        else:
            assert service.get_product(product_id) == correct_value


@pytest.mark.parametrize(
    "returned_value, correct_value",
    [
        (product_list, product_list),
        ([], []),
        (None, None),
    ],
)
def test_list_product(returned_value, correct_value):
    product_repo = ProductRepository
    order_repo = MagicMock()
    service = WarehouseService(product_repo, order_repo)
    with mock.patch.object(ProductRepository, "list", return_value=returned_value):
        assert service.list_product() == correct_value


@pytest.mark.parametrize(
    "should_raise, products_in_order, product_list, correct_value, side_effect",
    [
        (False, product_list, product_list, Order(None, product_list), None),
        (False, product_list[:1], product_list, Order(None, product_list[:1]), None),
        (
            True,
            [],
            product_list,
            None,
            OrderNotCreatedException(message="An order can't be created. Product list is empty"),
        ),
        (
            True,
            [product_list[0], product_list[0]],
            None,
            None,
            OrderNotCreatedException(
                message=f"An order can't be created. These products {[product_list[0]]} have been added more than once."
            ),
        ),
        (True, product_list[:1], product_list[1:], None, OrderNotCreatedException(products=product_list[:1])),
    ],
)
def test_create_order(should_raise, products_in_order, product_list, correct_value, side_effect):
    product_repo = ProductRepository
    order_repo = MagicMock()
    service = WarehouseService(product_repo, order_repo)

    with mock.patch.object(ProductRepository, "list", return_value=product_list):
        if should_raise:
            with pytest.raises(OrderNotCreatedException) as exc_info:
                service.create_order(products_in_order)
            assert str(exc_info.value) == side_effect.args[0]
        else:
            assert service.create_order(products_in_order) == correct_value


@pytest.mark.parametrize(
    "should_raise, order_id, returned_value, correct_value",
    [
        (False, 0, Order(0, product_list), Order(0, product_list)),
        (False, 1, Order(1, product_list[:1]), Order(1, product_list[:1])),
        (True, 10, None, NotFoundOrderException(order_id=10)),
    ],
)
def test_get_order(should_raise, order_id, returned_value, correct_value):
    product_repo = MagicMock()
    order_repo = OrderRepository
    service = WarehouseService(product_repo, order_repo)
    if should_raise:
        with (
            pytest.raises(NotFoundOrderException) as exc_info,
            mock.patch.object(
                SqlAlchemyProductRepository, "get", return_value=NoResultFound("No row was found when one was required")
            ),
        ):
            service.get_order(10)
        assert str(exc_info.value) == correct_value.args[0]
    else:
        with mock.patch.object(OrderRepository, "get", return_value=returned_value):
            assert service.get_order(order_id) == correct_value


@pytest.mark.parametrize(
    "should_raise, name, quantity, price, product_list_test, correct_value, side_effect",
    [
        (False, "name", 1, 1, product_list[1:], Product(None, "name", 1, 1), None),
        (False, "name2", 2, 3, product_list[:1], Product(None, "name2", 2, 3), None),
        (
            True,
            product_list[0].name,
            3,
            4,
            product_list,
            None,
            ProductAlreadyExistsException(product_name=product_list[0].name),
        ),
    ],
)
def test_create_product(should_raise, name, quantity, price, product_list_test, correct_value, side_effect):
    product_repo = ProductRepository
    order_repo = MagicMock()
    service = WarehouseService(product_repo, order_repo)
    if should_raise:
        with (
            pytest.raises(ProductAlreadyExistsException) as exc_info,
            mock.patch.object(ProductRepository, "list", return_value=product_list),
        ):
            service.create_product(name, quantity, price)
        assert str(exc_info.value) == side_effect.args[0]
    else:
        with (
            mock.patch.object(ProductRepository, "list", return_value=product_list_test),
            mock.patch.object(ProductRepository, "add", return_value=None),
        ):
            assert service.create_product(name, quantity, price) == correct_value


@pytest.mark.parametrize(
    "returned_value, correct_value",
    [
        (Order(0, product_list), Order(0, product_list)),
        ([], []),
        (None, None),
    ],
)
def test_list_order(returned_value, correct_value):
    product_repo = MagicMock()
    order_repo = OrderRepository
    service = WarehouseService(product_repo, order_repo)
    with mock.patch.object(OrderRepository, "list", return_value=returned_value):
        assert service.list_orders() == correct_value
