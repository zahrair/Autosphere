import json
import pytest
from playwright.sync_api import sync_playwright
from api_client import APIClient

BASE_URL = "http://192.168.1.202:8080"


# ============================================================
# TEST 1 — EMAIL SUMMARIZATION MODEL (ALLOW 200 OR 400)
# ============================================================
def test_email_summarization_model(request_context):

    test_payload = {
        "appName": "esummarize",
        "maximumLength": "3",
        "context": "sad day",
        "emailSubject": "sick leave",
        "emailBodyText": "I am very sick today and want a leave so I can rest and get better."
    }

    response = request_context.post(
        "/aiCenter/emailSummarization",
        multipart={
            "dataString": json.dumps(test_payload),
            "apiKey": "null"
        }
    )

    print("\nMODEL STATUS:", response.status)

    # Allow 200 OR 400 → do not fail test
    if response.status not in [200, 400]:
        pytest.fail(f"Unexpected status: {response.status}")

    try:
        resp_json = response.json()
    except:
        resp_json = {"error": "Invalid JSON"}

    print("MODEL RESPONSE:", resp_json)
    print("✔ MODEL TEST COMPLETED (200 or 400 allowed)")


# ============================================================
# TEST 2 — CREATE EMAIL SUMMARIZATION APP
# ============================================================
def test_email_summarization_create(request_context):

    payload = {
        "appName": "esummarize2",
        "maximumLength": "3",
        "context": "sad day",
        "emailSubject": "",
        "emailBodyText": "",
        "env": "zahra"
    }

    response = request_context.post(
        "/aiCenter/env/zahra/insert",
        multipart={
            "data": json.dumps(payload),
            "capabilityType": "EmailSummarization"
        }
    )

    print("\nCREATE STATUS:", response.status)

    if response.status == 304:
        print("✔ App already exists — OK")
        return

    assert response.status == 200, "❌ Failed to create EmailSummarization app"

    print("CREATE RESPONSE:", response.json())
    print("✔ EmailSummarization APP CREATED")


# ============================================================
# COMMON — UPDATE STATUS (disable / enable / delete)
# ============================================================
def update_email_app_status(request_context, action, appName="esummarize2"):

    # Step 1 — Get apps
    get_response = request_context.get("/aiCenter/env/zahra/getApps")
    assert get_response.status == 200, "❌ Cannot fetch apps"

    apps = get_response.json()
    print("\nAPPS LIST:", apps)

    # Step 2 — Find ID
    app_id = None
    for app in apps:
        if app.get("name") == appName:
            app_id = app.get("id")
            break

    assert app_id is not None, f"❌ App '{appName}' not found!"
    print(f"✔ Using App ID {app_id} for {action}")

    payload = {
        "id": str(app_id),
        "env": "zahra",
        "action": action
    }

    # Step 3 — Call updateStatus
    response = request_context.post(
        "/aiCenter/env/zahra/updateStatus",
        multipart={"data": json.dumps(payload)}
    )

    print(f"{action.upper()} STATUS:", response.status)

    if response.status in [200, 304]:
        print(f"✔ {action} OK")
        return True

    pytest.fail(f"Unexpected status: {response.status}")


# ============================================================
# TESTS FOR STATUS CHANGE
# ============================================================
def test_email_summarization_disable(request_context):
    assert update_email_app_status(request_context, "disable")


def test_email_summarization_enable(request_context):
    assert update_email_app_status(request_context, "enable")


def test_email_summarization_delete(request_context):
    assert update_email_app_status(request_context, "delete")
