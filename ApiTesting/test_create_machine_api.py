import pytest
from playwright.sync_api import sync_playwright
from api_client import APIClient

BASE_URL = "http://172.30.2.94:8080"


# ---------------------------------------------------------
# Helper: Machine Create API
# ---------------------------------------------------------
def create_machine(request_context, payload):
    response = request_context.post(
        "/machine/create",
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    return response


# ---------------------------------------------------------
# TEST CASES — Valid + Invalid
# ---------------------------------------------------------
machine_test_cases = [

    # 1️⃣ VALID MACHINE (should pass)
    ({
        "name": "robot1277",
        "envName": "zahra",
        "licenseId": "b3605639-21be-9f9d-bb05-1510da528c0a",
    }, True, "Valid machine"),

    # 2️⃣ EMPTY NAME
    ({
        "name": "",
        "envName": "zahra",
        "licenseId": "b3605639-21be-9f9d-bb05-1510da528c0a",
    }, False, "Machine name empty"),

    # 3️⃣ NAME TOO SHORT
    ({
        "name": "r",
        "envName": "zahra",
        "licenseId": "b3605639-21be-9f9d-bb05-1510da528c0a",
    }, False, "Machine name too short"),

    # 4️⃣ NAME TOO LONG
    ({
        "name": "robo_machine_name_is_too_long_12345678901234567890",
        "envName": "zahra",
        "licenseId": "b3605639-21be-9f9d-bb05-1510da528c0a",
    }, False, "Machine name too long"),

    # 5️⃣ MISSING LICENSE ID
    ({
        "name": "robot4",
        "envName": "zahra",
        "licenseId": "",
    }, False, "Missing license ID"),

    # 6️⃣ WRONG LICENSE ID
    ({
        "name": "robot5",
        "envName": "zahra",
        "licenseId": "wrong-license-id",
    }, False, "Invalid license ID"),

    

    # 8️⃣ INVALID ENVIRONMENT NAME
    ({
        "name": "robot7",
        "envName": "wrongEnvName",
        "licenseId": "b3605639-21be-9f9d-bb05-1510da528c0a",
    }, False, "Invalid environment name")
]


# ---------------------------------------------------------
# PARAMETERIZED TEST
# ---------------------------------------------------------
@pytest.mark.parametrize("payload, should_pass, description", machine_test_cases)
def test_create_machine(payload, should_pass, description):

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

        response = create_machine(request_context, payload)

        print("STATUS:", response.status)
        print("RESPONSE:", response.text())

        # -----------------------------------------------
        # EXPECTED SUCCESS
        # -----------------------------------------------
        if should_pass:
            assert response.status == 200, "❌ Valid machine creation failed!"
            print("✅ Machine created successfully")

        # -----------------------------------------------
        # EXPECTED FAILURE
        # -----------------------------------------------
        else:
            assert response.status != 200, "❌ Invalid data should NOT create machine!"
            print("❌ Correctly failed as expected")
