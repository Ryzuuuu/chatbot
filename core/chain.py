import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from langchain_classic.chains import ConversationChain
from langchain_core.prompts import PromptTemplate
from core.memory import MemoryFactory
from core.llm_engine import LLMEngine

SYSTEM_PROMPT = """You are a helpful AI assistant with excellent memory. \
You remember everything discussed in this conversation. \
Answer ONLY what is asked. No sign-offs. \
If asked to spell a word, reply with just the letters separated by dashes on one line. \
Be concise, accurate, and personable."""

# Mistral's required [INST] format — LlamaCpp needs a plain string, not chat objects
MISTRAL_PROMPT = PromptTemplate(
    input_variables=["history", "input"],
    template=(
        f"[INST] {SYSTEM_PROMPT}\n\n"
        "Conversation so far:\n{history}\n\n"
        "Human: {input} [/INST]"
    )
)

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
        return ConversationChain(
            llm=self.llm,
            memory=self.memory,
            prompt=MISTRAL_PROMPT,
            verbose=False
        )

    def chat(self, user_input: str) -> str:
        return self.chain.predict(input=user_input)

    def get_history(self) -> list:
        return self.memory.chat_memory.messages

    def clear(self):
        self.memory.clear()

if __name__ == "__main__":
    print("Loading model mistralai/Mistral-7B-Instruct-v0.2...")
    bot = ChatbotChain(memory_type="summary_buffer")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit", "bye"):
            print("Goodbye!")
            break

        response = bot.chat(user_input)
        print(f"Bot: {response}")