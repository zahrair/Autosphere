import json
from playwright.sync_api import sync_playwright
from api_client import APIClient

BASE_URL = "http://172.25.235.110:8080/#/robots/"   # <-- keep without #/

def test_create_queue():

    client = APIClient(BASE_URL)
    token = client.login("superadmin", "Admin@1234")

    payload = {
        "queueName": "queue12333",
        "description": "",
        "MaxNoOfRetries": "0",
        "encrypted": "0",
        "AutoRetry": "0",
        "id": "",
        "sla": "0",
        "Hdays": "",
        "Hhours": "",
        "Hmints": "",
        "Mdays": "",
        "Mhours": "",
        "Mmints": "",
        "Ldays": "",
        "Lhours": "",
        "Lmints": "",
        "uniqueReference": "0",
        "reference": "0",
        "environment": "zahra"
    }

    with sync_playwright() as p:
        request_context = p.request.new_context(
            base_url=BASE_URL,
            extra_http_headers={"Authorization": f"Bearer {token}"}
        )

        response = request_context.post(
            "/queue/env/zahra/create",
            multipart={"data": json.dumps(payload)}
        )

        print("STATUS:", response.status)
        print("RAW TEXT:", response.text())
        print("HEADERS:", response.headers)
        print("REQUEST SENT:", json.dumps(payload, indent=2))

        assert response.status == 200
