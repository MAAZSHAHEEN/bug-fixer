# Bug Fixer 🔧

An AI-powered developer tool that automatically detects and repairs Python syntax errors using Google's Gemini AI, validating every fix with AST parsing before applying it.

## Live API
- **Base URL:** `http://3.21.35.40`
- **Interactive Docs:** `http://3.21.35.40/docs`

## Tech Stack
- **FastAPI** — REST API framework
- **Google Gemini AI** — AI-powered code repair
- **Nginx + Ubuntu EC2** — Production deployment on AWS

## Installation
```bash
# Clone the repository
git clone https://github.com/MAAZSHAHEEN/bug-fixer.git
cd bug-fixer

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate  # On Windows
source .venv/bin/activate  # On Mac/Linux

# Install dependencies
pip install fastapi uvicorn requests pydantic python-dotenv

# Create .env file
echo "GOOGLE_API_KEY=your_key_here" > .env

# Start the server
uvicorn main:app --reload
```

## Usage

### 1. Fix a Single File via CLI
```bash
python fixit.py path/to/file.py "describe the bug"
```

### 2. Bulk Scan a Folder
```bash
python bulk.py /path/to/folder
```

### 3. API Request
```bash
POST http://3.21.35.40/fix
Content-Type: application/json

{
  "title": "Fix syntax error",
  "issue_body": "missing closing parenthesis",
  "file_path": "your_file.py",
  "language": "python",
  "related_files": []
}
```

## Project Structure

| File | Purpose |
|------|---------|
| `main.py` | FastAPI server — handles requests, backups, and file writing |
| `service.py` | AI brain — calls Gemini with self-healing retry loop and multi-file context |
| `model.py` | Pydantic schema defining the BugReport structure |
| `fixit.py` | CLI tool for single file fixes with diff output |
| `bulk.py` | Batch processor for scanning and fixing entire folders |

## Features

- ✅ Auto-backup before any changes
- ✅ AST syntax validation before saving
- ✅ Self-healing loop — retries up to 3 times if AI fix fails
- ✅ Multi-file context — sends related file signatures to AI
- ✅ Diff preview showing exactly what changed
- ✅ Bulk mode for entire folders
- ✅ Deployed on AWS EC2 with Nginx