# Bug Fixer 🔧

An AI-powered CLI tool that automatically detects and repairs Python syntax errors using Google's Gemini AI, validating every fix with AST parsing before applying it.

## Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/bug-fixer.git
cd bug-fixer

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate  # On Windows
source .venv/bin/activate  # On Mac/Linux

# Install dependencies
pip install fastapi uvicorn requests pydantic python-dotenv

# Create .env file
echo "GOOGLE_API_KEY=your_key_here" > .env
```

## Usage

### 1. Start the Server
```bash
uvicorn main:app --reload
```

### 2. Fix a Single File
```bash
python fixit.py path/to/file.py "describe the bug"
```

### 3. Bulk Scan a Folder
```bash
python bulk.py /path/to/folder
```

## Project Structure

| File | Purpose |
|------|---------|
| `main.py` | FastAPI server — handles requests, backups, and file writing |
| `service.py` | AI brain — calls Gemini with retry loop and multi-file context |
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