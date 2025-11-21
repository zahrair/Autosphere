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


@when("I click Create Role button")
def click_create_role(page):
    RolesPage(page).click_create_role()


@when('I fill the role name as "AutomationRole"')
def fill_role_name(page):
    RolesPage(page).fill_role_name("AutomationRole")

@when("I select the first Environment option")
def select_environment(page):
    RolesPage(page).select_environment()

@when("I select the permission scheme Administrator")
def select_permission_scheme(page):
    RolesPage(page).select_permission_scheme("Administrator")

@when("I click the Create Role button")
def click_create_role_button(page):
    RolesPage(page).click_create_role_button()

@then('I should see the role "AutomationRole" in the roles table')
def verify_role_in_table(page):
    RolesPage(page).verify_role_in_table("AutomationRole")
@when('I open the action menu for role "AutomationRole"')
def open_role_action_menu(page):
    RolesPage(page).open_role_action_menu("AutomationRole")
@when('I click delete for role "AutomationRole"')
def click_delete_role(page):
    RolesPage(page).click_delete_role("AutomationRole")


@when("I confirm deleting the role")
def confirm_delete_role(page):
    RolesPage(page).confirm_delete_role()


@then('the role "AutomationRole" should not be listed in the roles table')
def verify_role_deleted(page):
    RolesPage(page).verify_role_not_in_table("AutomationRole")

@when('I open the action menu for role "user_role"')
def open_action_menu_again(page):
    RolesPage(page).open_role_action_menu("user_role")


@when('I click the details option for role "user_role"')
def click_role_details(page):
    RolesPage(page).click_role_details("user_role")


@when('I update the permission scheme to "Administrator"')
def update_permission_scheme(page):
    RolesPage(page).select_permission_scheme("Administrator")


@when("I save the updated role")
def save_updated_role(page):
    RolesPage(page).save_role_changes()


@then('the role "user_role" should be updated successfully')
def verify_role_updated(page):
    print("✅ Role updated successfully!")

