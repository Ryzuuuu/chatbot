from langchain_huggingface import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
import os
from dotenv import load_dotenv

load_dotenv()

class LLMEngine:
    def __init__(self, model_id: str = "mistralai/Mistral-7B-Instruct-v0.2"):
        self.model_id = model_id
        self.llm = self._load_model()

    def _load_model(self) -> HuggingFacePipeline:
        tokenizer = AutoTokenizer.from_pretrained(
            self.model_id,
            token=os.getenv("HF_TOKEN")
        )
        model = AutoModelForCausalLM.from_pretrained(
            self.model_id,
            torch_dtype=torch.float16,
            device_map="auto",
            token=os.getenv("HF_TOKEN")
        )
        pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=512,
            temperature=0.7,
            do_sample=True,
        )
        return HuggingFacePipeline(pipeline=pipe)

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