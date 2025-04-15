import os
from dotenv import load_dotenv
from llm.models import LlamaModel, GPTModel, MistralModel

class Config:
    def __init__(self):
        load_dotenv()
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.groq_api_key = os.getenv("GROQ_API_KEY")

    def get_models(self):
        return [
            LlamaModel(self.groq_api_key),
            GPTModel(self.openai_api_key),
            MistralModel(self.groq_api_key)
        ]
