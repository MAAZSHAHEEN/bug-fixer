import requests
import json
import ast
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY missing from .env file")

def call_gemini(prompt: str) -> str:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    response = requests.post(url, json=payload)
    data = response.json()

    if response.status_code != 200:
        raise Exception(f"API Error: {data}")

    raw = data['candidates'][0]['content']['parts'][0]['text'].strip()

    if raw.startswith("```"):
        lines = raw.splitlines()
        raw = "\n".join(lines[1:-1])

    parsed = json.loads(raw)
    return parsed["fixed_code"]


def get_ai_fix(code_content: str, issue_description: str, related_files: list = [], max_attempts: int = 3) -> str:
    
    context = ""
    for filepath in related_files:
        if os.path.exists(filepath):
            file_context = get_file_context(filepath)
            context += f"\nContext from {filepath}:\n{file_context}\n"

    prompt = f"""Fix this bug: {issue_description}
Code:
{code_content}
{f"Related file context:{context}" if context else ""}
Respond ONLY with a JSON object in this exact format, no markdown, no explanation:
{{"fixed_code": "corrected code here"}}"""

    last_error = None
    last_fix = None

    for attempt in range(1, max_attempts + 1):
        print(f"Attempt {attempt} of {max_attempts}...")

        if last_error:
            prompt = f"""Your previous fix had a syntax error: {last_error}
Here was your broken fix:
{last_fix}
Original bug: {issue_description}
Original code:
{code_content}
Try again. Respond ONLY with a JSON object:
{{"fixed_code": "corrected code here"}}"""

        try:
            last_fix = call_gemini(prompt)
            ast.parse(last_fix)
            print(f"✅ Valid fix found on attempt {attempt}")
            return last_fix

        except SyntaxError as e:
            last_error = str(e)
            print(f"❌ Attempt {attempt} failed: {last_error}")

        except Exception as e:
            raise Exception(f"AI call failed: {str(e)}")

    raise Exception(f"AI failed after {max_attempts} attempts.")
def get_file_context(filepath: str) -> str:
    context_lines = []
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            stripped = line.strip()
            if stripped.startswith("import") or \
               stripped.startswith("from") or \
               stripped.startswith("def") or \
               stripped.startswith("class"):
                context_lines.append(stripped)
    return "\n".join(context_lines)