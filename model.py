from pydantic import BaseModel
from typing import Optional, List

class BugReport(BaseModel):
    title: str
    issue_body: str
    file_path: str
    language: str = "python"
    ai_suggestion: Optional[str] = None
    related_files: List[str] = []