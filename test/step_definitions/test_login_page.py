from pytest_bdd import scenarios, given, when, then
from pages.login_page import LoginPage

# Link the feature file
scenarios('../features/login_page.feature')

@given("I open the login page")
def open_login_page(page):
    page.goto("http://172.18.36.58/#/")
    return LoginPage(page)

@then("I should see the Autosphere text")
def verify_autosphere_text(page):
    LoginPage(page).verify_autosphere_text()

@then("the Username and Password labels")
def verify_username_password_labels(page):
    LoginPage(page).verify_username_password_labels()

@then("the Login button")
def verify_login_button(page):
    LoginPage(page).verify_login_button()

@then("the Login card should be centered")
def verify_login_card_centered(page):
    LoginPage(page).verify_login_card_centered()

@when("I enter valid credentials")
def enter_valid_credentials(page):
    login = LoginPage(page)
    login.perform_login("superadmin", "Admin@1234")

@then("I should be logged into the dashboard")
def verify_dashboard(page):
    assert page.locator("#header-username").is_visible(), "❌ Dashboard not visible!"

@when("I enter invalid credentials")
def enter_invalid_credentials(page):
    login = LoginPage(page)
    login.perform_login("superadmin22", "Admin@1234")

@then("I should see a login error")
def verify_login_error(page):
    content = page.content()
    assert "Invalid" in content or "error" in content.lower(), "❌ No error message displayed for invalid login!"

@given("I am logged in")
def ensure_logged_in(page):
    page.goto("http://172.18.36.58/#/")
    login = LoginPage(page)
    login.perform_login("superadmin", "Admin@1234")

@when("I perform logout")
def perform_logout(page):
    LoginPage(page).perform_logout()

@then("I should be redirected back to the login page")
def verify_login_page(page):
    assert page.locator("button#login-submit-btn").is_visible(), "❌ Login page not visible after logout!"
