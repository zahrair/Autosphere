import subprocess
import sys

# THE EXACT ORDER YOU WANT
workflow_tests = [
    "test_create_machine_api.py",
    "test_email_classification.py",
    "test_email_summarization.py",
    "test_text_classification.py",
    "test_text_summarization.py",
    "test_image_analysis.py",
]

print("🚀 STARTING WORKFLOW...\n")

for test in workflow_tests:
    print(f"▶️ Running: {test}\n")

    result = subprocess.run(["pytest", test, "-s"])

    if result.returncode != 0:
        print(f"\n❌ FAILED at: {test}")
        print("⛔ WORKFLOW STOPPED")
        sys.exit(result.returncode)

    print(f"✔ Completed: {test}\n")

print("\n🎉 WORKFLOW FINISHED SUCCESSFULLY!\n")
