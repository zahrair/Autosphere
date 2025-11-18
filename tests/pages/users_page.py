class UsersPage:
    def __init__(self, page):
        self.page = page
        self.logo = page.locator("#header-logo-img")
        self.sidebar_btn = page.locator("#header-sidebar-btn")
        self.users_option = page.locator("#users-sidebar-btn")  # update if needed
        # Buttons
        self.add_user_btn = page.locator("#superadmin-users-add-btn")
        self.create_btn = page.locator("#user-setting-create-user-create-btn")

        # Fields
        self.username_field = page.locator("#user-setting-create-user-username-field")
        self.fullname_field = page.locator("#user-setting-create-user-fullname-field")
        self.password_field = page.locator("#user-setting-create-user-password-field")
        self.confirm_password_field = page.locator("#user-setting-create-user-confirm-password-field")
        self.email_field = page.locator("#user-setting-create-user-email-field")

        # Dropdowns
        self.role_dropdown = page.locator("#user-setting-create-user-role-select")
        self.license_dropdown = page.locator("#user-setting-create-user-license-select")

        # Dropdown panels
        self.role_panel = page.locator(".mat-mdc-select-panel")
        self.license_panel = page.locator(".mat-mdc-select-panel")

    def click_logo(self):
        print("🔹 Clicking logo...")
        self.logo.click()

        print("⏳ Waiting for Environment page...")
        # URL must match actual! Yours is plural "environments"
        self.page.wait_for_url("**/environments", timeout=15000)
        print("✅ Landed on Environment page")

    def open_sidebar_and_go_to_users(self):
       print("🔹 Opening sidebar...")
       self.sidebar_btn.click()
   
       print("⏳ Waiting for Users menu item...")
       users_item = self.page.locator("#adminsidebar-users")

       users_item.wait_for(state="visible", timeout=10000)

       print("🔹 Clicking Users menu item...")
       users_item.click(force=True)

       print("⏳ Waiting for Users page...")
       self.page.wait_for_url("**/users", timeout=15000)
   
       print("✅ Successfully arrived on Users page!")
    
    
    