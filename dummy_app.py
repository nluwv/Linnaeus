import gradio as gr
import pandas as pd
from Database import Database
from dummy_LLM import LLMManager
from usecase_text import (Usecase_description_samenvatten,
                          Usecase_description_vereenvoudigen,
                          samenvatten_prompt,
                          vereenvoudigen_prompt)

# Instantiate models
groq_model = "groq_model"
gpt_model = "gpt_model"
mistral_model = "mistral_model"

# Initiate LLMManager, the LLMManager generates output from 2 random models
llm_manager = LLMManager([groq_model, gpt_model, mistral_model])

# Initiate database
db = Database()

# Global variable to store the user's input and model responses
stored_usecase = None
stored_user_input = None
prompt = None
stored_model_a_name = None
stored_model_b_name = None
stored_model_a_response = None
stored_model_b_response = None
feedback = None
stored_user_feedback = None

# Function to set the use case
def set_usecase(value):
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

    global prompt, stored_usecase

    # Set the use case to "samenvatten" and assign the corresponding prompt
    if value == "samenvatten":
        stored_usecase = "samenvatten"
        prompt = samenvatten_prompt

    # Set the use case to "vereenvoudigen" and assign the corresponding prompt
    elif value == "vereenvoudigen":
        stored_usecase = "vereenvoudigen"
        prompt = vereenvoudigen_prompt

    # Raise an error if an unsupported use case is provided
    else:
        pass

    return change_tab(1)


# Function to switch tabs after selecting usecase and pressing the continue button
def change_tab(id):
    return gr.Tabs(selected=id)


# Function to handle the submit action by passing the user input to generate responses
def handle_submit(user_message):
    """
    Generates responses from two randomly selected models by passing the user's input
    to the LLM manager. The selected models and their responses are stored in global
    variables for later use (e.g., writing to a database).

    Args:
        user_message (str): The user's input message that will be sent to the LLMs.

    Returns:
        tuple: A tuple containing the responses from model A and model B, respectively.
    """

    # Declare global variables to store the user input, model names, and responses
    global stored_user_input, \
        stored_model_a_name, \
        stored_model_b_name, \
        stored_model_a_response, \
        stored_model_b_response, \
        prompt

    # Get model names and responses by interacting with the LLM manager using the provided user message and prompt
    model_a_name, model_b_name, model_a_response, model_b_response = llm_manager.chat_with_models(
        user_message, prompt, history=None
    )

    # Store the user input, model names, and responses in global variables for later storage or analysis
    stored_user_input = user_message
    stored_model_a_response = model_a_response
    stored_model_a_name = model_a_name
    stored_model_b_response = model_b_response
    stored_model_b_name = model_b_name

    # Return the responses from model A and model B
    return model_a_response, model_b_response


# Function to set feedback
def set_feedback(value):
    """
    Updates the global feedback variable with the user's provided feedback.

    Args:
        value (str): The feedback provided by the user that will be stored.

    Returns:
        None
    """
    # Declare the global feedback variable to store the user's feedback
    global feedback

    # Assign the user's feedback to the global variable
    feedback = value

    # Print the updated feedback for confirmation
    print(f"Feedback set to: {feedback}")


# Function to handle feedback submission
def handle_feedback(feedback_motivation):
    """
    Logs the user's feedback and related information to the database if all required
    global variables and feedback motivation are provided.

    Args:
        feedback_motivation (str): The user's motivation or explanation behind the feedback.

    Returns:
        None
    """
    # Declare the global variables that store the user input, model names, responses, and feedback
    global stored_user_input, stored_model_a_name, stored_model_b_name, stored_model_a_response, stored_model_b_response, feedback

    # Check if all required variables (input, model names, responses, feedback, and motivation) are available
    if (stored_user_input and stored_model_a_name and stored_model_b_name and
            stored_model_a_response and stored_model_b_response and feedback and feedback_motivation):
        # Log the feedback and related data into the database
        db.log_feedback(stored_usecase, stored_user_input, stored_model_a_name, stored_model_b_name,
                        stored_model_a_response, stored_model_b_response, feedback, feedback_motivation)

        # Confirm successful logging of feedback
        print("Feedback logged successfully.")


# Create interface
with (gr.Blocks() as demo):
    gr.Markdown("## UWV Lineaus")

    # Create tabs to switch between different sections of the interfac
    with gr.Tabs() as tabs:

        # First tab for selecting the use case
        with gr.TabItem("Select Usecase 🔍", id=0):
            # Display descriptions for the two use cases (Samenvatten and Vereenvoudigen)
            with gr.Row():
                gr.Textbox(label="Usecase Samenvatten", lines=5, interactive=False, value=Usecase_description_samenvatten)
                gr.Textbox(label="Usecase Vereenvoudigen", lines=5, interactive=False, value=Usecase_description_vereenvoudigen)


            # Buttons for selecting one of the usecases
            with gr.Row():
                select_samenvatten_button = gr.Button("Selecteer 'Samenvatten' use case")
                select_vereenvoudigen_button = gr.Button("Selecteer 'Vereenvoudigen' use case")

            # Output textbox to display selected prompt
            selected_prompt = gr.Textbox(label="Selected prompt", lines=2, interactive=False)

            # Button actions to update the selected prompt textbox and use_case_input label

            select_samenvatten_button.click(fn=lambda: set_usecase('samenvatten'), inputs=[],
                                            outputs=selected_prompt)
            select_vereenvoudigen_button.click(fn=lambda: set_usecase('vereenvoudigen'), inputs=[],
                                               outputs=selected_prompt)


            # Continue button
            continue_button = gr.Button("Continue")
            # Button action to go to the testing tab after pressing continue
            # continue_button.click(change_tab, gr.Number(1, visible=False), tabs)
            continue_button.click(fn=lambda: set_usecase('samenvatten'), inputs=[], outputs=tabs)

        # Second tab for Testing the usecase
        with gr.TabItem("Test Usecase 🚀", id=1):

            metadata = [[f"Aangedragen door: {''}", "Lijn: "],
                        ["Beoordelingen: ", "Specialisatie: "], 
                        ["Uniek: ", "Type: "],
                        ["Fors: ", "Impact: "],
                        ["Best: ", "Sensitiviteit: "]]
            df_metadata = pd.DataFrame(metadata)

            styled_table = df_metadata.style.hide(axis="index").hide(axis='columns').set_table_styles(
                [{"selector": "table", "props": [("border", "none")],
                  "selector": "td", "props": [("padding", "5px")]}]
            ).to_html()

            with gr.Accordion(label="Omschrijving en metadata", 
                              open=False):
                gr.HTML(styled_table)

            # Two Text boxes to display the models output
            with gr.Row():
                model_a_output = gr.Textbox(label="Model A Output", lines=10, interactive=False)
                model_b_output = gr.Textbox(label="Model B Output", lines=10, interactive=False)

            # Textbox for user input
            use_case_input = gr.Textbox(label="Use Case Input", lines=2, placeholder="Type message hier...")

            # Define the submit button
            submit_button = gr.Button("Submit 🚀")

            # Button action to start generating model responses when user submits their input
            submit_button.click(fn=lambda user_message: handle_submit(user_message),
                                inputs=[use_case_input],
                                outputs=[model_a_output, model_b_output])

            # Add the feedback buttons
            with gr.Row():
                model_a_better_button = gr.Button("Model A is better 👈")
                tie_button = gr.Button("Tie 🤝")
                model_b_better_button = gr.Button("Model B is better 👉")

            # Feedback button actions
            model_a_better_button.click(fn=lambda: set_feedback("Model A is better"), inputs=[], outputs=[])
            model_b_better_button.click(fn=lambda: set_feedback("Model B is better"), inputs=[], outputs=[])
            tie_button.click(fn=lambda: set_feedback("Tie"), inputs=[], outputs=[])
            # both_bad_button.click(fn=lambda: set_feedback("Both are bad"), inputs=[], outputs=[])

            # Feedback text field
            user_feedback_motivation = gr.Textbox(label="Feedback", lines=2, placeholder="Type feedback hier...")

            # Button action to intiate the saving of all global variables to the database
            submit_feedback_button = gr.Button("Submit feedback 📝")
            submit_feedback_button.click(fn=handle_feedback, inputs=[user_feedback_motivation], outputs=[])

        with gr.Tab("Leader board 🏆", id=2):
            leader_board_button = gr.Button("Leader board")

# Launch the interface
demo.launch(share=True)
