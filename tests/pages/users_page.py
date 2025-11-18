class UsersPage:
    def __init__(self, page):
        self.page = page
        self.logo = page.locator("#header-logo-img")
        self.sidebar_btn = page.locator("#header-sidebar-btn")
        self.users_option = page.locator("#users-sidebar-btn")  # update if needed
        # Buttons
        self.add_user_btn = page.locator("#superadmin-users-add-btn")
        self.create_user_btn = page.locator("#user-setting-create-user-create-btn")

        # Fields
        self.username = page.locator("#user-setting-create-user-username-field")
        self.fullname = page.locator("#user-setting-create-user-fullname-field")
        self.password = page.locator("#user-setting-create-user-password-field")
        self.confirm_password = page.locator("#user-setting-create-user-confirm-password-field")
        self.email = page.locator("#user-setting-create-user-email-field")

        self.save_btn = page.locator("#user-setting-create-user-accept-btn")

        # Dropdowns
        self.role_dropdown = page.locator("#user-setting-create-user-role-select")
        self.license_dropdown = page.locator("#user-setting-create-user-license-select")

        # Generic dropdown panel
        self.dropdown_panel = page.locator(".mat-mdc-select-panel")

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
    
    # -------------------------------
    # CLICK ADD USER BUTTON
    # -------------------------------
    def click_add_user(self):
        print("🔹 Clicking Add User button...")
        self.add_user_btn.wait_for(state="visible", timeout=10000)
        self.add_user_btn.click()
        print("✅ Add User popup opened.")

    # -------------------------------
    # FILL FIELDS
    # -------------------------------
    def fill_user_fields(self, uname, fname, pwd, email):
        print("🔹 Filling Create User form...")

        self.username.fill(uname)
        self.fullname.fill(fname)
        self.password.fill(pwd)
        self.confirm_password.fill(pwd)
        self.email.fill(email)

        print("✅ All fields filled.")

    # -------------------------------
    # ROLE DROPDOWN → SHOW OPTIONS → SELECT FIRST
    # -------------------------------
    def select_first_role(self):
        print("🔹 Opening Role dropdown...")
        self.role_dropdown.click()

        # Wait for overlay to be visible
        self.page.wait_for_selector(".mat-mdc-select-panel", timeout=5000)

        options = self.page.locator(".mat-mdc-option")
        count = options.count()

        print(f"📌 Found {count} role options:")
        for i in range(count):
            print("   ➜", options.nth(i).inner_text())
    
        if count == 0:
            raise Exception("❌ No role options found!")

        # Select first option
        options.nth(0).click()

    # 🔥 Close overlay properly
        self.page.keyboard.press("Escape")
        self.page.wait_for_timeout(500)

        print("✅ Role selected.")
    
    def select_first_license(self):
      print("🔹 Opening Taskhub License dropdown...")
      self.license_dropdown.click()
  
      # Wait for dropdown panel
      panel = self.page.locator(".mat-mdc-select-panel")
      panel.wait_for(state="visible", timeout=5000)
  
      # Get options
      options = self.page.locator(".mat-mdc-option")
      count = options.count()

      print(f"📌 Found {count} license options:")
      for i in range(count):
          print("   ➜", options.nth(i).inner_text())

      if count == 0:
          raise Exception("❌ No license options found!")

      # Select first option
      print("🟡 Clicking first license option...")
      options.nth(0).click()

    # IMPORTANT:
    # Do NOT press Escape
    # Do NOT click outside
    # Just wait until Angular closes only the dropdown panel
      panel.wait_for(state="hidden", timeout=5000)

      print("🟢 Dropdown closed normally (Angular handled it) — popup still open.")
      self.page.wait_for_timeout(300)

    
    def create_user(self):
      print("🔹 Clicking Create User button...")

      # Always re-locate the button (simple fix!)
      create_btn = self.page.locator("#user-setting-create-user-accept-btn").first

      # Wait for button to be visible
      create_btn.wait_for(state="visible", timeout=5000)

      # Simple reliable click
      create_btn.click()

      print("🎉 User creation triggered!")
    

    def open_user_action_menu(self, username):
        print(f"🔹 Opening action menu for '{username}'...")
        safe_name = username.replace(" ", "\\ ")  # escape spaces for CSS selector

        btn = self.page.locator(f"#superadmin-users-{safe_name}-action-btn")
        btn.wait_for(state="visible", timeout=8000)
        btn.click()
        print("🟢 Action menu opened.")

    def click_delete_user(self, username):
        print(f"🔹 Clicking delete for '{username}'...")
        safe_name = username.replace(" ", "\\ ")

        delete_btn = self.page.locator(f"#superadmin-users-{safe_name}-delete-btn")
        delete_btn.wait_for(state="visible", timeout=8000)
        delete_btn.click()
        print("🟢 Delete clicked.")

    def confirm_delete(self):
        print("🔹 Confirming delete...")
        confirm = self.page.locator("#delete-accept-btn").first
        confirm.wait_for(state="visible", timeout=8000)
        confirm.click()

        print("🟢 Delete confirmed.")

    def verify_user_not_in_table(self, username):
        print(f"🔍 Checking that '{username}' is deleted...")
        self.page.wait_for_timeout(8000)

        table = self.page.locator("table").inner_text().lower()
        assert username.lower() not in table, f"❌ User '{username}' still present!"
        print(f"✅ User '{username}' successfully deleted.")
    
    def open_user_action_menu(self, username):
      print(f"🔹 Opening action menu for {username}")
      row = self.page.locator("tr", has_text=username)
      row.wait_for(state="visible", timeout=8000)

      menu_btn = row.locator("button.mat-mdc-menu-trigger")
      menu_btn.wait_for(state="visible", timeout=8000)
      menu_btn.click()

      print("✅ Action menu opened.")
  
    def click_edit_user(self):
      print("✏️ Clicking Edit button...")
      edit_btn = self.page.get_by_role("menuitem", name="Edit")
      edit_btn.wait_for(state="visible", timeout=8000)
      edit_btn.click()
      print("✅ Edit popup opened.")
    
    def update_user_fullname(self, new_name):
     print(f"🔧 Updating Full Name to: {new_name}")

     fullname_field = self.page.locator("#user-setting-create-user-fullname-field")
     fullname_field.wait_for(state="visible", timeout=8000)
     fullname_field.fill("")
     fullname_field.fill(new_name)
     self.page.wait_for_timeout(8000)

     print("✅ Full name updated.")
     
    def update_user_password(self, new_password):
      print("🔧 Updating Password...")

      pwd_field = self.page.locator("#user-setting-create-user-password-field")
      cpwd_field = self.page.locator("#user-setting-create-user-confirm-password-field")

      pwd_field.wait_for(state="visible", timeout=8000)
      cpwd_field.wait_for(state="visible", timeout=8000)

      pwd_field.fill("")
      cpwd_field.fill("")

      pwd_field.fill(new_password)
      cpwd_field.fill(new_password)
      self.page.wait_for_timeout(12000)

      print("✅ Password fields updated.")
    
    def save_user_updates(self):
     print("💾 Saving updated user...")

     save_btn = self.page.locator("#user-setting-create-user-accept-btn").first

     save_btn.wait_for(state="visible", timeout=8000)
     save_btn.click()

     self.page.wait_for_timeout(2000)
 
     print("✅ User update saved.")
 
    def verify_user_in_table(self, username):
      print(f"🔍 Checking for updated username: {username}")
      table_text = self.page.locator("table").inner_text().lower()

      assert username.lower() in table_text, f"❌ Updated user '{username}' NOT found!"
      print(f"✅ Updated user '{username}' found successfully!")
