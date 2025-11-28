import json
from playwright.sync_api import sync_playwright
from api_client import APIClient

BASE_URL = "https://192.168.1.236:8080"


# ---------------------------------------------------------
# 1️⃣ TEST THE TEXT CHARACTERIZATION MODEL
# ---------------------------------------------------------

def test_text_characterization_model():
    """Test Text Characterization model BEFORE creating app."""
    client = APIClient(BASE_URL)
    token = client.login("superadmin", "Admin@1234")

    test_payload = {
        "appName": "tcharacterize",
        "context": "felling low",
        "analysisRequired": {
            "sentiment": True,
            "profanity": True,
            "emotion": True,
            "sarcasm": True,
            "grammar": True,
            "gibberish": True,
            "toxicity": True
        },
        "testInput": "i am felling low today because I had too much work"
    }

    with sync_playwright() as p:
        request_context = p.request.new_context(
            base_url=BASE_URL,
            ignore_https_errors=True,
            extra_http_headers={"Authorization": f"Bearer {token}"}
        )

        response = request_context.post(
            "/aiCenter/textCharacterization",
            multipart={
                "dataString": json.dumps(test_payload),
                "apiKey": "null"
            }
        )

        print("MODEL TEST STATUS:", response.status)
        assert response.status == 200, "❌ TextCharacterization API FAIL!"

        resp_json = response.json()
        print("MODEL RESPONSE:", resp_json)

        # Basic validation
        assert resp_json["status"] == 200
        assert "response" in resp_json
        assert "sentiment" in resp_json["response"].lower()

        print("✔ MODEL TEST PASSED. Ready to create app.")


# ---------------------------------------------------------
# 2️⃣ CREATE THE APP ONLY IF MODEL TEST PASSED
# ---------------------------------------------------------

def test_text_characterization_create_app():
    """Create Text Characterization App — handles both fresh create (200) and already exists (304)."""
    
    client = APIClient(BASE_URL)
    token = client.login("superadmin", "Admin@1234")

    app_payload = {
        "appName": "tcharacterize2",
        "context": "felling low",
        "analysisRequired": {
            "sentiment": True,
            "profanity": True,
            "emotion": True,
            "sarcasm": True,
            "grammar": True,
            "gibberish": True,
            "toxicity": True
        },
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
                "capabilityType": "TextCharacterization"
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
