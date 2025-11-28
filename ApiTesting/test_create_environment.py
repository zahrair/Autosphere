from playwright.sync_api import sync_playwright
from api_client import APIClient
import random, string

BASE_URL = "http://172.30.2.94:8080"


# -----------------------------------------
# Helper – Get all environments (LIST API)
# -----------------------------------------
def get_environments(request_context):
    response = request_context.get("/user/environments")
    assert response.status == 200, f"Failed to get environments: {response.status}"
    return response.json()

def random_suffix(length=4):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

# -----------------------------------------
# TEST 1 — Create Environment
# -----------------------------------------
def test_create_environment():

    client = APIClient(BASE_URL)
    token = client.login("superadmin", "Admin@1234")
  # SAVE TO FILE so delete test can read it
    
    env_name = f"myenvironmenttest_{random_suffix()}"
    with open("created_env.txt", "w") as f:
        f.write(env_name)
    payload = {
        "name": env_name,
        "description": "",
        "licenses": ["7f9ea688-ed29-5564-c054-8a3a58af474c"]
    }

    with sync_playwright() as p:
        request_context = p.request.new_context(
            base_url=BASE_URL,
            extra_http_headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )

        # STEP 1 — Print existing environments BEFORE creation
        before_envs = get_environments(request_context)
        print("\n📌 ENVIRONMENTS BEFORE CREATE:")
        for env in before_envs:
            print(" •", env["name"])

        # STEP 2 — Create environment
        response = request_context.post("/environment/create", data=payload)

        print("\nSTATUS:", response.status)
        print("RESPONSE:", response.text())

        assert response.status == 200, f"Expected 200, got {response.status}"

        print("✅ Environment created successfully!")

        # STEP 3 — Print environments AFTER creation
        after_envs = get_environments(request_context)
        print("\n📌 ENVIRONMENTS AFTER CREATE:")
        for env in after_envs:
            print(" •", env["name"])


# -----------------------------------------
# TEST 2 — Delete Environment
# -----------------------------------------
def test_delete_environment():

    client = APIClient(BASE_URL)
    token = client.login("superadmin", "Admin@1234")

    # READ name generated in test 1
    with open("created_env.txt", "r") as f:
        env_to_delete = f.read().strip()

    with sync_playwright() as p:
        request_context = p.request.new_context(
            base_url=BASE_URL,
            extra_http_headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )

        # STEP 1 — Print existing environments BEFORE delete
        all_envs_before = get_environments(request_context)
        print("\n📌 ENVIRONMENTS BEFORE DELETE:")
        for env in all_envs_before:
            print(" •", env["name"])

        # ENV MUST EXIST
        assert env_to_delete in [env["name"] for env in all_envs_before], \
            f"❌ Environment {env_to_delete} not found!"

        print(f"\n🗑 Deleting Environment: {env_to_delete}")

        # STEP 3 — DELETE
        response = request_context.post(
            f"/environment/delete?environmentName={env_to_delete}",
            data="{}"
        )

        print("\nSTATUS:", response.status)
        print("RESPONSE:", response.text())

        assert response.status == 200, "❌ Delete failed!"

        print("✅ Environment deleted successfully!")

        # STEP 4 — After delete
        all_envs_after = get_environments(request_context)
        print("\n📌 ENVIRONMENTS AFTER DELETE:")
        for env in all_envs_after:
            print(" •", env["name"])
