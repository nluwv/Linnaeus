from llm import BaseLLM
import groq

class LlamaModel(BaseLLM):
    """
    Implementation of the BaseLLM for Llama model using Groq's API.
    Provides access to the Llama-3.1 model through Groq's infrastructure.
    """
    def __init__(self, groq_api_key):
        """
        Initializes the Llama model client using Groq's API.

        Args:
            groq_api_key (str): Authentication key for Groq's API service.
                Must be a valid Groq API key.
        """
        super().__init__(name="Llama", client=groq.Groq(api_key=groq_api_key))

    def _call_model_api(self, messages):
        """
        Makes a completion request to Groq's API for the Llama model.

        Sends the formatted messages to the Llama-3.1 model and retrieves
        the response.

        Args:
            messages (list[dict]): List of message dictionaries formatted
                for Groq's chat completion API.

        Returns:
            str: The model's response content.
        """
        # Groq API call for Llama model
        response = self.client.chat.completions.create(
            messages=messages,
            model="llama-3.1-8b-instant",
            max_tokens=1000
        ).choices[0].message.content
        return response