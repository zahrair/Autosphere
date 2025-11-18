
class RolesPage:

    def __init__(self, page):
        self.page = page
        self.sidebar_btn = page.locator("#header-sidebar-btn")
        self.roles_option = page.locator("#adminsidebar-roles")  # this matches your HTML id

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
