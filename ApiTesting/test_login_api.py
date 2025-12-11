from playwright.sync_api import sync_playwright
import pytest

BASE_URL = "https://192.168.1.236:8080"


# ---------------------------------------------------------
# Reusable Login Function
# ---------------------------------------------------------
def perform_login(request_context, username, password):
    login_payload = {
        "username": username,
        "password": password
    }

    response = request_context.post(
        "/api/auth/login",
        data=login_payload,
        headers={"Content-Type": "application/json"}
    )

    return response


# ---------------------------------------------------------
# Test Data — All scenarios
# ---------------------------------------------------------
login_test_cases = [
    ("superadmin", "Admin@1234", True, "Valid credentials"),
    ("", "", False, "Both empty"),
    ("superadmin", "", False, "Password empty"),
    ("", "Admin@1234", False, "Username empty"),
    ("   ", "   ", False, "Spaces only"),
    ("wronguser", "Admin@1234", False, "Wrong username"),
    ("superadmin", "wrongpass", False, "Wrong password")
]


# ---------------------------------------------------------
# Actual parameterized test
# ---------------------------------------------------------
@pytest.mark.parametrize("username, password, should_pass, description", login_test_cases)
def test_login_api(username, password, should_pass, description):

    print(f"\n🔍 TEST CASE: {description}")
    print(f"   Username = '{username}', Password = '{password}'")

    with sync_playwright() as p:

        request_context = p.request.new_context(
            base_url=BASE_URL
        )

        response = perform_login(request_context, username, password)
        print("STATUS =", response.status)

        # ----------- EXPECTED PASS -----------
        if should_pass:
            assert response.status == 200, "❌ Expected success but got failure!"
            json_data = response.json()
            print("RESPONSE:", json_data)

            # Token must exist for successful login
            assert "token" in json_data, "❌ Token missing in valid login!"

            print("✅ PASSED — Valid login returned token!")

        # ----------- EXPECTED FAIL -----------
        else:
            assert response.status != 200, "❌ Expected failure but login succeeded!"
            print("❌ Correctly failed — Invalid credentials test passed.")
