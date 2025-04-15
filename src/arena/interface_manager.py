import gradio as gr
from usecase_manager import UsecaseManager
from feedback_handler import FeedbackHandler
from llm import LLMManager
from arena.config import Config
from db.feedback import FeedbackDB

class InterfaceManager:
    def __init__(self, config: Config):
        self.usecase_manager = UsecaseManager()
        self.llm_manager = LLMManager(config.get_models())
        self.feedback_handler = FeedbackHandler(FeedbackDB())

        self._usecase = None
        self._prompt = None
        self._given_feedback = None

        self.demo = self._create_interface()

    def _create_interface(self):
        with gr.Blocks() as demo:
            gr.Markdown("## UWV Lineaus")
            
            with gr.Tabs() as tabs:
                with gr.TabItem("Select Usecase", id=0):
                    self._create_usecase_tab(tabs)
                
                with gr.TabItem("Test Usecase", id=1):
                    self._create_test_tab()
                
                with gr.Tab("Leader board"):
                    self._create_leaderboard_tab()
        
        return demo

    def _set_usecase(self, value: str) -> str:
        """
        Retrieves the appropriate prompt for the selected use case and stores
        the selected use case value in a global variable for later use in a database.

        Args:
            value (str): The name of the use case to select. Expected values are
                        "samenvatten" or "vereenvoudigen".

        Returns:
            str: The corresponding prompt based on the selected use case.

        Raises:
            ValueError: If the provided use case value is invalid.
        """

        # Set the use case to "samenvatten" and assign the corresponding prompt
        if value == "samenvatten":
            self._usecase = "samenvatten"
            self._prompt = self.usecase_manager.get_samenvatten_prompt()
            return self._prompt

        # Set the use case to "vereenvoudigen" and assign the corresponding prompt
        elif value == "vereenvoudigen":
            self._usecase = "vereenvoudigen"
            self._prompt = self.usecase_manager.get_vereenvoudigen_prompt()
            return self._prompt

        # Raise an error if an unsupported use case is provided
        else:
            raise ValueError("Invalid use case value")

    def _handle_user_submit(self, user_message: str):
        """
        Handle the user submit action by passing the user input to generate responses.
        """
        # Get model names and responses by interacting with the LLM manager using the provided user message and prompt
        model_a_name, model_b_name, model_a_response, model_b_response = self.llm_manager.chat_with_models(
            user_message, self._prompt, history=None
        )

        # Store the user input, model names, and responses in global variables for later storage or analysis
        stored_user_input = user_message
        stored_model_a_response = model_a_response
        stored_model_a_name = model_a_name
        stored_model_b_response = model_b_response
        stored_model_b_name = model_b_name

        # Return the responses from model A and model B
        return model_a_response, model_b_response

    def _set_feedback_value(self, value: str) -> None:
        """
        Set the feedback value based on the button clicked.
        """
        self._given_feedback = value

    def _add_feedback(self, feedback):
        pass

    def _create_usecase_tab(self, tabs):
        # Display descriptions for the two use cases (Samenvatten and Vereenvoudigen)
        with gr.Row():
            gr.Textbox(label="Usecase Samenvatten", lines=5, interactive=False, value=self.usecase_manager.get_usecase_descr_samenvatten())
            gr.Textbox(label="Usecase Vereenvoudigen", lines=5, interactive=False, value=self.usecase_manager.get_usecase_descr_vereenvoudigen())

        # Buttons for selecting one of the usecases
        with gr.Row():
            select_samenvatten_button = gr.Button("Selecteer 'Samenvatten' use case")
            select_vereenvoudigen_button = gr.Button("Selecteer 'Vereenvoudigen' use case")

        # Output textbox to display selected prompt
        selected_prompt = gr.Textbox(label="Selected prompt", lines=2, interactive=False)

        # Button actions to update the selected prompt textbox and use_case_input label
        select_samenvatten_button.click(fn=self._set_usecase('samenvatten'), inputs=[],
                                        outputs=selected_prompt)
        select_vereenvoudigen_button.click(fn=self._set_usecase('vereenvoudigen'), inputs=[],
                                            outputs=selected_prompt)

        # Continue button
        continue_button = gr.Button("Continue")

        # Button action to go to the testing tab after pressing continue
        continue_button.click(change_tab, gr.Number(1, visible=False), tabs)

    def _create_test_tab(self):
        # Two Text boxes to display the models output
        with gr.Row():
            model_a_output = gr.Textbox(label="Model A Output", lines=10, interactive=False)
            model_b_output = gr.Textbox(label="Model B Output", lines=10, interactive=False)

        # Textbox for user input
        use_case_input = gr.Textbox(label="Use Case Input", lines=2, placeholder="Type message hier...")

        # Define the submit button
        submit_button = gr.Button("Submit")

        # Button action to start generating model responses when user submits their input
        submit_button.click(fn=lambda user_message: handle_submit(user_message),
                            inputs=[use_case_input],
                            outputs=[model_a_output, model_b_output])

        # Add the feedback buttons
        with gr.Row():
            model_a_better_button = gr.Button("Model A is better")
            model_b_better_button = gr.Button("Model B is better")
            tie_button = gr.Button("Tie")

        # Feedback button actions
        model_a_better_button.click(fn=self._set_feedback_value("Model A is better"), inputs=[], outputs=[])
        model_b_better_button.click(fn=self._set_feedback_value("Model B is better"), inputs=[], outputs=[])
        tie_button.click(fn=self._set_feedback_value("Tie"), inputs=[], outputs=[])

        # Feedback text field
        user_feedback_motivation = gr.Textbox(label="Feedback", lines=2, placeholder="Type feedback hier...")

        # Button action to intiate the saving of all global variables to the database
        submit_feedback_button = gr.Button("Submit feedback")
        submit_feedback_button.click(fn=self._add_feedback, inputs=[user_feedback_motivation], outputs=[])


    def _create_leaderboard_tab(self):
        leader_board_button = gr.Button("Leader board")
