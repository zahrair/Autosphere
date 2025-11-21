
class RolesPage:

    def __init__(self, page):
        self.page = page
        self.sidebar_btn = page.locator("#header-sidebar-btn")
        self.roles_option = page.locator("#adminsidebar-roles")  # this matches your HTML id
        self.create_btn = page.locator("#superadmin-roles-create-btn")
        self.role_name_field = page.get_by_placeholder("Enter Role Name")

        self.permission_dropdown_placeholder = page.locator(".mat-mdc-select-placeholder")
        self.environment_dropdown = page.get_by_label("Environment")
        self.dropdown_options = page.locator(".mat-mdc-option")

        self.outline_next_btn = page.locator("button.mdc-button--outlined")

        self.first_checkbox = page.locator("#mat-mdc-checkbox-95-input")

        self.select_all_buttons = page.locator("button:has-text('Select All')")

        self.submit_role_btn = page.locator(
            "button:has-text('Create Role')"
        )
        
    def open_sidebar_and_go_to_roles(self):
        print("🔹 Opening sidebar...")
        self.sidebar_btn.click()

        print("⏳ Waiting for Roles menu item...")
        self.roles_option.wait_for(state="visible", timeout=10000)

        print("🔹 Clicking Roles menu item...")
        self.roles_option.click(force=True)

        print("⏳ Waiting for Roles page to load...")
        self.page.wait_for_url("**/roles", timeout=15000)

        print("✅ Successfully arrived on Roles page!")
    
    def click_create_role(self):
        print("🔹 Clicking Create Role button…")
        self.create_btn.wait_for(state="visible", timeout=8000)
        self.create_btn.click()
        self.page.wait_for_timeout(800)


    # ----------------------------------------------------------
    def fill_role_name(self, role_name):
        print(f"🔹 Filling role name: {role_name}")
        self.role_name_field.wait_for(state="visible", timeout=8000)
        self.role_name_field.fill("")
        self.role_name_field.fill(role_name)
        self.page.wait_for_timeout(800)

    def select_environment(self):
      print("🔹 Opening Environment dropdown...")
      env_dropdown = self.page.locator("mat-form-field", has_text="Environment").locator("mat-select")
      env_dropdown.click()
      print("⏳ Waiting for environment options...")
      panel = self.page.locator(".mat-mdc-select-panel")
      panel.wait_for(state="visible", timeout=10000)
      options = self.page.locator("mat-option")
      count = options.count()
      print(f"📌 Found {count} environment options")
      if count == 0:
          raise Exception("❌ No environment options found!")
      print("🟦 Selecting the FIRST Environment option...")
      options.first.click()
      self.page.wait_for_timeout(500)
      print("✅ Environment option selected.")
    
    def select_permission_scheme(self, scheme_name):
       print(f"🔹 Opening Permission Scheme dropdown…")

       dropdown = self.page.locator("mat-form-field", has_text="Select Permission Scheme").locator("mat-select")
       dropdown.click()

       print("⏳ Waiting for permission scheme options…")
       panel = self.page.locator(".mat-mdc-select-panel")
       panel.wait_for(state="visible", timeout=10000)

       print(f"🟦 Selecting scheme: {scheme_name}")
       target = self.page.get_by_role("option", name=scheme_name)
       target.click()

       print("✅ Permission scheme selected successfully.")
   
    def click_create_role_button(self):
      print("🔹 Clicking Create Role button...")

      btn = self.page.get_by_role("button", name="Create Role")
      btn.wait_for(state="visible", timeout=10000)
      btn.click()

      print("✅ Create Role button clicked successfully.")
    
    def verify_role_in_table(self, role_name):
      print(f"🔍 Checking if role '{role_name}' exists in the table...")

      # Wait for table to finish loading
      self.page.wait_for_timeout(2000)

      # Get entire table text
      table_text = self.page.locator("table").inner_text().lower()

      print("📄 Table content:")
      print(table_text)

      assert role_name.lower() in table_text, f"❌ Role '{role_name}' was NOT found in the table!"

      print(f"✅ Role '{role_name}' is present in the roles table.")
  
  
    def open_role_action_menu(self, role_name):
       print(f"🔹 Opening action menu for role '{role_name}'...")

       # Create safe CSS ID (spaces become \ )
       safe_name = role_name.replace(" ", "\\ ")

       # Example: #superadmin-roles-AutomationRole-action-btn
       action_btn = self.page.locator(f"#superadmin-roles-{safe_name}-action-btn")

       action_btn.wait_for(state="visible", timeout=10000)
       action_btn.click()

       print("⏳ Waiting 8 seconds so you can SEE the action menu...")
       self.page.wait_for_timeout(8000)

       print("✅ Action menu opened.")

    def click_delete_role(self, role_name):
      print(f"🗑️ Clicking delete for role '{role_name}'...")

      safe_name = role_name.replace(" ", "\\ ")

      delete_btn = self.page.locator(f"#superadmin-roles-{safe_name}-action-delete-btn")
      delete_btn.wait_for(state="visible", timeout=10000)
      delete_btn.click()

      print("🟢 Delete button clicked.")

    def confirm_delete_role(self):
      print("🔹 Confirming delete...")

      confirm_btn = self.page.locator("#delete-accept-btn").first
      confirm_btn.wait_for(state="visible", timeout=10000)
      confirm_btn.click()

      print("🟢 Delete confirmed.")
      self.page.wait_for_timeout(2000)
         
    def verify_role_not_in_table(self, role_name):
       print(f"🔍 Checking that role '{role_name}' is removed...")

       # Allow table to reload
       self.page.wait_for_timeout(3000)

       table_text = self.page.locator("table").inner_text().lower()

       assert role_name.lower() not in table_text, f"❌ Role '{role_name}' is still present!"
       print(f"✅ Role '{role_name}' successfully removed from table.")

    def open_role_action_menu(self, role_name):
      print(f"🔹 Opening action menu for role '{role_name}'...")

      safe = role_name.replace(" ", "\\ ")
      btn = self.page.locator(f"#superadmin-roles-{safe}-action-btn")

      btn.wait_for(state="visible", timeout=10000)
      btn.click()

      self.page.wait_for_timeout(2000)
      print("🟢 Action menu opened again.")

    def click_role_details(self, role_name):
       print(f"🔹 Clicking DETAILS for role '{role_name}'...")

       safe = role_name.replace(" ", "\\ ")
       details_btn = self.page.locator(f"#superadmin-roles-{safe}-action-details-btn")

       details_btn.wait_for(state="visible", timeout=10000)
       details_btn.click()
   
       self.page.wait_for_timeout(2000)
       print("🟢 Role details opened.")
   # Inside RolesPage class
    def scroll_main_container_until_visible(self, locator, max_attempts=12):
       container = self.page.locator("div.main-container")

       for i in range(max_attempts):
           try:
               locator.wait_for(state="visible", timeout=1000)
               print(f"👀 Update button visible after scroll #{i}")
               return True
           except:
               container.evaluate("el => el.scrollTop += 250")
               self.page.wait_for_timeout(300)

       return False
     
    def save_role_changes(self):
       print("💾 Trying to click Update Role...")

       update_btn = self.page.locator("button[mat-flat-button][type='submit']").first

       # 1️⃣ Scroll the REAL container (main-container)
       print("🔽 Scrolling main-container to find Update button…")
       if not self.scroll_main_container_until_visible(update_btn):
           print("⚠ Still not visible… trying final fallback scroll")
           self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
           self.page.wait_for_timeout(800)
   
       # 2️⃣ Ensure visibility
       update_btn.wait_for(state="visible", timeout=5000)

       # 3️⃣ Scroll into exact position
       update_btn.scroll_into_view_if_needed()
       self.page.wait_for_timeout(400)

       # 4️⃣ Click
       update_btn.click(force=True)
       print("🟢 Update Role clicked successfully!")

   