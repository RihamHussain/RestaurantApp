from .utils import *
from ..routers.users import get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_get_current_user(test_user):
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == "testuser"
    assert response.json()['email'] == "testuser@example.com"
    assert response.json()['first_name'] == "Test"
    assert response.json()['last_name'] == "User"   
    assert response.json()['phone_number'] == "1234567890"
    assert response.json()['role'] == Role.CUSTOMER.value
    password =  response.json().get('hashed_password')  
    bcrypt_context.verify(password, bcrypt_context.hash("fakepassword"))

def test_change_password(test_user):
    response = client.put("/user/password", json={"password": "fakepassword", "new_password": "newfakepassword"})
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify the password is changed
    db = TestingSessionLocal()
    user_model = db.query(User).filter(User.id == test_user.id).first()
    assert bcrypt_context.verify("newfakepassword", user_model.hashed_password)

def test_change_password_invalid(test_user):
    response = client.put("/user/password", json={"password": "wrongpassword", "new_password": "newfakepassword"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Error on password change"}

    # Verify the password is not changed
    db = TestingSessionLocal()
    user_model = db.query(User).filter(User.id == test_user.id).first()
    assert bcrypt_context.verify("fakepassword", user_model.hashed_password)

def test_change_phonenumber(test_user):
    response = client.put("/user/phonenumber/0987654321")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify the phone number is changed
    db = TestingSessionLocal()
    user_model = db.query(User).filter(User.id == test_user.id).first()
    assert user_model.phone_number == "0987654321"