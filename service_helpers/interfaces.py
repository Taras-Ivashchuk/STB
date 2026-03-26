from typing import Protocol


class TextSplitterInterface(Protocol):
    def chunk_text(self, text: str) -> list[str]:
        """Split text into chunks"""
