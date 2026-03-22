from pydantic import BaseModel


class PdfResult(BaseModel):
    file_name: str
    sentences: list[str]
