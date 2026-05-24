from langchain_classic.memory import (
    ConversationBufferMemory,
    ConversationBufferWindowMemory,
    ConversationSummaryMemory,
    ConversationSummaryBufferMemory,
    VectorStoreRetrieverMemory,
)
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import os

CHROMA_PATH = os.path.join(os.environ.get("USERPROFILE", "C:\\"), "chatbot_chroma_db")

class MemoryFactory:

    @staticmethod
    def buffer() -> ConversationBufferMemory:
        """Full history — good for short sessions."""
        return ConversationBufferMemory(
            memory_key="history", return_messages=False  # ← "history" matches prompt var
        )

    @staticmethod
    def window(k: int = 5) -> ConversationBufferWindowMemory:
        """Last k turns only — good for long sessions."""
        return ConversationBufferWindowMemory(
            k=k, memory_key="history", return_messages=False
        )

    @staticmethod
    def summary(llm) -> ConversationSummaryMemory:
        """Summarizes old turns — token-efficient."""
        return ConversationSummaryMemory(
            llm=llm, memory_key="history", return_messages=False
        )

    @staticmethod
    def summary_buffer(llm, max_token_limit: int = 2000):
        """Best option: buffer recent turns, summarize older ones."""
        return ConversationSummaryBufferMemory(
            llm=llm,
            max_token_limit=max_token_limit,
            memory_key="history",
            return_messages=False  # ← plain string, not message objects
        )

    @staticmethod
    def vector_store(persist_dir: str = CHROMA_PATH):
        """Long-term semantic memory via embeddings."""
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        vectorstore = Chroma(
            persist_directory=persist_dir,
            embedding_function=embeddings
        )
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        return VectorStoreRetrieverMemory(retriever=retriever)