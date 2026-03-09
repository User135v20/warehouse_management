class WarehouseServiceError(Exception):
    """basic exception class"""

    def __init__(self, message):
        if not message:
            message = "Unknown problem with warehouse service"
        super().__init__(message)


class ProductAlreadyExistsException(WarehouseServiceError):
    def __init__(self, product_name):
        message = f"A product with the name '{product_name}' already exists."
        super().__init__(message=message)

class NotFoundProductException(WarehouseServiceError):
    def __init__(self, product_id):
        message = f"No product with id={product_id} was found."
        super().__init__(message=message)

class OrderNotCreatedException(WarehouseServiceError):
    def __init__(self, products = None, message = None):
        if not message:
            message = f"Order cannot be created: {products} not found."
        super().__init__(message)

class NotFoundOrderException(WarehouseServiceError):
    def __init__(self, order_id):
        message = f"No order with id={order_id} was found."
        super().__init__(message=message)
