import json
from playwright.sync_api import sync_playwright
from api_client import APIClient   # ← using your existing file

BASE_URL = "https://192.168.1.236:8080"


# ============================================================
# TEST 1 — TEXT SUMMARIZATION
# ============================================================
def test_text_summarization():
    client = APIClient(BASE_URL)
    token = client.login("superadmin", "Admin@1234")

    payload = {
        "appName": "tsummarize",
        "maximumLength": "3",
        "context": "beautiful day",
        "testInput": "today is a beautiful day with fresh air"
    }

    with sync_playwright() as p:
        request_context = p.request.new_context(
            base_url=BASE_URL,
            ignore_https_errors=True,
            extra_http_headers={"Authorization": f"Bearer {token}"}
        )

        response = request_context.post(
            "/aiCenter/textSummarization",
            multipart={
                "dataString": json.dumps(payload),
                "apiKey": "null"
            }
        )

        print("STATUS:", response.status)
        print("RESPONSE:", response.json())

        assert response.status == 200
        assert response.json()["status"] == 200


# ============================================================
# TEST 2 — INSERT AI APP
# ============================================================
def test_ai_app_insert():
    client = APIClient(BASE_URL)
    token = client.login("superadmin", "Admin@1234")

    payload = {
        "appName": "SummaryWorld",
        "maximumLength": "3",
        "context": "beautiful day",
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
                "data": json.dumps(payload),
                "capabilityType": "TextSummarization"
            }
        )

        print("INSERT STATUS:", response.status)

        if response.status == 304:
            print("✔ App already exists (304) — test passed.")
            assert True
            return

        if response.status == 200:
            resp_json = response.json()
            print("INSERT RESPONSE:", resp_json)

            if "already" in resp_json.get("message", "").lower():
                print("✔ App already exists — test passed.")
                assert True
                return

            if "AI App created successfully" in resp_json.get("message", ""):
                print("✔ App created successfully — test passed.")
                assert True
                return

            assert False, f"Unexpected 200 response: {resp_json}"

        assert False, f"Unexpected status code: {response.status}"


# ============================================================
# TEST 3 — UPDATE AI APP STATUS (DELETE)
# ============================================================
def update_app_status(action, appName="SummaryWorld"):
    client = APIClient(BASE_URL)
    token = client.login("superadmin", "Admin@1234")

    with sync_playwright() as p:
        request_context = p.request.new_context(
            base_url=BASE_URL,
            ignore_https_errors=True,
            extra_http_headers={"Authorization": f"Bearer {token}"}
        )

        get_response = request_context.get("/aiCenter/env/TrayRegression/getApps")
        assert get_response.status == 200, "getApps failed!"
        apps_list = get_response.json()

        found_id = None
        for app in apps_list:
            if app.get("name") == appName:
                found_id = app.get("id")
                break

        assert found_id is not None, f"❌ {appName} not found in getApps"

        print(f"✔ Found App ID: {found_id} for action: {action}")

        payload = {
            "id": str(found_id),
            "env": "TrayRegression",
            "action": action
        }

        response = request_context.post(
            "/aiCenter/env/TrayRegression/updateStatus",
            multipart={"data": json.dumps(payload)}
        )

        print(f"\n{action.upper()} STATUS:", response.status)

        if response.status == 304:
            print(f"✔ Already {action} — test passed.")
            return True

        if response.status == 200:
            resp_json = response.json()
            print(f"{action.upper()} RESPONSE:", resp_json)

            assert "success" in resp_json.get("message", "").lower()
            print(f"✔ App successfully {action}d.")
            return True

        assert False, f"Unexpected status code: {response.status}"

def test_ai_app_disable():
    assert update_app_status("disable") is True

def test_ai_app_enable():
    assert update_app_status("enable") is True

def test_ai_app_delete():
    assert update_app_status("delete") is True

def test_ai_app_edit():
    client = APIClient(BASE_URL)
    token = client.login("superadmin", "Admin@1234")

    appName = "tsummarize"  

    with sync_playwright() as p:
        request_context = p.request.new_context(
            base_url=BASE_URL,
            ignore_https_errors=True,
            extra_http_headers={"Authorization": f"Bearer {token}"}
        )

        list_resp = request_context.get("/aiCenter/env/TrayRegression/getApps")
        assert list_resp.status == 200, "getApps failed!"
        apps_list = list_resp.json()

        found_id = None
        for app in apps_list:
            if app.get("name") == appName:  
                found_id = app.get("id")
                break

        assert found_id is not None, f"❌ App '{appName}' not found!"
        print(f"✔ Editing App ID: {found_id}")

        payload = {
            "maximumLength": "3",
            "context": "nice day",     
            "testInput": "",
            "appName": appName,         
            "env": "TrayRegression"
        }

        update_url = f"/aiCenter/env/TrayRegression/update/{found_id}"

        response = request_context.post(
            update_url,
            multipart={"data": json.dumps(payload)}
        )

        print("\nUPDATE STATUS:", response.status)

        if response.status == 304:
            print("✔ Nothing to update — test passed.")
            assert True
            return

        if response.status == 200:
            resp_json = response.json()
            print("UPDATE RESPONSE:", resp_json)
            assert "successfully" in resp_json.get("message", "").lower()
            print("✔ App updated successfully.")
            return

        assert False, f"Unexpected status: {response.status}"
