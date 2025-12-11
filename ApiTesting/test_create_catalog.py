import pytest
from playwright.sync_api import sync_playwright
from api_client import APIClient

# IMPORTANT: API BASE URL SHOULD NOT CONTAIN /#/
BASE_URL = "https://192.168.1.236:8080"


# ---------------------------------------------------------
# CREATE CATALOG API
# ---------------------------------------------------------
def create_catalog(request_context, payload):
    """Creates a new catalog in the given environment."""
    return request_context.post(
        f"/env/{payload['environment']}/catalog/add",
        data={
            "name": payload["name"],
            "environment": payload["environment"],
            "description": payload["description"],
            "user": payload["user"]
        }
    )


# ---------------------------------------------------------
# EDIT CATALOG API
# ---------------------------------------------------------
def edit_catalog(request_context, payload):
    """
    Updates an existing catalog.
    payload requires:
        id (int),
        name (str),
        description (str),
        environment (str)
    """
    return request_context.post(
        f"/env/{payload['environment']}/catalog/edit",
        data={
            "id": payload["id"],
            "name": payload["name"],
            "description": payload["description"]
        }
    )
def delete_catalog(request_context, catalog_id, environment):
    """
    Deletes a catalog by sending a JSON number (not string, not object).
    Content-Type MUST be application/json.
    """
    return request_context.post(
        f"/env/{environment}/catalog/delete",
        data=str(catalog_id),                  # JSON number
        headers={"Content-Type": "application/json"}
    )


# ---------------------------------------------------------
# TEST: CREATE CATALOG
# ---------------------------------------------------------
def test_create_catalog():

    payload = {
        "name": "catalog55",
        "environment": "zahra",
        "description": "",
        "user": "superadmin"
    }

    print("\n🔍 TEST: Create Catalog")

    # Login and get token
    client = APIClient(BASE_URL)
    token = client.login("superadmin", "Admin@1234")

    with sync_playwright() as p:
        request_context = p.request.new_context(
            base_url=BASE_URL,
            ignore_https_errors=True,  # Fix for self-signed SSL
            extra_http_headers={
                "Authorization": f"Bearer {token}"
            }
        )

        # ----------------------
        # CREATE CATALOG
        # ----------------------
        response = create_catalog(request_context, payload)

        print("STATUS:", response.status)
        print("RESPONSE:", response.text())

        assert response.status == 200, "❌ Catalog creation failed!"
        print("✅ Catalog created successfully")


# ---------------------------------------------------------
# TEST: EDIT CATALOG
# ---------------------------------------------------------
def test_edit_catalog():

    # NOTE: You can change ID, name, description as needed
    payload = {
        "id": 32,                         # Catalog ID taken from UI
        "name": "catalog50",              # New updated name
        "description": "qwertyu",         # New updated description
        "environment": "zahra"
    }

    print("\n🔍 TEST: Edit Catalog")

    # Login and get token
    client = APIClient(BASE_URL)
    token = client.login("superadmin", "Admin@1234")

    with sync_playwright() as p:
        request_context = p.request.new_context(
            base_url=BASE_URL,
            ignore_https_errors=True,  # Fix for SSL
            extra_http_headers={
                "Authorization": f"Bearer {token}"
            }
        )

        # ----------------------
        # EDIT CATALOG
        # ----------------------
        response = edit_catalog(request_context, payload)

        print("STATUS:", response.status)
        print("RESPONSE:", response.text())

        assert response.status == 200, "❌ Catalog update failed!"
        print("✅ Catalog updated successfully")
def test_delete_catalog():

    catalog_id = 32
    environment = "zahra"

    print(f"\n🔍 TEST: Delete Catalog ID = {catalog_id}")

    client = APIClient(BASE_URL)
    token = client.login("superadmin", "Admin@1234")

    with sync_playwright() as p:
        request_context = p.request.new_context(
            base_url=BASE_URL,
            ignore_https_errors=True,
            extra_http_headers={"Authorization": f"Bearer {token}"}
        )

        response = delete_catalog(request_context, catalog_id, environment)

        print("STATUS:", response.status)
        print("RESPONSE:", response.text())

        assert response.status == 200, "❌ Catalog deletion failed!"
        print("✅ Catalog deleted successfully")
