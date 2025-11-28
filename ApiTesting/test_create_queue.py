import json
from playwright.sync_api import sync_playwright
from api_client import APIClient

BASE_URL = "http://172.30.2.94:8080"

def test_create_queue():

    client = APIClient(BASE_URL)
    token = client.login("superadmin", "Admin@1234")

    payload = {
        "queueName": "1qqqqqqqqqqqqqqqqqqqqq",
        "description": "",
        "MaxNoOfRetries": "0",
        "encrypted": 0,
        "id": "",
        "sla": 0,
        "Hdays": "",
        "Hhours": "",
        "Hmints": "",
        "Mdays": "",
        "Mhours": "",
        "Mmints": "",
        "Ldays": "",
        "Lhours": "",
        "Lmints": "",
        "uniqueReference": 0,
        "reference": 0,
        "environment": "zahra"
    }

    json_payload = json.dumps(payload)

    with sync_playwright() as p:
        request_context = p.request.new_context(
            base_url=BASE_URL,
            extra_http_headers={
                "Authorization": f"Bearer {token}"
                # IMPORTANT: Do NOT set Content-Type manually for form data
            }
        )

        response = request_context.post(
            "/queue/env/zahra/create",
            form={"data": json_payload}   # <-- THIS IS THE FIX
        )

        print("\nSTATUS:", response.status)
        print("RESPONSE:", response.json())

        assert response.status == 200, f"Queue creation failed! Status: {response.status}"
