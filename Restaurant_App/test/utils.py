from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from ..database import Base
from ..main import app
from ..models import Role, User
from fastapi.testclient import TestClient
from ..routers.orders import get_db, get_current_user
from ..helpers import config
import pytest
from ..models import Orders, OrdersStatus
from sqlalchemy import text
from ..routers.auth import bcrypt_context

settings = config.get_settings()

SQLALCHEMY_TEST_DATABASE_URL = settings.SQLALCHEMY_TEST_DATABASE_URL

engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, poolclass=StaticPool)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Base.metadata.create_all(bind=engine)
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {
        "id": 1,
        "username": "testuser",
        "email": "testuser@example.com",
        "first_name": "Test",
        "last_name": "User",
        "phone_number": "1234567890",
        "role": Role.ADMIN.value
    }


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)


def _clean_all(db):
    """Helper to wipe test data and reset sequences."""
    db.execute(text("TRUNCATE TABLE orders RESTART IDENTITY CASCADE"))
    db.execute(text("TRUNCATE TABLE users RESTART IDENTITY CASCADE"))
    db.commit()


@pytest.fixture()
def test_orders():
    db = TestingSessionLocal()

    # ✅ Clean BEFORE inserting — prevents cascading failures from a previous run
    _clean_all(db)

    test_user = User(
        id=1,
        email="testuser@example.com",
        username="testuser",
        first_name="Test",
        last_name="User",
        hashed_password="fakehashedpassword",
        role=Role.CUSTOMER.value
    )
    db.add(test_user)
    db.commit()

    order1 = Orders(item="Pizza", price=10.0, time=1620000000,
                    order_status=OrdersStatus.PENDING.value, customer_id=1)
    order2 = Orders(item="Burger", price=5.0, time=1620003600,
                    order_status=OrdersStatus.COMPLETED.value, customer_id=1)
    db.add(order1)
    db.add(order2)
    db.commit()

    yield

    # ✅ Clean AFTER as well
    _clean_all(db)
    db.close()


@pytest.fixture()
def test_user():
    db = TestingSessionLocal()

    # ✅ Clean BEFORE inserting
    _clean_all(db)

    test_user = User(
        id=1,
        email="testuser@example.com",
        username="testuser",
        first_name="Test",
        last_name="User",
        hashed_password=bcrypt_context.hash("fakepassword"),
        role=Role.CUSTOMER.value,
        phone_number="1234567890"
    )
    db.add(test_user)
    db.commit()

    yield test_user

    # ✅ Clean AFTER as well
    _clean_all(db)
    db.close()