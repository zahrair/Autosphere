from pytest_bdd import scenarios, given, when, then
from tests.pages.login_page import LoginPage

# Link the feature file
scenarios('../features/login_page.feature')

@given("I am on the login page")
def open_login_page(page):
    # It will automatically open the default URL from conftest.py
    return LoginPage(page)

@when("I enter valid login credentials")
def enter_valid_login(page):
    login = LoginPage(page)
    username = "superadmin"
    password = "Admin@1234"
    login.perform_login(username, password)

@then("I should see my username displayed on the dashboard")
def verify_dashboard(page):
    header_username = page.locator("#header-username")
    header_username.wait_for(state="visible", timeout=10000)
    assert header_username.is_visible(), "❌ Username not visible after login!"
    print("✅ Login successful — username visible on dashboard.")
