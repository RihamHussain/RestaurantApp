from .utils import *
from ..routers.admin import get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_admin_read_all_authenticated(test_orders):
    response = client.get("/admin/orders")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {"id": 1, "item": "Pizza", "price": 10.0, "time": 1620000000, "order_status": OrdersStatus.PENDING.value, "customer_id": 1},
        {"id": 2, "item": "Burger", "price": 5.0, "time": 1620003600, "order_status": OrdersStatus.COMPLETED.value, "customer_id": 1}
    ]

def test_admin_delete_order(test_orders):
    response = client.delete("/admin/orders/1")
    response = client.delete("/admin/orders/2")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify the order is deleted
    response = client.get("/admin/orders")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

    db = TestingSessionLocal()
    result = db.execute(text("SELECT * FROM orders WHERE id IN (1, 2)")).fetchall()
    assert len(result) == 0

def test_admin_delete_nonexistent_order():
    response = client.delete("/admin/orders/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "orders not found."}