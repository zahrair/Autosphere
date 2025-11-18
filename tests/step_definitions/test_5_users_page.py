from pytest_bdd import scenarios, given, when, then
from tests.pages.users_page import UsersPage

# Load the feature file
scenarios("../features/users_page.feature")


@given("I am on any page")
def any_page(page):
    print("ℹ️ Starting test from current page")
    return page


@when("I click the logo to return to the Environment page")
def click_logo(page):
    UsersPage(page).click_logo()


@when("I open the sidebar and go to the Users page")
def go_sidebar_users(page):
    UsersPage(page).open_sidebar_and_go_to_users()


@then("I should land on the Users page successfully")
def verify_users_page(page):
    assert "/users" in page.url, f"❌ Expected /users but got {page.url}"
    print("🎉 Users page loaded successfully!")
