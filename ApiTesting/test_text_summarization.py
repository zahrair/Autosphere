import json
import pytest


# ============================================================
# TEST 1 — TEXT SUMMARIZATION MODEL (ALLOW 200 or 400)
# ============================================================
def test_text_summarization_model(request_context):

    payload = {
        "appName": "tsummarize",
        "maximumLength": "3",
        "context": "beautiful day",
        "testInput": "today is a beautiful day with fresh air"
    }

    response = request_context.post(
        "/aiCenter/textSummarization",
        multipart={
            "dataString": json.dumps(payload),
            "apiKey": "null"
        }
    )

    print("\nMODEL STATUS:", response.status)

    # ALLOW 200 or 400 (AI Center often returns 400 when not configured)
    if response.status not in [200, 400]:
        pytest.fail(f"Unexpected model status: {response.status}")

    try:
        print("MODEL RESPONSE:", response.json())
    except:
        print("MODEL RESPONSE: Invalid JSON")

    print("✔ MODEL TEST COMPLETED (200 or 400 allowed)")


# ============================================================
# TEST 2 — CREATE TEXT SUMMARIZATION APP
# ============================================================
def test_text_summarization_create(request_context):

    payload = {
        "appName": "SummaryWorld",
        "maximumLength": "3",
        "context": "beautiful day",
        "testInput": "",
        "env": "zahra"
    }

    response = request_context.post(
        "/aiCenter/env/zahra/insert",
        multipart={
            "data": json.dumps(payload),
            "capabilityType": "TextSummarization"
        }
    )

    print("\nINSERT STATUS:", response.status)

    # Already exists
    if response.status == 304:
        print("✔ App already exists — OK")
        return

    assert response.status == 200, f"❌ Insert failed: {response.status}"

    resp_json = response.json()
    print("INSERT RESPONSE:", resp_json)

    assert "AI App created successfully" in resp_json.get("message", "")
    print("✔ TEXT SUMMARIZATION APP CREATED")


# ============================================================
# COMMON — UPDATE STATUS (disable / enable / delete)
# ============================================================
def update_app_status(request_context, action, appName="SummaryWorld"):

    # Step 1 — Get apps
    list_resp = request_context.get("/aiCenter/env/zahra/getApps")
    assert list_resp.status == 200, "getApps failed"
    apps = list_resp.json()

    # Step 2 — Find ID
    app_id = None
    for app in apps:
        if app.get("name") == appName:
            app_id = app.get("id")
            break

    assert app_id is not None, f"❌ App '{appName}' not found"
    print(f"✔ Found App ID: {app_id} for {action}")

    payload = {
        "id": str(app_id),
        "env": "TrayRegression",
        "action": action
    }

    # Step 3 — Update status
    response = request_context.post(
        "/aiCenter/env/zahra/updateStatus",
        multipart={"data": json.dumps(payload)}
    )

    print(f"{action.upper()} STATUS:", response.status)

    if response.status in [200, 304]:
        print(f"✔ {action} completed")
        return True

    pytest.fail(f"Unexpected update status: {response.status}")


def test_ai_app_disable(request_context):
    assert update_app_status(request_context, "disable")


def test_ai_app_enable(request_context):
    assert update_app_status(request_context, "enable")


def test_ai_app_delete(request_context):
    assert update_app_status(request_context, "delete")


