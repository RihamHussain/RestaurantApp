from datetime import timedelta, datetime, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request, Cookie, Response  
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from ..database import SessionLocal
from ..models import User, Role
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from ..helpers import config
from fastapi.templating import Jinja2Templates
import os

settings = config.get_settings()
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

# Setup templates path (consistent with your main.py)
base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
templates = Jinja2Templates(directory=os.path.join(base_dir, "templates"))


# 1. ADD THIS: Route to show the Login Page
@router.get("/login")
async def render_login_page(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")

# 2. ADD THIS: Route to show the Register Page
@router.get("/register")
async def render_register_page(request: Request):
    # Make sure you create a register.html later!
    return templates.TemplateResponse(request=request, name="register.html")

class Create_User_Request(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    phone_number: str
    role: str 


class Token(BaseModel):
    access_token: str
    token_type: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id: int, expires_delta: timedelta, role: str, is_superadmin: bool):
    encode = {'sub': username, 'id': user_id, 'role': role, 'is_superadmin': is_superadmin}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(access_token: Annotated[str | None, Cookie()] = None):
    # If cookie is missing
    if not access_token:
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Not authenticated (Cookie missing)')
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')
        is_superadmin: bool = payload.get('is_superadmin', False)
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user.')
        return {'username': username, 'id': user_id, 'role': user_role, 'is_superadmin': is_superadmin}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid token')

@router.get("/me")
async def get_user_info(current_user: Annotated[dict, Depends(get_current_user)]):
    return current_user

@router.post("/register")
async def create_user(db: db_dependency, create_user_request: Create_User_Request):

    # 1. Check if Username exists
    user_model = db.query(User).filter(User.username == create_user_request.username).first()
    if user_model:
        raise HTTPException(status_code=400, detail="Username already taken.")

    # 2. Check if Email exists
    email_model = db.query(User).filter(User.email == create_user_request.email).first()
    if email_model:
        raise HTTPException(status_code=400, detail="Email already registered.")
    
    # 3. Password Validation (Manual check if not using Pydantic)
    if len(create_user_request.password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters.")
    
    # SECURITY FIX: Always force role to 'customer' regardless of input
    
    create_user_model = User(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        phone_number=create_user_request.phone_number,
        role="customer",
        is_superadmin=False 
    )
    db.add(create_user_model)
    db.commit()


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency,
                                 response: Response, # Add response parameter
                                 ):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    token = create_access_token(user.username, user.id, timedelta(minutes=20), user.role, user.is_superadmin)
    # Set the cookie in the browser
    response.set_cookie(
        key="access_token", 
        value=token, 
        httponly=True,  # JavaScript cannot read this (Secure!)
        max_age=1200,   # Expires in 20 minutes (same as token)
        samesite="lax", 
        secure=True,    # Set to True if using HTTPS,
        path="/"
    )

    return {'access_token': token, 'token_type': 'bearer'}

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token", path="/") # <--- ADD THIS
    return {"message": "Logged out"}