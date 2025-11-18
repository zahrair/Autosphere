from playwright.sync_api import Page

class EnvironmentPage:
    def __init__(self, page: Page):
        self.page = page
        self.env_card = page.locator("#environment-zahra-card")
        self.user_label = page.locator("span.mdc-button__label")

    def open_environment_and_verify_user(self):
        print("Opening environment card and verifying user label...")
        self.env_card.wait_for(state="visible", timeout=10000)
        self.env_card.click()
        print(" Environment card clicked!")
        self.page.wait_for_load_state("networkidle", timeout=10000)

       
