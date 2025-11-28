import json
from playwright.sync_api import sync_playwright

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def login(self, username, password):
        """Login and return token"""
        with sync_playwright() as p:
            request_context = p.request.new_context(
                base_url=self.base_url,
                ignore_https_errors=True,
                extra_http_headers={
                    "Content-Type": "application/json"
                }
            )

            # Convert payload to JSON string manually
            payload = json.dumps({
                "username": username,
                "password": password
            })

            response = request_context.post(
                "/api/auth/login",
                data=payload    # <-- FIXED ✔
            )


            assert response.status == 200, f"Login failed: {response.status}"
            json_data = response.json()

            assert "token" in json_data, "Token missing in login response!"
            print("🔑 Logged in successfully. Token received.")

            return json_data["token"]
def test_ai_app_update_status():
    client = APIClient(BASE_URL)
    token = client.login("superadmin", "Admin@1234")

    payload = {
        "id": "37",
        "env": "TrayRegression",
        "action": "delete"
    }

    with sync_playwright() as p:
        request_context = p.request.new_context(
            base_url=BASE_URL,
            ignore_https_errors=True,
            extra_http_headers={"Authorization": f"Bearer {token}"}
        )

        response = request_context.post(
            "/aiCenter/env/TrayRegression/updateStatus",
            multipart={
                "data": json.dumps(payload)
            }
        )

        print("\nUPDATE STATUS:", response.status)

        # 304 means already updated / no change
        if response.status == 304:
            print("✔ Status already updated — test passed.")
            assert True
            return

        # If 200, we expect JSON message
        if response.status == 200:
            resp_json = response.json()
            print("UPDATE RESPONSE:", resp_json)

            if "AI App status updated successfully" in resp_json.get("message", ""):
                print("✔ Status updated successfully — test passed.")
                assert True
                return

            assert False, f"Unexpected 200 response: {resp_json}"

        # Anything else = FAIL
        assert False, f"Unexpected status code: {response.status}"
