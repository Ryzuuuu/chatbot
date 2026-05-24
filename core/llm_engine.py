from langchain_community.llms import LlamaCpp
import os
from dotenv import load_dotenv

load_dotenv()

class LLMEngine:
    def __init__(self, model_path: str = r"C:\Projects\chatbot\models\mistral-7b-instruct-v0.2.Q4_K_M.gguf"):
        self.model_path = model_path
        self.llm = self._load_model()

    def _load_model(self) -> LlamaCpp:
        print(f"Loading model from {self.model_path}...")

        if not os.path.exists(self.model_path):
            raise FileNotFoundError(
                f"Model file not found at {self.model_path}\n"
                "Download it from: https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf\n"
                "Save it to: C:\\Projects\\chatbot\\models\\"
            )

        return LlamaCpp(
            model_path=self.model_path,
            n_ctx=4096,
            n_threads=6,
            n_gpu_layers=0,      # Pure CPU — no GPU needed
            temperature=0.7,
            max_tokens=512,
            verbose=False,
            stop=["Human:", "\nHuman:", "You:", "\nYou:"],
        )

    @staticmethod
    def load_ollama():
        """
        Lightweight CPU option for development.
        1. Download Ollama: https://ollama.com/download/windows
        2. Open PowerShell and run: ollama pull mistral
        3. Then use this method instead of __init__
        """
        from langchain_community.llms import Ollama
        return Ollama(model="mistral")