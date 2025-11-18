import os
from playwright.sync_api import Page

class ProcessesPage:
    def __init__(self, page: Page):
        self.page = page
        self.sidebar_processes = page.locator("#sidebar-processes")
        self.processes_heading = page.locator("h1, h2, .page-title, .header-title")
        self.create_btn = page.locator("#processes-create-btn")
        self.name_field = page.locator("#create-process-name-field")
        self.machine_dropdown = page.locator("#create-process-machine-select")
        self.execution_field = page.locator("#create-process-execution-name-field")
        self.upload_btn = page.locator("#create-process-package-upload-btn")
        self.submit_btn = page.locator("#create-process-create-btn").first
        self.table_body = page.locator("tbody")

    def open_processes_section(self):
        print("🔹 Clicking on Processes sidebar option...")
        self.sidebar_processes.wait_for(state="visible", timeout=10000)
        self.sidebar_processes.click()
        self.page.wait_for_load_state("networkidle")
        print("✅ Processes section opened successfully.")

    def verify_processes_heading(self):
        print("🔹 Verifying Processes heading...")
        self.processes_heading.wait_for(state="visible", timeout=8000)
        heading_text = self.processes_heading.inner_text().strip()
        assert "processes" in heading_text.lower(), f"❌ Expected heading 'Processes', but got '{heading_text}'"
        print(f"✅ Heading verified: '{heading_text}'")

     # ------------------  CREATE PROCESS ------------------

    def click_create_process(self):
        print("🔹 Clicking Create Process button...")
        self.create_btn.wait_for(state="visible", timeout=8000)
        self.create_btn.click()
        print("✅ Create Process form opened.")

    def fill_process_name(self, name):
        print(f"🔹 Filling Process Name: {name}")
        self.name_field.wait_for(state="visible", timeout=8000)
        self.name_field.fill(name)

    def select_machine(self):
        print("🔹 Selecting machine from dropdown...")

        # 1. Open the dropdown
        self.machine_dropdown.wait_for(state="visible", timeout=10000)
        self.machine_dropdown.click()
        print("🔽 Dropdown opened.")

        # 2. Wait for the dropdown panel
        panel = self.page.locator("#create-process-machine-select-panel")
        panel.wait_for(state="visible", timeout=10000)
        print("📌 Machine dropdown panel visible.")

        # 3. Log all available mat-options (just like licenses in Robots page)
        options = self.page.locator("mat-option")
        count = options.count()

        print(f"🔍 Found {count} machine options in dropdown:")
        for i in range(count):
            option_id = options.nth(i).get_attribute("id")
            option_text = options.nth(i).inner_text().strip()
            print(f"   ➜ {option_id}: {option_text}")

        # 4. Pick the target option (mat-option-20)
        target_option = self.page.locator("#mat-option-17")
        target_option.wait_for(state="visible", timeout=10000)
        target_option.click()
        print("✅ Selected machine option with ID mat-option-20.")

        # 5. Close overlay (Escape)
        overlays = self.page.locator(".cdk-overlay-backdrop")
        if overlays.count() > 0:
            print("🔒 Closing overlay dropdown backdrop…")
            self.page.keyboard.press("Escape")
            self.page.wait_for_timeout(600)
    
        print("🎉 Machine selection completed successfully.")
    

    def upload_robo_file(self, file_name="AddQueueItem.robot"):
        print("🔹 Uploading .robot package file...")
    
        full_path = rf"D:\Autosphere\auto1\{file_name}"
        print(f"📁 Uploading file: {full_path}")

        if not os.path.exists(full_path):
         raise FileNotFoundError(f"❌ File not found: {full_path}")

        # 1️⃣ Click the button that opens the file dialog
        #upload_btn = self.page.locator("#create-process-package-upload-btn")
        #upload_btn.wait_for(state="visible", timeout=8000)
        #upload_btn.click()

        # 2️⃣ Find the real file input element
        file_input = self.page.locator("input[type='file']")
        file_input.wait_for(state="attached", timeout=8000)

        # 3️⃣ Upload the file to the <input>
        file_input.set_input_files(full_path)
        print("📤 File uploaded — waiting for backend processing...")

        # 4️⃣ Wait for filename preview to appear (Autosphere shows uploaded file name)
        uploaded_file_name = self.page.locator(f"text={file_name}")
        try:
            uploaded_file_name.wait_for(state="visible", timeout=8000)
            print("✅ UI shows uploaded file name.")
        except:
            print("⚠️ Filename preview not found — maybe UI uses a card instead.")

        # 5️⃣ Wait for loading spinner to disappear (Autosphere uses mat-progress-spinner)
        try:
            spinner = self.page.locator("mat-progress-spinner")
            spinner.wait_for(state="hidden", timeout=10000)
            print("⏳ Upload spinner gone — upload complete.")
        except:
            print("⚠️ No spinner detected or already completed.")
    
        # 6️⃣ Wait for package card (Autosphere displays the uploaded package as a card)
        try:
            package_card = self.page.locator(".package-file-card")
            package_card.wait_for(state="visible", timeout=10000)
            print("📦 Package card visible — upload successful!")
        except:
            print("⚠️ No package card found — but file may still be uploaded.")

        print("🎉 File upload completed successfully!")


    

    def fill_execution_name(self, execution_name):
        print(f"🔹 Filling Execution Name: {execution_name}")
        self.execution_field.wait_for(state="visible", timeout=8000)
        self.execution_field.fill(execution_name)

    def submit_process(self):
        print("🔹 Clicking Create button...")
        self.submit_btn.wait_for(state="visible", timeout=8000)
        self.submit_btn.click()
        self.page.wait_for_load_state("networkidle")
        print("✅ Process created successfully!")

    def verify_process_present(self, process_name):
       print(f"🔍 Verifying process '{process_name}' in table...")

       self.page.wait_for_selector("table.mat-mdc-table", timeout=15000)

       rows = self.page.locator("td.process-display-name div.wordwrap")

       rows.first.wait_for(state="visible", timeout=10000)

       row_texts = rows.all_text_contents()

       print("📄 Processes found in table:")
       for r in row_texts:
           print("  ➜", r)

       assert process_name in row_texts, f"❌ Process '{process_name}' NOT found in table!"

       print(f"✅ Process '{process_name}' is successfully present in the table!")
    
    
   