import random
from typing import List

class LLMManager:
    """
    A manager class for handling multiple Language Learning Models (LLMs).
    
    This class provides functionality to:
    - Manage multiple LLM instances
    - Select random pairs of models for comparison
    - Generate responses from multiple models for the same input
    
    The manager ensures that responses can be generated and compared across
    different LLM implementations while maintaining a consistent interface.
    
    Attributes:
        models (List[str]): A list of LLM model instances that implement
            the base LLM interface.
    """
    
    def __init__(self, models: List[str]):
        """
        Initializes the LLM manager with a list of available model instances.

        Args:
            models (list): List of LLMBase model instances.
        """
        self.models = models
        self.model_a_name = None
        self.model_b_name = None

    def chat_with_models(self, message, prompt, history=None):
        """
        Sends a message to two randomly selected models.

        Args:
            message (str): The user's input message.
            prompt (str): The system's initial prompt.
            history (list of tuples): Previous conversation history as (user_message, assistant_message).

        Returns:
            tuple: Model A name, Model B name, Model A response, Model B response.
        """
        if len(self.models) < 2:
            raise ValueError("At least two models are required to chat.")

        # Randomly select 2 models from the list
        selected_models = random.sample(self.models, 2)

        model_a_response, model_b_response = None, None

        for i, model in enumerate(selected_models):
            model_name = model.__class__.__name__
            response = model.generate_response(message, prompt, history)
            print(f'Response for {model_name} was generated')

            # Store the model names and responses
            if i == 0:
                self.model_a_name = model_name
                model_a_response = response
            else:
                self.model_b_name = model_name
                model_b_response = response

        return model_a_response, model_b_response
