import os
from dotenv import load_dotenv
from llm.models import LlamaModel, GPTModel, MistralModel

class Config:
    """
    Manages application configuration including API keys and model initialization.
    """

    def __init__(self):
        """
        Initialize the Config object by loading environment variables and API keys.
        """
        load_dotenv()
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.groq_api_key = os.getenv("GROQ_API_KEY")

    def get_models(self):
        """
        Create and return instances of all available language models.

        Returns:
            list: A list of initialized model instances ready for use.
        """
        return [
            LlamaModel(self.groq_api_key),
            GPTModel(self.openai_api_key),
            MistralModel(self.groq_api_key)
        ]