import ast
import os
import requests
import sys

def scan_folder(folder_path):
    broken_files = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".py"):
            filepath = os.path.join(folder_path, filename)
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                code = f.read()
            try:
                ast.parse(code)
            except SyntaxError as e:
                broken_files.append((filepath, str(e)))

    return broken_files

def fix_file(filepath, issue):
    response = requests.post("http://127.0.0.1:8000/fix", json={
        "title": "Bulk Fix",
        "issue_body": issue,
        "file_path": filepath,
        "language": "python"
    })
    return response.json()

if len(sys.argv) < 2:
    print("Usage: python bulk.py <folder_path>")
    sys.exit(1)

folder = sys.argv[1]
print(f"\n🔍 Scanning folder: {folder}\n")

broken = scan_folder(folder)

if not broken:
    print("✅ No syntax errors found.")
else:
    print(f"Found {len(broken)} broken file(s):\n")
    for filepath, error in broken:
        print(f"  ❌ {filepath} — {error}")

    confirm = input("\nFix all? (y/n): ")
    if confirm.lower() == "y":
        for filepath, error in broken:
            print(f"\n🔧 Fixing {filepath}...")
            result = fix_file(filepath, error)
            if result["status"] == "success":
                print(f"  ✅ Fixed")
            else:
                print(f"  ❌ Failed: {result['message']}")
