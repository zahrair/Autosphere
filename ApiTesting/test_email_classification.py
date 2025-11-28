import json
from playwright.sync_api import sync_playwright
from api_client import APIClient

BASE_URL = "http://172.24.186.84:8080"


# ============================================================
# TEST 1 — EMAIL CLASSIFICATION MODEL TEST (FAIL IS OK)
# ============================================================
def test_email_classification_model():
    """Test Email Classification model BEFORE creating app."""
    client = APIClient(BASE_URL)
    token = client.login("superadmin", "Admin@1234")

    test_payload = {
        "appName": "EClassify",
        "context": "work from home",
        "categories": ["sad", "sick", "happy"],
        "multiCategory": False,
        "emailSubject": "work from home",
        "emailBodyText": "i am very sick today and unable to come to work",
    }

    with sync_playwright() as p:
        request_context = p.request.new_context(
            base_url=BASE_URL,
            ignore_https_errors=True,
            extra_http_headers={"Authorization": f"Bearer {token}"}
        )

        response = request_context.post(
            "/aiCenter/emailClassification",
            multipart={
                "dataString": json.dumps(test_payload),
                "apiKey": "null"
            }
        )

        print("MODEL TEST STATUS:", response.status)
        assert response.status == 200, "❌ EmailClassification API not reachable!"

        resp_json = response.json()
        print("MODEL RESPONSE:", resp_json)

        # Status must be present
        assert resp_json["status"] in [200, 400]

        # FAIL is allowed
        print("✔ MODEL TEST COMPLETED (PASS or FAIL allowed)")


# ============================================================
# TEST 2 — CREATE EMAIL CLASSIFICATION APP
# ============================================================
def test_email_classification_create_app():
    """Create Email Classification app (handles 200 + 304)."""

    client = APIClient(BASE_URL)
    token = client.login("superadmin", "Admin@1234")

    app_payload = {
        "appName": "EClassify",
        "context": "work from home",
        "categories": ["sad", "sick", "happy"],
        "multiCategory": False,
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
                "data": json.dumps(app_payload),
                "capabilityType": "EmailClassification"
            }
        )

        print("CREATE STATUS:", response.status)

        if response.status == 304:
            print("✔ APP ALREADY EXISTS — Test Passed.")
            return True

        assert response.status == 200, "❌ App creation failed!"

        resp_json = response.json()
        print("CREATE RESPONSE:", resp_json)

        assert "AI App created successfully" in resp_json.get("message", "")
        print("✔ APP CREATED SUCCESSFULLY")


# ============================================================
# HELPER — GET APP ID BY NAME
# ============================================================
def get_email_app_id(appName):
    client = APIClient(BASE_URL)
    token = client.login("superadmin", "Admin@1234")

    with sync_playwright() as p:
        request_context = p.request.new_context(
            base_url=BASE_URL,
            ignore_https_errors=True,
            extra_http_headers={"Authorization": f"Bearer {token}"}
        )

        resp = request_context.get("/aiCenter/env/zahra/getApps")
        assert resp.status == 200, "❌ Failed to fetch apps!"

        apps = resp.json()
        for app in apps:
            if app.get("name") == appName:
                return app.get("id")

    return None


# ============================================================
# TEST 3 — DISABLE / ENABLE / DELETE
# ============================================================
def update_email_app_status(action):
    client = APIClient(BASE_URL)
    token = client.login("superadmin", "Admin@1234")

    app_id = get_email_app_id("EClassify")
    assert app_id is not None, "❌ EClassify app not found!"

    print(f"✔ Using App ID {app_id} for {action}")

    payload = {
        "id": str(app_id),
        "env": "zahra",
        "action": action
    }

    with sync_playwright() as p:
        request_context = p.request.new_context(
            base_url=BASE_URL,
            ignore_https_errors=True,
            extra_http_headers={"Authorization": f"Bearer {token}"}
        )

        response = request_context.post(
            "/aiCenter/env/zahra/updateStatus",
            multipart={"data": json.dumps(payload)}
        )

        print(f"{action.upper()} STATUS:", response.status)

        if response.status == 304:
            print(f"✔ Already {action} — OK")
            return True

        if response.status == 200:
            print(f"✔ Successfully {action}d — OK")
            return True

        assert False, f"Unexpected status {response.status}"


def test_email_app_disable():
    assert update_email_app_status("disable")


def test_email_app_enable():
    assert update_email_app_status("enable")


def test_email_app_delete():
    assert update_email_app_status("delete")


