from pytest_bdd import scenarios, given, when, then
from tests.pages.roles_page import RolesPage
from tests.pages.users_page import UsersPage

# Load feature file
scenarios("../features/roles_page.feature")


@given("I am on any page")
def any_page(page):
    print("ℹ️ Starting test from current page")
    return page


@when("I click the logo to return to the Environment page")
def click_logo(page):
    UsersPage(page).click_logo()


@when("I click the Roles tab from the sidebar")
def go_to_roles(page):
    RolesPage(page).open_sidebar_and_go_to_roles()


@then("I should be navigated to the Roles page")
def verify_roles(page):
    assert "/roles" in page.url.lower(), f"❌ Expected /roles but got {page.url}"
    print("🎉 Roles page loaded successfully!")



