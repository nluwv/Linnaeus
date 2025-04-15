import gradio as gr

from src.llm import LLMManager
from src.db import Database

from .config import Config
from .usecase_manager import UsecaseManager
from .feedback_handler import FeedbackHandler

class InterfaceManager:
    def __init__(self, config: Config) -> None:
        self.usecase_manager = UsecaseManager()
        self.llm_manager = LLMManager(config.get_models())
        self.feedback_handler = FeedbackHandler(Database(db_name="feedback"))
        self.demo = self._create_interface()

    def _change_tab(self, _id: gr.Number) -> gr.Tabs:
        return gr.Tabs(selected=_id)

    def _create_interface(self) -> gr.Blocks:
        with gr.Blocks() as demo:
            gr.Markdown("## UWV Lineaus")
            
            with gr.Tabs() as tabs:
                with gr.TabItem("Select Usecase", id=0):
                    self._create_select_usecase_tab(tabs)
                
                with gr.TabItem("Test Usecase", id=1):
                    self._create_test_usecase_tab()
                
                with gr.Tab("Leader board"):
                    self._create_leaderboard_tab()
        
        return demo

    def _create_select_usecase_tab(self, tabs):
        # Display descriptions for the two use cases (Samenvatten and Vereenvoudigen)
        with gr.Row():
            gr.Textbox(label="Usecase Samenvatten", lines=5, interactive=False, value=self.usecase_manager.get_samenvatten_description)
            gr.Textbox(label="Usecase Vereenvoudigen", lines=5, interactive=False, value=self.usecase_manager.get_vereenvoudigen_description)


        # Buttons for selecting one of the usecases
        with gr.Row():
            select_samenvatten_button = gr.Button("Selecteer 'Samenvatten' use case")
            select_vereenvoudigen_button = gr.Button("Selecteer 'Vereenvoudigen' use case")

        # Output textbox to display selected prompt
        selected_prompt = gr.Textbox(label="Selected prompt", lines=2, interactive=False)

        # Button actions to update the selected prompt textbox and use_case_input label
        select_samenvatten_button.click(fn=lambda: self.usecase_manager.set_usecase('samenvatten'), inputs=[], # pylint:disable=E1101
                                        outputs=selected_prompt)
        select_vereenvoudigen_button.click(fn=lambda: self.usecase_manager.set_usecase('vereenvoudigen'), inputs=[], # pylint:disable=E1101
                                            outputs=selected_prompt)

        # Continue button
        continue_button = gr.Button("Continue")
        continue_button.click(self._change_tab, inputs=gr.Number(1, visible=False), outputs=tabs) # pylint:disable=E1101

    def _create_test_usecase_tab(self):
        # Display the models output
        with gr.Row():
            model_a_output = gr.Textbox(label="Model A Output", lines=10, interactive=False)
            model_b_output = gr.Textbox(label="Model B Output", lines=10, interactive=False)

        # Textbox for user input
        use_case_input = gr.Textbox(label="Use Case Input", lines=2, placeholder="Type message hier...")

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
        model_a_better_button.click(fn=lambda: self.feedback_handler.set_feedback("Model A is beter"), inputs=[], outputs=[]) # pylint:disable=E1101
        model_b_better_button.click(fn=lambda: self.feedback_handler.set_feedback("Model B is beter"), inputs=[], outputs=[]) # pylint:disable=E1101
        tie_button.click(fn=lambda: self.feedback_handler.set_feedback("Gelijkspel"), inputs=[], outputs=[]) # pylint:disable=E1101

        # Feedback text field
        user_feedback_motivation = gr.Textbox(label="Feedback", lines=2, placeholder="Type feedback hier...")

        # Button action to intiate the saving of all global variables to the database
        submit_feedback_button = gr.Button("Submit feedback")
        submit_feedback_button.click(fn=self.feedback_handler.submit_feedback, inputs=[user_feedback_motivation], outputs=[]) # pylint:disable=E1101


    def _create_leaderboard_tab(self):
        # ...existing leaderboard tab code...
        pass
