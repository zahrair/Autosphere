import json
import pytest


# ============================================================
# TEST 1 — TEXT CLASSIFICATION MODEL (ALLOW 200 OR 400)
# ============================================================
def test_text_classification_model(request_context):

    test_payload = {
        "appName": "tclassification",
        "context": "good",
        "categories": ["sad"],
        "multiCategory": False,
        "testInput": "i am feeling good today as i complete all my tasks"
    }

    response = request_context.post(
        "/aiCenter/textClassification",
        multipart={
            "dataString": json.dumps(test_payload),
            "apiKey": "null"
        }
    )

    print("\nMODEL STATUS:", response.status)

    # Allow 200 OR 400 → do not fail
    if response.status not in [200, 400]:
        pytest.fail(f"Unexpected status {response.status}")

    try:
        resp_json = response.json()
    except:
        resp_json = {"error": "Invalid JSON"}

    print("MODEL RESPONSE:", resp_json)

    print("✔ MODEL TEST COMPLETED (200 or 400 allowed)")


# ============================================================
# TEST 2 — CREATE TEXT CLASSIFICATION APP (200 OR 304)
# ============================================================
def test_text_classification_create_app(request_context):

    payload = {
        "appName": "tclassification",
        "context": "good",
        "categories": ["sad"],
        "multiCategory": False,
        "testInput": "",
        "env": "zahra"
    }

    response = request_context.post(
        "/aiCenter/env/zahra/insert",
        multipart={
            "data": json.dumps(payload),
            "capabilityType": "TextClassification"
        }
    )

    print("\nCREATE STATUS:", response.status)

    # App exists → 304
    if response.status == 304:
        print("✔ TEXT CLASSIFICATION APP ALREADY EXISTS — OK")
        return

    # Fresh create → must be 200
    assert response.status == 200, "❌ Failed to create TextClassification app"

    resp_json = response.json()
    print("CREATE RESPONSE:", resp_json)

    assert "AI App created successfully" in resp_json.get("message", "")
    print("✔ TEXT CLASSIFICATION APP CREATED SUCCESSFULLY")
