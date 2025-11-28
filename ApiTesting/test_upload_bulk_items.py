import json
from playwright.sync_api import sync_playwright
from api_client import APIClient

BASE_URL = "http://172.30.2.94:8080"

def test_upload_bulk_items():

    client = APIClient(BASE_URL)
    token = client.login("superadmin", "Admin@1234")

    data_json = json.dumps({
        "queueName": "1qqqqqqqqqqqqqqqqqqqqq",
        "environment": "zahra",
        "priority": "Medium",
        "referenceColumnName": ""
    })

    file_path = r"D:\Autosphere\TestCases_Autosphere\Autosphere_bdd\ApiTesting\sample_bulk_upload.csv"

    with sync_playwright() as p:
        request_context = p.request.new_context(
            base_url=BASE_URL,
            extra_http_headers={
                "Authorization": f"Bearer {token}"
            }
        )

        response = request_context.post(
            "/queue/item/uploadbulkitems",
            multipart={
                "file": open(file_path, "rb"),
                "data": data_json
            }
        )

        print("\nSTATUS:", response.status)
        print("RESPONSE:", response.json())

        assert response.status == 200, f"Bulk upload failed: {response.status}"
