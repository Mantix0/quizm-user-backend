import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.config import get_db_url
from app.dependencies import get_session
from app.main import app


@pytest.fixture
async def test_client():
    engine_test = create_async_engine(get_db_url(), echo=True)
    async_session_test = async_sessionmaker(engine_test, expire_on_commit=False)

    async with engine_test.connect() as connection:
        trans = await connection.begin()
        session = async_session_test(bind=connection)

        async def override_get_session():
            yield session

        app.dependency_overrides[get_session] = override_get_session

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://") as client:
            yield client

        await session.close()
        await trans.rollback()
        await connection.close()
        await engine_test.dispose()

    app.dependency_overrides.clear()


@pytest.fixture()
async def user_payload():
    return {
        "username": "JohnDoe",
        "email": "JohnDoe@gmail.com",
        "password": "12s34f5g6",
    }


@pytest.fixture()
async def user_payload_invalid():
    return {
        "username": "JohnDoe",
        "email": "JohnDoe",
        "password": "12s34f5g6",
    }


@pytest.mark.asyncio
async def test_nonexistent_page(test_client):
    response = await test_client.get("/page")
    assert response.status_code == 200
    assert response.json() == {
        "data": "null",
        "errors": [
            {"code": "NotFoundHttpException", "message": "Страница не существует"}
        ],
    }


@pytest.mark.asyncio
async def test_register(test_client, user_payload):
    response = await test_client.post("api/v1/users:register/", json=user_payload)
    assert response.status_code == 200
    assert response.json() == {"message": "Вы успешно зарегистрированы!"}


@pytest.mark.asyncio
async def test_register_invalid(test_client, user_payload_invalid):
    response = await test_client.post(
        "api/v1/users:register/", json=user_payload_invalid
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_login_user(test_client, user_payload):
    await test_client.post("/api/v1/users:register/", json=user_payload)
    response = await test_client.post(
        "/api/v1/users:login/",
        json={"email": user_payload["email"], "password": user_payload["password"]},
    )
    assert response.status_code == 200
    assert "user_access_token" in response.json()


@pytest.mark.asyncio
async def test_logout_user(test_client, user_payload):
    await test_client.post("/api/v1/users:register/", json=user_payload)
    login_response = await test_client.post(
        "/api/v1/users:login/",
        json={"email": user_payload["email"], "password": user_payload["password"]},
    )
    access_token = login_response.json()["user_access_token"]

    headers = {"Cookie": f"users_access_token={access_token}"}
    response = await test_client.post("/api/v1/users:logout/", headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Пользователь успешно вышел из системы"


@pytest.mark.asyncio
async def test_get_user_by_id(test_client, user_payload):
    await test_client.post("/api/v1/users:register/", json=user_payload)
    login_response = await test_client.post(
        "/api/v1/users:login/",
        json={"email": user_payload["email"], "password": user_payload["password"]},
    )

    access_token = login_response.json()["user_access_token"]
    headers = {"Cookie": f"users_access_token={access_token}"}

    current_user = await test_client.get("/api/v1/users:current-user/", headers=headers)
    user_id = current_user.json()["data"]["id"]

    response = await test_client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["data"]["email"] == user_payload["email"]


@pytest.mark.asyncio
async def test_get_user_records_by_id(test_client, user_payload):
    await test_client.post("/api/v1/users:register/", json=user_payload)

    login_response = await test_client.post(
        "/api/v1/users:login/",
        json={"email": user_payload["email"], "password": user_payload["password"]},
    )

    access_token = login_response.json()["user_access_token"]
    headers = {"Cookie": f"users_access_token={access_token}"}

    current_user = await test_client.get("/api/v1/users:current-user/", headers=headers)
    user_id = current_user.json()["data"]["id"]

    response = await test_client.get(f"/api/v1/users/{user_id}/records")
    assert response.status_code == 200
    assert isinstance(response.json()["data"], list)


@pytest.mark.asyncio
async def test_add_record_to_current_user(test_client, user_payload):
    await test_client.post("/api/v1/users:register/", json=user_payload)
    login_response = await test_client.post(
        "/api/v1/users:login/",
        json={"email": user_payload["email"], "password": user_payload["password"]},
    )

    access_token = login_response.json()["user_access_token"]
    headers = {"Cookie": f"users_access_token={access_token}"}
    record_data = {"quiz_id": 1, "score": 85}

    response = await test_client.post(
        "/api/v1/users:current-user/records", json=record_data, headers=headers
    )
    assert response.status_code == 200
    assert response.json()["data"]["score"] == 85
