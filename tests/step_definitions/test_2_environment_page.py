from pytest_bdd import scenarios, when, then
from tests.pages.environment_page import EnvironmentPage

# Link feature file
scenarios('../features/environment_page.feature')

@when("I open my environment card")
def open_environment_card(page):
    env = EnvironmentPage(page)
    env.open_environment_and_verify_user()

@then('I should see my username "zahra" displayed on the page')
def verify_username_display(page):
    user_label = page.locator("span.mdc-button__label").first
    user_label.wait_for(state="visible", timeout=10000)
    text = user_label.inner_text().strip()
    assert "zahra" in text.lower(), f"❌ Expected 'zahra' but found '{text}'"
    print("✅ Username 'zahra' is correctly displayed in environment.")
