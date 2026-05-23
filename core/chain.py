from langchain.chains import ConversationChain
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from core.memory import MemoryFactory
from core.llm_engine import LLMEngine

SYSTEM_PROMPT = """You are a helpful AI assistant with excellent memory.
You remember everything discussed in this conversation.
Be concise, accurate, and personable."""

class ChatbotChain:
    def __init__(self, memory_type: str = "summary_buffer", llm=None):
        self.llm = llm or LLMEngine().llm
        self.memory = self._build_memory(memory_type)
        self.chain = self._build_chain()

    def _build_memory(self, memory_type: str):
        if memory_type == "buffer":
            return MemoryFactory.buffer()
        elif memory_type == "window":
            return MemoryFactory.window(k=6)
        elif memory_type == "summary":
            return MemoryFactory.summary(self.llm)
        elif memory_type == "vector":
            return MemoryFactory.vector_store()
        else:
            return MemoryFactory.summary_buffer(self.llm)

    def _build_chain(self) -> ConversationChain:
        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(SYSTEM_PROMPT),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{input}"),
        ])
        return ConversationChain(
            llm=self.llm,
            memory=self.memory,
            prompt=prompt,
            verbose=False
        )

    def chat(self, user_input: str) -> str:
        return self.chain.predict(input=user_input)

    def get_history(self) -> list:
        return self.memory.chat_memory.messages

    def clear(self):
        self.memory.clear()