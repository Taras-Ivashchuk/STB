from pydantic import BaseModel
from pathlib import Path


class PdfResult(BaseModel):
    file_path: Path
    sentences: list[str]