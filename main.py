import ast
import shutil
from fastapi import FastAPI
from model import BugReport
from service import get_ai_fix

app = FastAPI()

@app.post("/fix")
def repair_bug(report: BugReport):
    try:
        with open(report.file_path, "r") as file:
            code = file.read()

        shutil.copy(report.file_path, report.file_path + ".bak")

        fixed_code = get_ai_fix(code, report.issue_body, report.related_files)

        try:
            ast.parse(fixed_code)
        except SyntaxError:
            return {
                "status": "error",
                "message": "AI returned invalid code. Original file kept safe."
            }

        with open(report.file_path, "w") as file:
            file.write(fixed_code)

        return {
            "status": "success",
            "filename": report.file_path,
            "original_code": code,
            "fixed_code": fixed_code
        }

    except FileNotFoundError:
        return {"status": "error", "message": f"File '{report.file_path}' not found."}
    except Exception as e:
        return {"status": "error", "message": str(e)}