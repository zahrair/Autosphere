from playwright.sync_api import Page

class RobotsPage:
    def __init__(self, page: Page):
        self.page = page
        self.sidebar_robots = page.locator("#sidebar-robots")
        self.robots_heading = page.locator("h1, h2, .page-title, .header-title")
        self.create_btn = page.locator("#robot-create-btn")
        self.machine_name_field = page.locator("#create-machine-name-field")
        self.license_select = page.locator("#create-robot-license-select")
        self.remote_dir_field = page.locator("#remote-root-directory-field")
        self.submit_btn = page.locator("#create-machine-create-btn").first
        self.table_body = page.locator("tbody")

    def open_robots_section(self):
        print("🔹 Opening Robots section...")
        self.sidebar_robots.wait_for(state="visible", timeout=10000)
        self.sidebar_robots.click()
        self.page.wait_for_load_state("networkidle")
        print(" Robots section opened successfully!")

    def verify_robots_heading(self):
        print("🔹 Verifying Robots heading...")
        self.robots_heading.wait_for(state="visible", timeout=8000)
        heading_text = self.robots_heading.inner_text().strip()
        assert "robots" in heading_text.lower(), f"Expected heading 'Robots', got '{heading_text}'"
        print(f"Heading verified: '{heading_text}'")

    def click_create_robot(self):
        print(" Clicking Create Robot button...")
        self.create_btn.wait_for(state="visible", timeout=8000)
        self.create_btn.click()
        print(" Create Robot form opened.")

    def fill_machine_name(self, name: str):
        print(f" Filling Machine Name: {name}")
        self.machine_name_field.wait_for(state="visible", timeout=8000)
        self.machine_name_field.fill(name)

    def select_robot_license(self):
        print("Selecting license option (listing all available)...")

        self.license_select.wait_for(state="visible", timeout=10000)
        self.license_select.click()
        print(" Dropdown opened.")

        overlay_panel = self.page.locator("#create-robot-license-select-panel")
        overlay_panel.wait_for(state="visible", timeout=10000)
        print("License dropdown     panel visible.")

        options = self.page.locator("mat-option")
        count = options.count()
        print(f" Found {count} license options in dropdown:")

        for i in range(count):
            option_id = options.nth(i).get_attribute("id")
            option_text = options.nth(i).inner_text().strip()
            print(f"   ➜ {option_id}: {option_text}")

        target_option = self.page.locator("#mat-option-9")
        target_option.wait_for(state="visible", timeout=10000)
        target_option.click()
        print(" Clicked license option with ID mat-option-106 successfully!")
        overlays = self.page.locator(".cdk-overlay-backdrop")
        if overlays.count() > 0:
          print("Closing dropdown overlay before submitting...")
          self.page.keyboard.press("Escape")    
          self.page.wait_for_timeout(1000)

  

    def fill_working_directory(self, path: str):
        print(f" Filling Working Directory: {path}")
        self.remote_dir_field.wait_for(state="visible", timeout=8000)
        self.remote_dir_field.fill(path)

    def submit_robot_creation(self):
        print("Submitting robot creation form...")
        self.submit_btn.wait_for(state="visible", timeout=8000)
        self.submit_btn.click()
        self.page.wait_for_load_state("networkidle")
        print(" Robot creation submitted!")

    def verify_robot_present(self, name: str):
        print(f"Verifying '{name}' in robots table...")
        self.table_body.wait_for(state="visible", timeout=10000)
        table_text = self.table_body.inner_text().lower()
        assert name.lower() in table_text, f" Robot '{name}' not found in table!"
        print(f"Robot '{name}' found successfully in table.")
    
    
    def open_robot_menu(self, name: str):
      print(f"Opening menu for robot '{name}'...")
      menu_button = self.page.locator(f"#{name}-robot-action-btn")
      menu_button.wait_for(state="visible", timeout=10000)
      menu_button.click()
      print(f" Menu opened for robot '{name}'")


    def click_delete_button(self, name: str):
     print(f"Clicking delete button for robot '{name}'...")
     delete_button = self.page.locator(f"#{name}-process-delete-btn")
     delete_button.wait_for(state="visible", timeout=10000)
     delete_button.click()
     print(f" Delete button clicked for robot '{name}'")


    def confirm_delete_action(self):
      print("Confirming delete action...")
      confirm_button = self.page.locator("#delete-accept-btn").first
      confirm_button.wait_for(state="visible", timeout=10000)
      confirm_button.click()
      print("Delete confirmed!")


    def verify_robot_not_present(self, name: str):
     print(f"Checking that robot '{name}' is no longer listed...")
     self.page.wait_for_timeout(2000)
     table_text = self.table_body.inner_text().lower()
     assert name.lower() not in table_text, f" Robot '{name}' still present!"
     print(f"Robot '{name}' successfully deleted and removed from the table.")
    
    
    
    
    def click_edit_button(self, name="robo3"):
      print(f"🔹 Clicking edit button for '{name}'...")
      self.page.wait_for_timeout(1000)
      edit_btn = self.page.locator(f"#{name}-machine-edit-btn")
      self.page.wait_for_selector(f"#{name}-machine-edit-btn", timeout=10000)
      edit_btn.click()
      print("Edit button clicked successfully")
    
    
    def edit_robot_description(self, description_text):
      print(f"🔹 Editing robot description to '{description_text}'...")

      desc_field = self.page.locator("#create-machine-description-field")
      desc_field.wait_for(state="visible", timeout=8000)

      desc_field.fill("")
      desc_field.fill(description_text)
      print(f" Robot description changed to '{description_text}'")

     
    def submit_robot_edit(self):
       print("🔹 Clicking Update button to save changes...")

       update_btn = self.page.locator("button#create-machine-create-btn").first
       update_btn.wait_for(state="visible", timeout=8000)

       print(f"Before click — Current URL: {self.page.url}")
       update_btn.click()
       print("✅ Update button clicked — waiting for AJAX save...")

       self.page.wait_for_load_state("networkidle")
       
       success_toast = self.page.locator("text=Robot updated successfully")
       if success_toast.count() > 0:
           success_toast.wait_for(state="visible", timeout=8000)
           print("✅ Update success toast appeared!")
       else:
           print("⚠️ No success toast found — assuming silent save.")
   
       print("🔹 Returning to Robots list manually...")
       self.sidebar_robots.wait_for(state="visible", timeout=10000)
       self.sidebar_robots.click()
   
       self.page.wait_for_load_state("networkidle")
       self.page.wait_for_selector("tbody", state="visible", timeout=15000)
       print("✅ Robots list page loaded successfully after update.")

     
 
    def verify_robot_present(self, name):
       print(f"🔹 Verifying robot '{name}' in the table...")

       self.page.wait_for_selector("tbody", state="visible", timeout=15000)
       table_text = self.page.locator("tbody").inner_text().lower()

       assert name.lower() in table_text, f" Robot '{name}' not found in table!"
       print(f" Robot '{name}' found successfully in the table.")
    