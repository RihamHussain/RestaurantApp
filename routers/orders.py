from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from models import Orders, OrdersStatus
from database import SessionLocal
from .auth import get_current_user
import time

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class OrderRequest(BaseModel):
    item: str = Field(min_length=3)
    price: float = Field(gt=0.0)
    time : int = Field (time.time())
    status : OrdersStatus


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Orders).filter(Orders.customer_id == user.get('id')).all()


@router.get("/orders/{order_id}", status_code=status.HTTP_200_OK)
async def read_orders(user: user_dependency, db: db_dependency, order_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    order_model = db.query(Orders).filter(Orders.id == order_id)\
        .filter(Orders.customer_id == user.get('id')).first()
    if order_model is not None:
        return order_model
    raise HTTPException(status_code=404, detail='Order not found.')


@router.post("/orders", status_code=status.HTTP_201_CREATED)
async def create_orders(user: user_dependency, db: db_dependency,
                      orders_request: OrderRequest):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    orders_model = Orders(**orders_request.model_dump(), customer_id=user.get('id'))
    print("orders_model", orders_model)
    db.add(orders_model)
    db.commit()


@router.put("/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_orders(user: user_dependency, db: db_dependency,
                      orders_request: OrderRequest,
                      order_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    order_model = db.query(Orders).filter(Orders.id == order_id)\
        .filter(Orders.customer_id == user.get('id')).first()
    if order_model is None:
        raise HTTPException(status_code=404, detail='Order not found.')

    order_model.item = orders_request.item
    order_model.price = orders_request.price
    order_model.time = orders_request.time
    order_model.status = orders_request.status

    db.add(order_model)
    db.commit()


@router.delete("/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_orders(user: user_dependency, db: db_dependency, order_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    orders_model = db.query(Orders).filter(Orders.id == order_id)\
        .filter(Orders.customer_id == user.get('id')).first()
    if orders_model is None:
        raise HTTPException(status_code=404, detail='Order not found.')
    db.query(Orders).filter(Orders.id == order_id).filter(Orders.customer_id == user.get('id')).delete()

    db.commit()












