from fastapi import status
from ..models import OrdersStatus

from .utils import *

def test_read_all_authenticated(test_orders):
    response = client.get("/order")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {"id": 1, "item": "Pizza", "price": 10.0, "time": 1620000000, "order_status": OrdersStatus.PENDING.value, "customer_id": 1},
        {"id": 2, "item": "Burger", "price": 5.0, "time": 1620003600, "order_status": OrdersStatus.COMPLETED.value, "customer_id": 1}
    ]