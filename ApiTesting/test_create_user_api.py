import pytest
from playwright.sync_api import sync_playwright
from api_client import APIClient

BASE_URL = "http://172.30.2.94:8080"


# ---------------------------------------------------------
# Helper: Create User API
# ---------------------------------------------------------
def create_user(request_context, payload):
    response = request_context.post(
        "/api/users",
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    return response


# ---------------------------------------------------------
# ALL TEST CASES
# ---------------------------------------------------------
user_test_cases = [

    # 1️⃣ VALID USER (should PASS)
    ({
        "username": "user_valid",
        "password": "Valid123@",
        "displayName": "Test User",
        "email": "testuser@gmail.com",
        "roles": ["user_role"],
        "taskhubLicenseId": "bb74aff1-4fa0-05da-91b4-2efb7b3d19fe"
    }, True, "Valid user"),

    # 2️⃣ FULL NAME MISSING
    ({
        "username": "user1",
        "password": "Valid123@",
        "displayName": "",
        "email": "test1@gmail.com",
        "roles": ["user_role"],
        "taskhubLicenseId": "bb74aff1-4fa0-05da-91b4-2efb7b3d19fe"
    }, False, "Full name missing"),

    # 3️⃣ PASSWORD NO CAPITAL LETTER
    ({
        "username": "user2",
        "password": "invalid123@",   # all lowercase
        "displayName": "User Two",
        "email": "test2@gmail.com",
        "roles": ["user_role"],
        "taskhubLicenseId": "bb74aff1-4fa0-05da-91b4-2efb7b3d19fe"
    }, False, "Password missing capital letter"),

    # 4️⃣ PASSWORD NO SPECIAL CHARACTER
    ({
        "username": "user3",
        "password": "Invalid123",    # no @#$ etc.
        "displayName": "User Three",
        "email": "test3@gmail.com",
        "roles": ["user_role"],
        "taskhubLicenseId": "bb74aff1-4fa0-05da-91b4-2efb7b3d19fe"
    }, False, "Password missing special character"),

    # 5️⃣ PASSWORD NO NUMBER
    ({
        "username": "user4",
        "password": "Invalid@Password",   # no digits
        "displayName": "User Four",
        "email": "test4@gmail.com",
        "roles": ["user_role"],
        "taskhubLicenseId": "bb74aff1-4fa0-05da-91b4-2efb7b3d19fe"
    }, False, "Password missing number"),

    # 6️⃣ USERNAME EMPTY
    ({
        "username": "",
        "password": "Valid123@",
        "displayName": "User Five",
        "email": "test5@gmail.com",
        "roles": ["user_role"],
        "taskhubLicenseId": "bb74aff1-4fa0-05da-91b4-2efb7b3d19fe"
    }, False, "Username empty"),

    # 7️⃣ PASSWORD EMPTY
    ({
        "username": "user6",
        "password": "",
        "displayName": "User Six",
        "email": "test6@gmail.com",
        "roles": ["user_role"],
        "taskhubLicenseId": "bb74aff1-4fa0-05da-91b4-2efb7b3d19fe"
    }, False, "Password empty"),

    # 8️⃣ EMAIL INVALID FORMAT
    ({
        "username": "user7",
        "password": "Valid123@",
        "displayName": "User Seven",
        "email": "wrongemailformat",
        "roles": ["user_role"],
        "taskhubLicenseId": "bb74aff1-4fa0-05da-91b4-2efb7b3d19fe"
    }, False, "Invalid email format"),

    # 9️⃣ EVERYTHING INVALID
    ({
        "username": "",
        "password": "abc",
        "displayName": "",
        "email": "123",
        "roles": ["user_role"],
        "taskhubLicenseId": "bb74aff1-4fa0-05da-91b4-2efb7b3d19fe"
    }, False, "Entire payload invalid")
]


# ---------------------------------------------------------
# PARAMETERIZED TEST
# ---------------------------------------------------------
@pytest.mark.parametrize("payload, should_pass, description", user_test_cases)
def test_create_user(payload, should_pass, description):

    print(f"\n🔍 TEST: {description}")

    client = APIClient(BASE_URL)
    token = client.login("superadmin", "Admin@1234")

    with sync_playwright() as p:

        request_context = p.request.new_context(
            base_url=BASE_URL,
            extra_http_headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )

        response = create_user(request_context, payload)

        print("STATUS:", response.status)
        print("RESPONSE:", response.text())

        # ---------------- PASS CASE ----------------
        if should_pass:
            assert response.status == 200, "❌ Valid user creation failed!"
            print("✅ User created successfully")

        # ---------------- FAIL CASE ----------------
        else:
            assert response.status != 200, "❌ Invalid data should NOT create user!"
            print("❌ Correctly failed as expected")
