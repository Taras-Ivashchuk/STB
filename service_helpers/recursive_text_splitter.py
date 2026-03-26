from langchain_text_splitters import RecursiveCharacterTextSplitter


class RecursiveLangChainTextSplitter:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 500) -> None:
        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ". ", " "]
        )

    def chunk_text(self, text: str) -> list[str]:
        """LangChain text splitter which uses recursive split strategy"""

        return self._splitter.split_text(text)
