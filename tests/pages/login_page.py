from playwright.sync_api import Page

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.login_card = page.locator("mat-card.mat-mdc-card")  

    def verify_autosphere_text(self):
        content = self.page.content()
        assert "Autosphere" in content, "❌ 'Autosphere' text NOT found on Login Page!"
        print("✅ [Login Page] 'Autosphere' text found!")

    def verify_username_password_labels(self):
        username_label = self.page.locator("#login-username-label")
        password_label = self.page.locator("#login-password-label")

        assert username_label.is_visible(), "❌ Username label not visible"
        assert password_label.is_visible(), "❌ Password label not visible"

        print("✅ [Login Page] Username and Password labels are visible!")

    def verify_login_button(self):
        login_button = self.page.locator("#login-submit-btn").first
        assert login_button.first.is_visible(), "❌ Login button is NOT visible!"
        print("✅ [Login Page] Login button is visible!")
     
    def perform_login(self, username, password):
         print("🔹 Performing login and verifying user...")

         username_field = self.page.locator("#login-username-field")
         password_field = self.page.locator("#login-password-field")
         login_button = self.page.locator("button#login-submit-btn")
         
         

         username_field.fill(username)
         password_field.fill(password)
         login_button.click()
         assert login_button.is_disabled(), "❌ Login button did NOT disable during processing!"
         print("✅ [Login Page] Login button disabled during processing.")
         self.page.wait_for_load_state("networkidle")

         header_username = self.page.locator("#header-username")
         header_username.wait_for(state="visible", timeout=5000)

         displayed_user = header_username.inner_text().strip()
         print(f" Logged in user detected: {displayed_user}")
        
         
         
         assert displayed_user.lower() == username.lower(), (
         f"❌ Login verification failed! Expected '{username}', got '{displayed_user}'"
      )

         print(f"✅ Login successful. User '{displayed_user}' verified in header!")