import pytest
from io import BytesIO
from pathlib import Path
from unittest.mock import AsyncMock, patch

from httpx import AsyncClient

from tests.conftest import auth_header, create_test_user, login_user


@pytest.mark.anyio
async def test_empty_database(client: AsyncClient):
    response = await client.get("/api/users/showcase")
    assert response.status_code == 200
    data = response.json()
    print("\n.Empty Database Test Complete. Database Here ---> ",data)


@pytest.mark.anyio
async def test_create_user_validation_error(client: AsyncClient):
    response = await client.post(
        "/api/users/creation", 
        json = { "email": "testuser@gmail.com", 
                "password": "apple"}
        )
    assert response.status_code == 422
    assert "email" in response.text
    assert "password" in response.text
    print("Test_Create_User_Validation_Error Complete")


@pytest.mark.anyio
async def test_create_user_duplicate_email(client: AsyncClient):
    await create_test_user(client)
    response = await client.post("/api/users/creation",
        json = {
            "name": "testuser",
            "email": "test@gmail.com",
            "password": "testpassword123",
            "total_assets": 10000,
            "total_debt": 840,
            "phone_number" : "1234567891"
        }
    )
    assert response.status_code == 409
    assert response.json()["detail"] == "WealthManager Already Exists"
    print("Test_Create_User_Duplicate_Email Success")


@pytest.mark.anyio
async def test_create_user_field_types_wrong(client: AsyncClient):
    response = await client.post("/api/users/creation",
        json = {
            "name" : 1,
            "email" : 2,
            "password" : 3,
            "net_worth" : "3.00",
            "total_assets": 10000,
            "total_debt": 840,
            "phone_number" : "1234567891"
        }
    )
    assert response.status_code == 422
    print("Test_Create_User_Field_Types_Wrong Success")


@pytest.mark.anyio
async def test_create_test_user_success(client: AsyncClient):
    response = await client.post("/api/users/creation",
        json = {
            "name" : "name",
            "email" : "name@gmail.com",
            "password" : "namepassword",
            "total_assets": 10000,
            "total_debt": 840,
            "phone_number" : "1234567891"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["email"] == "name@gmail.com"
    assert data["name"] == "name"
    assert "id" in data
    assert "password" not in data
    assert "hashed_password" not in data
    print("Create_Test_User_Success")


@pytest.mark.anyio
async def test_delete_user(client: AsyncClient):
    email = "name1@gmail.com"
    password = "namepassword1"

    response = await client.post("/api/users/creation",
        json = {
            "name" : "name1",
            "email" : email,
            "password" : password,
            "total_assets": 10000,
            "total_debt": 840,
            "phone_number" : "1234567891"
        }
    )
    assert response.status_code == 201
    data = response.json()
    token = await login_user(client, email, password)
    assert response.status_code == 201
    response = await client.delete(f"/api/users/delete/{data['id']}",
        headers = auth_header(token), 
    )
    assert response.status_code == 204
    print("Test_Delete_User Success")


@pytest.mark.anyio
async def test_forgot_password_sends_email(client: AsyncClient):
    await create_test_user(client)
    with patch("backend.routers.users.send_password_reset_email",
                new_callable= AsyncMock,
    ) as mock_send:
        response = await client.post("/api/users/forgot-password", 
            json={"email": "test@gmail.com"},
        )
    assert response.status_code == 202
    mock_send.assert_awaited_once()
    call_kwargs = mock_send.call_args.kwargs
    assert call_kwargs["to_email"] == "test@gmail.com"
    assert call_kwargs["username"] == "test@gmail.com"
    assert "token" in call_kwargs
    print("Test_Forgot_Password_Sends_Email Success")
