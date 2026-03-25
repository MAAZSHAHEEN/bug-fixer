import sys
import requests
import difflib

if len(sys.argv) < 3:
    print("Usage: python fixit.py <file_path> <issue_description>")
    sys.exit(1)

file_path = sys.argv[1]
issue_body = sys.argv[2]

response = requests.post("http://127.0.0.1:8000/fix", json={
    "title": "CLI Fix",
    "issue_body": issue_body,
    "file_path": file_path,
    "language": "python"
})

data = response.json()

if data["status"] == "success":
    original = data["original_code"].splitlines()
    fixed = data["fixed_code"].splitlines()

    diff = difflib.unified_diff(
        original,
        fixed,
        fromfile="original",
        tofile="fixed",
        lineterm=""
    )

    print("\n✅ Bug Fixed! Here is what changed:\n")
    for line in diff:
        print(line)
else:
    print(f"\n❌ Error: {data['message']}")