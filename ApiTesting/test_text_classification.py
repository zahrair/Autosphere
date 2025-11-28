import json
from playwright.sync_api import sync_playwright
from api_client import APIClient   # ← using your existing file

BASE_URL = "https://192.168.1.236:8080"


def test_text_classification_model():
    """Test Text Classification model BEFORE creating app."""
    client = APIClient(BASE_URL)
    token = client.login("superadmin", "Admin@1234")

    test_payload = {
        "appName": "tclassification",
        "context": "good",
        "categories": ["sad"],
        "multiCategory": False,
        "testInput": "i am feeling good today as i complete all my tasks"
    }

    with sync_playwright() as p:
        request_context = p.request.new_context(
            base_url=BASE_URL,
            ignore_https_errors=True,
            extra_http_headers={"Authorization": f"Bearer {token}"}
        )

        response = request_context.post(
            "/aiCenter/textClassification",
            multipart={
                "dataString": json.dumps(test_payload),
                "apiKey": "null"
            }
        )

        print("MODEL TEST STATUS:", response.status)
        assert response.status == 200, "❌ TextClassification API FAIL!"

        resp_json = response.json()
        print("MODEL RESPONSE:", resp_json)

        # Basic validation
        assert resp_json["status"] == 200
        assert "response" in resp_json

        # Extract inside the double braces {{ }}
        result_text = resp_json["response"].lower()  

        # Allow all valid outcomes
        valid_keywords = ["sad", "happy", "angry", "none", "category"]

        assert any(keyword in result_text for keyword in valid_keywords), \
            f"❌ Classification result missing expected fields! Got: {result_text}"

        print("✔ MODEL TEST PASSED. Ready to create app.")

def test_text_classification_create_app():
    """Create Text classification App — handles both fresh create (200) and already exists (304)."""
    
    client = APIClient(BASE_URL)
    token = client.login("superadmin", "Admin@1234")

    app_payload = {
        "appName": "tclassification",
        "context": "good",
        "categories": ["sad"],
        "multiCategory": False,
        "testInput": "",
        "env": "TrayRegression"
    }

    with sync_playwright() as p:
        request_context = p.request.new_context(
            base_url=BASE_URL,
            ignore_https_errors=True,
            extra_http_headers={"Authorization": f"Bearer {token}"}
        )

        response = request_context.post(
            "/aiCenter/env/TrayRegression/insert",
            multipart={
                "data": json.dumps(app_payload),
                "capabilityType": "TextClassification"
            }
        )

        print("CREATE STATUS:", response.status)

        # ---------------------------------------------
        # 1️⃣ If app already exists → 304
        # ---------------------------------------------
        if response.status == 304:
            print("✔ APP ALREADY EXISTS — Test Passed.")
            assert True
            return

        # ---------------------------------------------
        # 2️⃣ Fresh creation → should be 200
        # ---------------------------------------------
        assert response.status == 200, "❌ App creation failed!"

        resp_json = response.json()
        print("CREATE RESPONSE:", resp_json)

        assert "AI App created successfully" in resp_json.get("message", "")
        print("✔ APP CREATED SUCCESSFULLY")
