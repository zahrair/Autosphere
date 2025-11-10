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
        login_button = self.page.locator("#login-submit-btn")
        assert login_button.first.is_visible(), "❌ Login button is NOT visible!"
        print("✅ [Login Page] Login button is visible!")
     
    def verify_login_card_centered(self):
        box = self.login_card.bounding_box()
        viewport = self.page.viewport_size
        login_button = self.page.locator("#login-submit-btn")
        button_box = login_button.bounding_box()

        page_center_x = viewport['width'] / 2
        element_center_x = box['x'] + box['width'] / 2
        diff_x = abs(page_center_x - element_center_x)

        page_center_y = viewport['height'] / 2
        element_center_y = box['y'] + box['height'] / 2
        diff_y = abs(page_center_y - element_center_y)

        assert diff_x < 1, f"❌ Login card not centered horizontally"
        assert diff_y < 1, f"❌ Login card not centered vertically"
        
        button_center_x = button_box['x'] + button_box['width'] / 2
        horizontal_diff = abs(button_center_x - element_center_x )

        distance_from_bottom = (element_center_x ['y'] + element_center_x ['height']) - (button_box['y'] + button_box['height'])
        vertical_ratio = distance_from_bottom / element_center_x ['height']

        assert horizontal_diff < 3, f"❌ Login button not centered horizontally in the card (diff: {horizontal_diff})"
        assert 0.05 < vertical_ratio < 0.25, f"❌ Login button not positioned near the bottom of the card (ratio: {vertical_ratio:.2f})"

        print("✅ [Layout] Login button is properly centered and positioned near bottom of the card.")

        
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
         
    def perform_logout(self):
      print("🔹 Attempting to log out...")

      username_button = self.page.locator("#header-username-btn")
      username_button.wait_for(state="visible", timeout=5000)
      username_button.click()

      self.page.wait_for_selector(".cdk-overlay-pane", timeout=5000)

      logout_button = self.page.locator("#header-logout-menuitem")
      logout_button.wait_for(state="visible", timeout=5000)
      logout_button.click()


      self.page.wait_for_load_state("networkidle")
      self.page.wait_for_selector("#login-submit-btn", timeout=8000)
  
      assert self.page.locator("button#login-submit-btn").is_visible(), "❌ Logout failed — login button not visible again!"
