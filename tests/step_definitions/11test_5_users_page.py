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


@given("I am on the Users page")
def open_users_page(page):
    # Assumes you're already logged in and sidebar flows exist
    page.goto("http://172.24.67.254:8080/#/users")  
    page.wait_for_timeout(1500)


@when("I click Add User button")
def click_add_user(page):
    UsersPage(page).click_add_user()


@when("I fill in all user fields")
def fill_fields(page):
    user = UsersPage(page)
    user.fill_user_fields(
        uname="user12",
        fname="User Twelve",
        pwd="Admin@12345",
        email="user12@test.com"
    )


@when("I select the first role from dropdown")
def choose_role(page):
    UsersPage(page).select_first_role()


@when("I select the first license from dropdown")
def choose_license(page):
    UsersPage(page).select_first_license()


@when("I click Create User")
def click_create(page):
    UsersPage(page).create_user()


@when('I open the action menu for "User Twelve"')
def open_menu(page):
    UsersPage(page).open_user_action_menu("User Twelve")


@when('I click delete for "User Twelve"')
def click_delete(page):
    UsersPage(page).click_delete_user("User Twelve")


@when("I confirm user deletion")
def confirm_delete(page):
    UsersPage(page).confirm_delete()


@then('the user "User Twelve" should not be listed')
def verify_deleted(page):
    UsersPage(page).verify_user_not_in_table("User Twelve")


@when('I open the action menu for "User Test"')
def open_menu_edit(page):
    UsersPage(page).open_user_action_menu("User Test")

@when("I click the edit button")
def click_edit(page):
    UsersPage(page).click_edit_user()


@when('I update the user\'s name to "User Test Updated"')
def update_name(page):
    UsersPage(page).update_user_fullname("User Test Updated")

@when('I update the user\'s password to "newPass123"')
def update_password(page):
    UsersPage(page).update_user_password("newPass@123")
    
@when("I save the updated user")
def save_update(page):
    UsersPage(page).save_user_updates()


@then('I should see the updated name "User Test Updated" in the users list')
def verify_update(page):
    UsersPage(page).verify_user_in_table("User Test Updated")