def click_delete_role(self, role_name):
    print(f"🗑️ Clicking delete for role '{role_name}'...")

    safe_name = role_name.replace(" ", "\\ ")

    delete_btn = self.page.locator(f"#superadmin-roles-{safe_name}-action-delete-btn")
    delete_btn.wait_for(state="visible", timeout=10000)
    delete_btn.click()

    print("🟢 Delete button clicked.")
def confirm_delete_role(self):
    print("🔹 Confirming delete...")

    confirm_btn = self.page.locator("#delete-accept-btn")
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
