import json
from playwright.sync_api import sync_playwright
from api_client import APIClient

BASE_URL = "http://172.24.186.84:8080"


# ============================================================
# TEST 1 — EMAIL SUMMARIZATION MODEL
# ============================================================
def test_email_summarization_model():
    """Test Email Summarization BEFORE creating the AI App."""
    client = APIClient(BASE_URL)
    token = client.login("superadmin", "Admin@1234")

    test_payload = {
        "appName": "esummarize",
        "maximumLength": "3",
        "context": "sad day",
        "emailSubject": "sick leave",
        "emailBodyText": "I am very sick today and want a leave so I can rest and get better."
    }

    with sync_playwright() as p:
        request_context = p.request.new_context(
            base_url=BASE_URL,
            ignore_https_errors=True,
            extra_http_headers={"Authorization": f"Bearer {token}"}
        )

        response = request_context.post(
            "/aiCenter/emailSummarization",
            multipart={
                "dataString": json.dumps(test_payload),
                "apiKey": "null"
            }
        )

        print("MODEL STATUS:", response.status)
        print("MODEL RESPONSE:", response.json())

        # For Email Summarization, FAIL is normal if model is not configured
        assert response.status == 200, "❌ EmailSummarization API FAILED!"
        assert response.json()["message"] == "success"

        print("✔ MODEL CALLED SUCCESSFULLY (Even if response = FAIL)")


# ============================================================
# TEST 2 — CREATE EMAIL SUMMARIZATION APP
# ============================================================
def test_email_summarization_create():
    """Create Email Summarization AI App — handles 200 and 304."""
    client = APIClient(BASE_URL)
    token = client.login("superadmin", "Admin@1234")

    payload = {
        "appName": "esummarize2",
        "maximumLength": "3",
        "context": "sad day",
        "emailSubject": "",
        "emailBodyText": "",
        "env": "zahra"
    }

    with sync_playwright() as p:
        request_context = p.request.new_context(
            base_url=BASE_URL,
            ignore_https_errors=True,
            extra_http_headers={"Authorization": f"Bearer {token}"}
        )

        response = request_context.post(
            "/aiCenter/env/zahra/insert",
            multipart={
                "data": json.dumps(payload),
                "capabilityType": "EmailSummarization"
            }
        )

        print("CREATE STATUS:", response.status)

        # Already exists → 304
        if response.status == 304:
            print("✔ EmailSummarization App already exists — Test Passed.")
            assert True
            return

        # Fresh success
        assert response.status == 200, "❌ Failed to CREATE EmailSummarization app!"
        resp_json = response.json()

        print("CREATE RESPONSE:", resp_json)
        assert "AI App created successfully" in resp_json["message"]

        print("✔ EmailSummarization APP CREATED SUCCESSFULLY!")
# ============================================================
# COMMON FUNCTION — UPDATE EMAIL APP STATUS (disable/enable/delete)
# ============================================================
def update_email_app_status(action, appName="esummarize2"):
    client = APIClient(BASE_URL)
    token = client.login("superadmin", "Admin@1234")

    with sync_playwright() as p:
        request_context = p.request.new_context(
            base_url=BASE_URL,
            ignore_https_errors=True,
            extra_http_headers={"Authorization": f"Bearer {token}"}
        )

        # STEP 1 — Get list of apps
        get_response = request_context.get("/aiCenter/env/zahra/getApps")
        assert get_response.status == 200, "❌ Failed to fetch apps list!"

        apps_list = get_response.json()
        print("\nAPPS LIST:", apps_list)

        # STEP 2 — Find ID of the email summarization app
        found_id = None
        for app in apps_list:
            if app.get("name") == appName:
                found_id = app.get("id")
                break

        assert found_id is not None, f"❌ App '{appName}' not found in Zahra environment!"
        print(f"✔ Found App ID: {found_id} for action: {action}")

        # STEP 3 — Prepare request payload
        payload = {
            "id": str(found_id),
            "env": "zahra",
            "action": action
        }

        # STEP 4 — Hit updateStatus API
        response = request_context.post(
            "/aiCenter/env/zahra/updateStatus",
            multipart={"data": json.dumps(payload)}
        )

        print(f"\n{action.upper()} STATUS:", response.status)

        # Handle responses
        if response.status == 304:
            print(f"✔ Already {action} — Test Passed.")
            return True

        if response.status == 200:
            resp_json = response.json()
            print(f"{action.upper()} RESPONSE:", resp_json)

            assert "success" in resp_json.get("message", "").lower()
            print(f"✔ App successfully {action}d.")
            return True

        assert False, f"❌ Unexpected status code: {response.status}"
def test_email_summarization_disable():
    assert update_email_app_status("disable") is True
def test_email_summarization_enable():
    assert update_email_app_status("enable") is True
def test_email_summarization_delete():
    assert update_email_app_status("delete") is True
