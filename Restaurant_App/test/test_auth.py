from .utils import *
from ..routers.auth import get_db, authenticate_user, create_access_token, get_current_user
from datetime import timedelta
from jose import jwt
from fastapi import HTTPException

app.dependency_overrides[get_db] = override_get_db
db = TestingSessionLocal()

async def test_authenticate_user(test_user):

    user = authenticate_user(test_user.username, "fakepassword", db)
    assert user is not None
    assert user.username == test_user.username


async def test_authenticate_nonexistent_user(test_user):

    user = authenticate_user("nonexistentuser", "fakepassword", db)
    assert user is False

async def test_authenticate_wrong_password(test_user):
    user = authenticate_user(test_user.username, "wrongpassword", db)
    assert user is False

async def test_create_access_token(test_user):
    token = create_access_token(test_user.username, test_user.id, timedelta(minutes=15), Role.CUSTOMER.value, test_user.is_superadmin)
    assert token is not None

    decodedtoken = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    assert decodedtoken['sub'] == test_user.username
    assert decodedtoken['id'] == test_user.id   
    assert decodedtoken['role'] == Role.CUSTOMER.value

async def test_get_current_user_valid_token(test_user):
    encode = {'sub': test_user.username, 'id': test_user.id, 'role': Role.CUSTOMER.value}
    token = jwt.encode(encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    current_user = await get_current_user(token)
    assert current_user['username'] == test_user.username
    assert current_user['id'] == test_user.id
    assert current_user['role'] == Role.CUSTOMER.value

async def test_get_current_user_missing_payload():
    encode = {'role': Role.CUSTOMER.value}
    token = jwt.encode(encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token)
    
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == 'Could not validate user.'