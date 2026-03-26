from pypdf import PdfReader
from typing import BinaryIO
import asyncio

from dtos import PdfResult
from service_helpers.interfaces import TextSplitterInterface


class PdfProcessor:
    def _extract_text(self, pdf_file: BinaryIO) -> str:
        reader = PdfReader(pdf_file)

        text = ""
        try:
            for page in reader.pages:
                text += page.extract_text()

            return text.strip()
        except Exception as e:
            raise Exception(f"Error while extracting text from pdf {str(e)}")

    async def parse_pdf(self, text_splitter: TextSplitterInterface, filename: str, pdf_file: BinaryIO) -> PdfResult:
        def _parse() -> PdfResult:
            text = self._extract_text(pdf_file=pdf_file)
            sentences = text_splitter.chunk_text(text=text)

            return PdfResult(file_name=filename, sentences=sentences)

        return await asyncio.to_thread(_parse)
