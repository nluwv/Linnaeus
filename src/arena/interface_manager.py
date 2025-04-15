import gradio as gr

from src.llm import LLMManager
from src.db.feedback import FeedbackDB

from .config import Config
from .usecase_manager import UsecaseManager
from .feedback_handler import FeedbackHandler

class InterfaceManager:
    """
    Manages the Gradio-based user interface, connecting the UI components to application logic.
    Responsible for creating and organizing the interface tabs and handling user interactions.
    """

    def __init__(self, config: Config) -> None:
        """
        Initialize the InterfaceManager with necessary components.

        Args:
            config (Config): Configuration object containing API keys and model setup.
        """
        self.usecase_manager = UsecaseManager()
        self.llm_manager = LLMManager(config.get_models())
        self.feedback_handler = FeedbackHandler(FeedbackDB())
        self.demo = self._create_interface()

    def _change_tab(self, _id: gr.Number) -> gr.Tabs:
        """
        Change the currently selected tab in the interface.

        Args:
            _id (gr.Number): The ID of the tab to select.

        Returns:
            gr.Tabs: The updated Tabs component with the selected tab.
        """
        return gr.Tabs(selected=_id)

    def _create_interface(self) -> gr.Blocks:
        """
        Create the complete Gradio interface with all tabs and components.

        Returns:
            gr.Blocks: The configured Gradio Blocks interface.
        """
        with gr.Blocks() as demo:
            gr.Markdown("## UWV Lineaus")

            with gr.Tabs() as tabs:
                with gr.TabItem("Selecteer Usecase 🔎", id="Select_Usecases"):
                    self._create_select_usecase_tab(tabs)

                with gr.TabItem("Test Usecase 🚀", id=1):
                    self._create_test_usecase_tab()

                with gr.Tab("Leaderboard 🏆", id=2):
                    self._create_leaderboard_tab()

        return demo

    def _create_select_usecase_tab(self, tabs):
        """
        Create the tab for selecting a use case.

        Args:
            tabs (gr.Tabs): The tabs component for navigation between tabs.
        """
        # Display descriptions for the two use cases (Samenvatten and Vereenvoudigen)
        with gr.Row():
            gr.Textbox(
                label="Usecase Samenvatten",
                lines=5,
                interactive=False,
                value=self.usecase_manager.get_samenvatten_description
            )
            gr.Textbox(
                label="Usecase Vereenvoudigen",
                lines=5,
                interactive=False,
                value=self.usecase_manager.get_vereenvoudigen_description
            )


        # Buttons for selecting one of the usecases
        with gr.Row():
            select_samenvatten_button = gr.Button("Selecteer 'Samenvatten' use case")
            select_vereenvoudigen_button = gr.Button("Selecteer 'Vereenvoudigen' use case")

        # Output textbox to display selected prompt
        selected_prompt = gr.Textbox(label="Selected prompt", lines=2, interactive=False)

        # Button actions to update the selected prompt textbox and use_case_input label
        select_samenvatten_button.click( # pylint:disable=E1101
            fn=lambda: self.usecase_manager.set_usecase('samenvatten'),
            inputs=[],
            outputs=selected_prompt
        )
        select_vereenvoudigen_button.click( # pylint:disable=E1101
            fn=lambda: self.usecase_manager.set_usecase('vereenvoudigen'),
            inputs=[],
            outputs=selected_prompt
        )

        # Continue button
        continue_button = gr.Button("Continue")
        continue_button.click(self._change_tab, inputs=gr.Number(1, visible=False), outputs=tabs) # pylint:disable=E1101

    def _create_test_usecase_tab(self):
        """
        Create the tab for testing the selected use case with language models.
        This tab allows users to input text, submit it to the models, and provide feedback
        on the quality of the model responses.
        """
        # Display the models output
        with gr.Row():
            model_a_output = gr.Textbox(label="Model A Output", lines=10, interactive=False)
            model_b_output = gr.Textbox(label="Model B Output", lines=10, interactive=False)

        # Textbox for user input
        use_case_input = gr.Textbox(
            label="Use Case Input",
            lines=2,
            placeholder="Type message hier..."
        )

        # Submit button
        submit_button = gr.Button("Submit")

        # Button action to start generating model responses when user submits their input
        submit_button.click( # pylint:disable=E1101
            fn=lambda user_message: self.llm_manager.chat_with_models(
                self.usecase_manager.get_current_prompt(), user_message
            ),
            inputs=[use_case_input],
            outputs=[model_a_output, model_b_output]
        )

       # Add the feedback buttons
        with gr.Row():
            model_a_better_button = gr.Button("👈 Model A is beter")
            tie_button = gr.Button("Gelijkspel 🤝")
            model_b_better_button = gr.Button("Model B is beter 👉")

        # Feedback button actions
        model_a_better_button.click( # pylint:disable=E1101
            fn=lambda: self.feedback_handler.set_feedback("Model A is beter"),
            inputs=[],
            outputs=[]
        )
        model_b_better_button.click( # pylint:disable=E1101
            fn=lambda: self.feedback_handler.set_feedback("Model B is beter"),
            inputs=[],
            outputs=[]
        )
        tie_button.click( # pylint:disable=E1101
            fn=lambda: self.feedback_handler.set_feedback("Gelijkspel"),
            inputs=[],
            outputs=[]
        )

        # Feedback text field
        user_feedback_motivation = gr.Textbox(
            label="Feedback",
            lines=2,
            placeholder="Type feedback hier..."
        )

        # Button action to intiate the saving of all global variables to the database
        submit_feedback_button = gr.Button("Submit feedback")
        submit_feedback_button.click( # pylint:disable=E1101
            fn=self.feedback_handler.submit_feedback,
            inputs=[user_feedback_motivation],
            outputs=[]
        )


    def _create_leaderboard_tab(self):
        """
        Create the tab for displaying the leaderboard of model performance.
        Shows performance metrics and comparison results between different models.
        """
        # ...existing leaderboard tab code...
