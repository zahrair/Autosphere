import json
import os
from playwright.sync_api import sync_playwright
from api_client import APIClient

BASE_URL = "http://172.24.186.84:8080"
# Path to image inside same folder as test file
IMAGE_PATH = os.path.join(os.path.dirname(__file__), "image.png")


def test_image_analysis_model():
    """Test Image Analysis model — must follow same style as EmailClassification test."""

    client = APIClient(BASE_URL)
    token = client.login("superadmin", "Admin@1234")
    print("🔑 Logged in successfully. Token received.")

    payload = {
        "appName": "ianalyze",
        "context": "cute image",
        "QueryQuestionField": "what is this?",
        "uploadImage": {},
        "testInput": "cute little puppy"
    }

    with sync_playwright() as p:
        request_context = p.request.new_context(
            base_url=BASE_URL,
            ignore_https_errors=True,
            extra_http_headers={"Authorization": f"Bearer {token}"}
        )

        response = request_context.post(
            "/aiCenter/imageAnalysis",
            multipart={
                "dataString": json.dumps(payload),
                "apiKey": "null",
                "testImage": open(IMAGE_PATH, "rb")   # image file
            }
        )

        status_code = response.status

        # Try JSON
        try:
            resp_json = response.json()
        except:
            resp_json = {"error": "Non-JSON response from server"}

        print("MODEL TEST STATUS:", status_code)

        # ------------------------------------
        # 🟢 CASE 1 — EXPECTED 200 SUCCESS
        # ------------------------------------
        if status_code == 200:
            print("🟢 SUCCESS RESPONSE:")
            print(resp_json)
            assert True
            return

        # ------------------------------------
        # 🔴 CASE 2 — FAILURE → SHOW ERROR
        # ------------------------------------
        print("🔴 FAILURE RESPONSE:")
        print(resp_json)

        assert False, f"❌ Expected 200 OK but got {status_code}. Response: {resp_json}"



# ============================================================
# 2️⃣ TEST — IMAGE ANALYSIS APP CREATE
# ============================================================
def test_image_analysis_create_app():

    client = APIClient(BASE_URL)
    token = client.login("superadmin", "Admin@1234")

    app_payload = {
        "appName": "ianalyze",
        "context": "cute image",
        "QueryQuestionField": "what is this?",
        "uploadImage": "",
        "testInput": "",
        "env": "zahra"
    }

    with sync_playwright() as p:

        request_context = p.request.new_context(
            base_url=BASE_URL,
            ignore_https_errors=True,
            extra_http_headers={"Authorization": f"Bearer {token}"}
        )

        # Create app
        response = request_context.post(
            "/aiCenter/env/zahra/insert",
            multipart={
                "data": json.dumps(app_payload),
                "capabilityType": "ImageAnalysis"
            }
        )

        print("CREATE STATUS:", response.status)

        # 304 → already exists
        if response.status == 304:
            print("✔ APP ALREADY EXISTS — Test Passed.")
            return

        assert response.status == 200, "❌ App creation failed!"

        resp_json = response.json()
        print("CREATE RESPONSE:", resp_json)

        assert "AI App created successfully" in resp_json["message"]
        print("✔ IMAGE ANALYSIS APP CREATED SUCCESSFULLY")
