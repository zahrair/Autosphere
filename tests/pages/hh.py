def select_first_license(self):
    print("🔹 Opening Taskhub License dropdown...")
    self.license_dropdown.click()

    # Wait for the dropdown panel
    panel = self.page.wait_for_selector(".mat-mdc-select-panel", timeout=5000)

    # Collect options
    options = self.page.locator(".mat-mdc-option")
    count = options.count()

    print(f"📌 Found {count} license options:")
    for i in range(count):
        print("   ➜", options.nth(i).inner_text())

    if count == 0:
        raise Exception("❌ No license options found!")

    # Click the first option (DO NOT close popup)
    options.nth(0).click()
    print("✅ License selected.")

    # Wait for dropdown panel to disappear (normal behavior)
    self.page.wait_for_selector(".mat-mdc-select-panel", state="hidden", timeout=5000)

    print("🟢 License dropdown closed, popup still open and ready to Create.")
