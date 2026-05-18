from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from ..models import Orders
from ..database import SessionLocal
from .auth import get_current_user
from fastapi import Request # Add this import
from fastapi.templating import Jinja2Templates
import os
from ..models import User # Add this import at the top


router = APIRouter(
    prefix='/admin',
    tags=['admin']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

# Setup templates
base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
templates = Jinja2Templates(directory=os.path.join(base_dir, "templates"))

@router.get("/management", status_code=status.HTTP_200_OK)
async def render_admin_management_page(request: Request):
    return templates.TemplateResponse(request=request, name="admin_management.html")


@router.get("/orders", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Orders).all()


@router.delete("/orders/{orders_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_orders(user: user_dependency, db: db_dependency, orders_id: int = Path(gt=0)):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    orders_model = db.query(Orders).filter(Orders.id == orders_id).first()
    if orders_model is None:
        raise HTTPException(status_code=404, detail='orders not found.')
    db.query(Orders).filter(Orders.id == orders_id).delete()
    db.commit()


# 1. Get all users so the admin can see the list
@router.get("/users", status_code=status.HTTP_200_OK)
async def read_all_users(user: user_dependency, db: db_dependency):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(User).all()

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user: user_dependency, db: db_dependency, user_id: int = Path(gt=0)):
    # 1. Basic Auth check
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')

    # 2. Find the target user
    user_model = db.query(User).filter(User.id == user_id).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail='User not found.')

    # 3. GET REQUESTER STATUS
    is_requester_super = user.get('is_superadmin')

    # 4. HIERARCHY LOGIC
    # If the target is an admin
    if user_model.role == 'admin':
        # AND I am not a super admin -> BLOCK
        if not is_requester_super:
            raise HTTPException(
                status_code=403, 
                detail='Forbidden: Admins cannot delete other admins. Only Super Admins can do this.'
            )
        
        # Safety check: Prevent deleting any Super Admin (including self)
        if user_model.is_superadmin:
            raise HTTPException(
                status_code=403, 
                detail='Forbidden: Super Admins cannot be deleted through the API.'
            )

    # 5. Execute Delete (If it reached here, either target is a Customer, 
    # or target is an Admin and requester is a Super Admin)
    Orders_models = db.query(Orders).filter(Orders.customer_id == user_id).all()
    if Orders_models:
        for order in Orders_models:
            db.query(Orders).filter(Orders.id == order.id).delete()
            db.commit()
    db.query(User).filter(User.id == user_id).delete()
    db.commit()


# 2. Promote a specific user to Admin
@router.put("/promote/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def promote_to_admin(user: user_dependency, db: db_dependency, user_id: int = Path(gt=0)):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    if user.get('is_superadmin') is not True:
        raise HTTPException(status_code=403, detail='Forbidden: Only superadmins can promote users to admin.')
    user_model = db.query(User).filter(User.id == user_id).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail='User not found.')
    
    user_model.role = 'admin'
    db.add(user_model)
    db.commit()

@router.put("/demote/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def demote_to_user(user: user_dependency, db: db_dependency, user_id: int = Path(gt=0)):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    if user.get('is_superadmin') is not True:
        raise HTTPException(status_code=403, detail='Forbidden: Only superadmins can downgrade admins to users.')
    user_model = db.query(User).filter(User.id == user_id).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail='User not found.')
    # Safety check: Super admin cannot demote themselves
    if user_model.id == user.get('id'):
        raise HTTPException(status_code=400, detail='Cannot demote yourself.')
    
    user_model.role = 'customer'
    db.add(user_model)
    db.commit()