from abc import ABC, abstractmethod
from typing import List, Dict, Union
import openai
import groq


# Base abstract class for all LLM models
class BaseLLM(ABC):
    """
    Abstract base class for Large Language Model implementations.
    Provides common functionality for different LLM providers while enforcing
    a consistent interface through abstract methods.
    """
    def __init__(self, name: str, client: Union[openai.Client, groq.Groq]):
        """
        Initialize a new LLM instance.

        Creates a new instance of a language model with the specified name
        and API client. This base initialization handles setting up the 
        common attributes needed by all LLM implementations.

        Args:
            name (str): Identifier name for the model instance. Used for
                logging and identification purposes.
            client (Union[openai.Client, groq.Groq]): API client instance
                for making calls to the LLM provider. Must be properly
                configured with API keys and endpoints.
        """
        self.name = name
        self.client = client

    @abstractmethod
    def _call_model_api(self, messages: List[Dict[str, str]]) -> str:
        """
        Makes the API call to the specific LLM provider.
        
        Must be implemented by concrete subclasses to handle provider-specific API calls.

        Args:
            messages (List[Dict[str, str]]): List of message dictionaries containing 
                'role' and 'content' for the conversation.

        Returns:
            str: The model's response text.

        Raises:
            NotImplementedError: If the subclass doesn't implement this method.
        """

    def prepare_messages(self, message, prompt, history=None):
        """
        Formats the conversation history and current message for API submission.

        Creates a properly formatted message list including system prompt,
        conversation history, and the current user message.

        Args:
            message (str): The current user message to process.
            prompt (str): The system prompt that guides the model's behavior.
            history (list[tuple[str, str]], optional): List of (user, assistant) 
                message pairs from previous interactions.

        Returns:
            list[dict]: List of formatted message dictionaries ready for API submission.
        """
        # Initial system message with the prompt
        messages = [{"role": "system", "content": prompt}]

        # Add conversation history if present
        if history:
            for human, assistant in history:
                messages.append({"role": "user", "content": human})
                messages.append({"role": "assistant", "content": assistant})

        # Add the latest user message
        messages.append({"role": "user", "content": message})

        return messages

    def generate_response(self, message, prompt, history=None):
        """
        Processes user input and generates a model response.

        Handles the complete flow of preparing messages and obtaining
        a response from the model.

        Args:
            message (str): The user's input message to respond to.
            prompt (str): The system prompt that guides the model's behavior.
            history (list[tuple[str, str]], optional): Previous conversation history
                as (user, assistant) message pairs.

        Returns:
            str: The generated response from the model.
        """
        # Prepare messages and call the specific model's API
        messages = self.prepare_messages(message, prompt, history)
        response = self._call_model_api(messages)
        return response