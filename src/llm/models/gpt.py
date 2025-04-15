import openai
from llm import BaseLLM

class GPTModel(BaseLLM):
    """
    Implementation of the BaseLLM for OpenAI's GPT models.
    Handles authentication and communication with OpenAI's API.
    """
    def __init__(self, openai_api_key):
        """
        Initializes the GPT model client using OpenAI's API.

        Args:
            openai_api_key (str): Authentication key for OpenAI's API service.
                Must be a valid OpenAI API key.
        """
        super().__init__(name="GPT", client=openai.Client(api_key=openai_api_key))

    def _call_model_api(self, messages):
        """
        Makes a completion request to OpenAI's GPT API.

        Sends the formatted messages to GPT-3.5-turbo and retrieves
        the model's response.

        Args:
            messages (list[dict]): List of message dictionaries formatted
                for OpenAI's chat completion API.

        Returns:
            str: The model's response content.
        """
        # OpenAI GPT API call
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=1000
        ).choices[0].message['content']
        return response