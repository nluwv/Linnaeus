import gradio as gr
import pandas as pd

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

    def get_usecases_table(self):
        """
        Reads the usecases from the Excel file and returns them as a pandas DataFrame.

        Returns:
            pd.DataFrame: DataFrame containing the usecases.
        """
        return pd.read_excel("data/usecases.xlsx")

    def _clear_statement(self):
        return ""

    def _on_select(self, value, evt: gr.SelectData) -> str:
        value = pd.DataFrame(value)
        row_index = evt.index[0]
        selected_element = value.loc[row_index,"Titel"]
        self.usecase_manager.set_usecase(selected_element.lower())
        return f"Wilt u de use case '{selected_element}' selecteren?"

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
        with gr.TabItem(" Selecteer Usecase 🔎", id="Select_Usecases"):
            df = self.get_usecases_table()

            # Filter functions
            def sort_hot(df):
                return df.sort_values(by=["Impact", "Sensitiviteit"], ascending=[False, True])
            def sort_new(df):
                return df.sort_values(by="U", ascending=False)
            def sort_trending(df):
                return df.sort_values(by="Impact", ascending=False)
            def sort_best(df):
                return df.sort_values(by=["Nauwkeurigheid", "Impact"], ascending=[False, False])
            def sort_controversial(df):
                return df.sort_values(by=["Spec", "Lijn"], ascending=[False, True])
            def sort_broadness(df):
                return df.sort_values(by="Lijn", key=lambda x: x.str.count(',') + 1, ascending=False)


            def filter_data(choice):
                if choice == "-":
                    return df
                if choice == "🔥 Hot":
                    return sort_hot(df)
                elif choice == "🌱 Nieuw":
                    return sort_new(df)
                elif choice == "🚀 Trending":
                    return sort_trending(df)
                elif choice == "⭐ Beste":
                    return sort_best(df)
                elif choice == "🤔 Controversieel":
                    return sort_controversial(df)
                elif choice == "🌐 Algemeenheid":
                    return sort_broadness(df)
                else:
                    return df

        gr.Markdown("### Filter")
        dropdown = gr.Dropdown(
            choices=["-", "🔥 Hot", "🌱 Nieuw", "🚀 Trending", "⭐ Beste", "🤔 Controversieel", "🌐 Algemeenheid"],
            label="Kies Filter: 🔥 Hot - 🌱 Nieuw - 🚀 Trending - ⭐ Beste - 🤔 Controversieel - 🌐 Algemeenheid"
        )

        dataframe_output = gr.DataFrame(df, datatype=["markdown"])
        dropdown.change(fn=filter_data, inputs=dropdown, outputs=dataframe_output) # pylint:disable=E1101
        statement = gr.Textbox(label="Usecase selecteren")
        dataframe_output.select( # pylint:disable=E1101
            self._on_select,
            [dataframe_output],
            outputs=[statement]
        )

        with gr.Row():
            select_use_case_ja_button = gr.Button("Ja")
            select_use_case_nee_button = gr.Button("Nee")

        select_use_case_ja_button.click( # pylint:disable=E1101
            self._change_tab,
            gr.Number(1, visible=False),
            tabs
        )
        select_use_case_nee_button.click(self._clear_statement, [], statement) # pylint:disable=E1101

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
