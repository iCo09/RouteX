import uuid
import pytest
from httpx import AsyncClient


# ---------------------------------------------------------------------------
# Test 1: Successful Customer Registration
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_register_customer_success(async_client: AsyncClient):
    """
    Verifies that a customer can register successfully:
    - Returns 201 Created.
    - Persists user info (email, full_name, role).
    - Ensures hashed_password is NOT returned in response.
    - Confirms customer accounts are active by default.
    """
    unique_email = f"customer_{uuid.uuid4().hex[:8]}@example.com"
    payload = {
        "email": unique_email,
        "password": "StrongPassword123!",
        "full_name": "Rahul Bisht",
        "phone_number": "+919876543210",
        "role": "customer",
    }
    response = await async_client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == unique_email
    assert data["full_name"] == "Rahul Bisht"
    assert data["role"] == "customer"
    assert data["is_active"] is True
    assert "hashed_password" not in data
    assert "id" in data


# ---------------------------------------------------------------------------
# Test 2: Duplicate Email Rejection
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_register_duplicate_email_fails(async_client: AsyncClient):
    """
    Verifies the uniqueness constraint on email:
    - First registration succeeds (201).
    - Second registration with identical email returns 400 Bad Request.
    """
    unique_email = f"duplicate_{uuid.uuid4().hex[:8]}@example.com"
    payload = {
        "email": unique_email,
        "password": "password123!",
        "full_name": "Duplicate Test",
        "role": "customer",
    }
    # First attempt: success
    res1 = await async_client.post("/api/v1/auth/register", json=payload)
    assert res1.status_code == 201

    # Second attempt: conflict rejection
    res2 = await async_client.post("/api/v1/auth/register", json=payload)
    assert res2.status_code == 400
    assert "already exists" in res2.json()["detail"]


# ---------------------------------------------------------------------------
# Test 3: Full Auth Flow (Register -> Login -> Access Protected /me)
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_login_and_access_protected_me_endpoint(async_client: AsyncClient):
    """
    Verifies the entire JWT authentication cycle:
    1. Register user.
    2. Login with credentials and receive access + refresh tokens.
    3. Send 'Authorization: Bearer <access_token>' to GET /me.
    4. Confirm correct user profile is returned.
    """
    email = f"flow_{uuid.uuid4().hex[:8]}@example.com"
    password = "secretPassword123!"

    # 1. Register
    reg_response = await async_client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": password,
            "full_name": "Auth Flow User",
            "role": "customer",
        },
    )
    assert reg_response.status_code == 201

    # 2. Login
    login_response = await async_client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )
    assert login_response.status_code == 200
    token_data = login_response.json()
    assert "access_token" in token_data
    assert "refresh_token" in token_data
    assert token_data["token_type"] == "bearer"
    assert token_data["user"]["email"] == email

    access_token = token_data["access_token"]

    # 3. Access protected /me endpoint with Bearer token
    me_response = await async_client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert me_response.status_code == 200
    me_data = me_response.json()
    assert me_data["email"] == email
    assert me_data["full_name"] == "Auth Flow User"


# ---------------------------------------------------------------------------
# Test 4: Invalid Password Rejection
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_login_with_invalid_credentials(async_client: AsyncClient):
    """
    Verifies that wrong password or non-existent email returns 401 Unauthorized.
    """
    response = await async_client.post(
        "/api/v1/auth/login",
        json={"email": "nobody@example.com", "password": "wrongPassword123!"},
    )
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]


# ---------------------------------------------------------------------------
# Test 5: Unauthorized Access to Protected Endpoint
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_unauthorized_access_fails(async_client: AsyncClient):
    """
    Verifies that calling GET /me without Authorization header returns 401.
    """
    response = await async_client.get("/api/v1/auth/me")
    assert response.status_code == 401
