from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float
import enum 
import time

class OrdersStatus(enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELED = "canceled"

class Role(enum.Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"
    OWNER = "owner"

class User(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    phone_number = Column(String)
    role = Column(String, default=Role.CUSTOMER.value)

class Orders(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    item = Column(String)
    price = Column(Float)
    time = Column(Integer, default=lambda: int(time.time()))
    order_status = Column(String, default=OrdersStatus.PENDING.value)
    customer_id = Column(Integer, ForeignKey("customers.id"))
