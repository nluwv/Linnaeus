import gradio as gr
import pandas as pd
from Database import Database
from dummy_LLM import LLMManager
from usecase_text import (Usecase_description_samenvatten,
                          Usecase_description_vereenvoudigen,
                          samenvatten_prompt,
                          vereenvoudigen_prompt,
                          anders_prompt)
from gradio_leaderboard import Leaderboard

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
list_other_use_cases = ["classificatie", "standaardiseren", "doelgroep-herschrijven", "brainstorming", "proofreading", "metadateren"]

# Global variables for dummy use 
aangedragen_door = None
beoordelingen = None
uniek = None
best = None
forks = None
lijn = None
specialisatie = None
_type = None
impact = None
sensitiviteit = None


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

    global prompt, stored_usecase, aangedragen_door, beoordelingen, uniek, best, forks, lijn, specialisatie, _type, impact, sensitiviteit
    
    # Set the use case to "samenvatten" and assign the corresponding prompt
    if value == "samenvatten":
        stored_usecase = "samenvatten"
        prompt = samenvatten_prompt

        # dummy
        aangedragen_door = "SVB"
        beoordelingen = 154
        uniek = 13
        forks = 2
        best = 5
        lijn = 2
        specialisatie = 1
        _type = "Summ"
        impact = 2
        sensitiviteit = "S"

    # Set the use case to "vereenvoudigen" and assign the corresponding prompt
    elif value == "vereenvoudigen":
        stored_usecase = "vereenvoudigen"
        prompt = vereenvoudigen_prompt

        # dummy
        aangedragen_door = "SVB"
        beoordelingen = 210
        uniek = 18
        forks = 2
        best = 9
        lijn = 1
        specialisatie = 1
        _type = "Rewrite"
        impact = 3
        sensitiviteit = "S"
    
    elif value in list_other_use_cases:
        stored_usecase = "anders"
        prompt = anders_prompt
    
    # Raise an error if an unsupported use case is provided
    else:
        raise ValueError("Invalid use case value")


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

def on_select(value, evt: gr.SelectData) -> None:
    value = pd.DataFrame(value)
    row_index = evt.index[0]
    selected_element = value.loc[row_index,"Titel"]
    set_usecase(selected_element.lower())
    return f"Wilt u de use case '{selected_element}' selecteren?"

def clear_statement(statement):
    statement = ""
    return statement

# Create interface
with (gr.Blocks() as demo):
    gr.Markdown("## UWV Lineaus")

    # Create tabs to switch between different sections of the interfac
    with gr.Tabs() as tabs:

        # First tab for selecting the use case
        with gr.TabItem(" Select Usecase 🔎", id="Select_Usecases"):
            df = pd.DataFrame({
            "Titel": ["Samenvatten", "Vereenvoudigen", "Classificatie", "Standaardiseren", "Doelgroep-herschrijven", "Brainstorming", "Proofreading", "Metadateren"],
            "Eigenaar": ["A", "A", "B", "A", "C", "B", "D", "C"],
            "Lijn": ["2", "1", "2", "2,1", "2,1", "2", "1,2", "2"],
            "Spec": [1, 1, 1, 1, 2, 1, 2, 3],
            "Type": ["Summ", "Rewr", "Extr", "Rewr", "Rewr", "Gene", "Ana", "Extr"],
            "Impact": [2, 3, 3, 3, 3, 2, 2, 3],
            "Sensitiviteit": ["S", "S", "S", "S", "M", "M", "S", "L"],
            "Nauwkeurigheid": ["M", "L", "L", "M", "M", "S", "M", "XL"],
            "U": [5, 4, 0, 0, 0, 0, 0, 0]
            })

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
                elif choice == "🌱 New":
                    return sort_new(df)
                elif choice == "🚀 Trending":
                    return sort_trending(df)
                elif choice == "⭐ Best":
                    return sort_best(df)
                elif choice == "🤔 Controversial":
                    return sort_controversial(df)
                elif choice == "🌐 Broadness":
                    return sort_broadness(df)
                else:
                    return df

            gr.Markdown("### Filter")
            dropdown = gr.Dropdown(
                choices=["-", "🔥 Hot", "🌱 New", "🚀 Trending", "⭐ Best", "🤔 Controversial", "🌐 Broadness"], 
                label="Choose Filter: 🔥 Hot - 🌱 New - 🚀 Trending - ⭐ Best - 🤔 Controversial - 🌐 Broadness"
            )
            
            dataframe_output = gr.DataFrame(df, datatype=["markdown"])
            dropdown.change(fn=filter_data, inputs=dropdown, outputs=dataframe_output)
            statement = gr.Textbox(label="Use case selecteren")
            dataframe_output.select(on_select, [dataframe_output], statement)

            with gr.Row():
                select_use_case_ja_button = gr.Button("Ja")
                select_use_case_nee_button = gr.Button("Nee")
            select_use_case_ja_button.click(change_tab, gr.Number(1, visible=False), tabs)
            select_use_case_nee_button.click(clear_statement, statement, statement)

        # Second tab for Testing the usecase
        with gr.TabItem("Test Usecase 🚀", id=1):

            # Dummy metadata
            data = {
                'h1': ['**Aangedragen door:**', '**Beoordelingen:**', '**Uniek:**', '**Forks:**', '**Best:**'],
                'h2': ['SVB', '210', '18', '3', '5'],
                'h3': ['**Lijn:**', '**Specialisatie:**', '**Type:**', '**Impact:**', '**Sensitiviteit:**'],
                'h4': ['1', '2', 'Rewrite', '1', 'S']
            }

            with gr.Accordion(label="Omschrijving en metadata", open=False):
                df_meta = pd.DataFrame(data)
                gr.DataFrame(df_meta,
                             elem_classes='gr-dataframe',
                             datatype=["markdown"] * len(df_meta.columns),
                             interactive=False)
                gr.Button("Open in VSCode", icon="https://th.bing.com/th?q=vs+Code+Logo+Black+Background+Small&w=120&h=120&c=1&rs=1&qlt=90&cb=1&pid=InlineBlock&mkt=nl-NL&cc=NL&setlang=en&adlt=moderate&t=1&mw=247", 
                            variant='huggingface')
                    # gr.Button("Open in Colab", icon="data:image/png;base64,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", 
                    #           variant='huggingface')
                gr.Markdown()
                gr.Markdown()

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
            with gr.Blocks():
                model_links = {
                    "model_name": ["Llama 3.2-3b", "GPT4o", "Claude Sonet", "Leesplank Noot"],
                    "links": ["link", "link", "link", "link"]
                }
                
                df_samenvatten_leaderboard = pd.DataFrame({
                "Model": [f'<a target="_blank" href="{model_links["links"][0]}">{model_links["model_name"][0]}</a>', 
                            f'<a target="_blank" href="{model_links["links"][1]}">{model_links["model_name"][1]}</a>',
                            f'<a target="_blank" href="{model_links["links"][2]}">{model_links["model_name"][2]}</a>',
                            f'<a target="_blank" href="{model_links["links"][3]}">{model_links["model_name"][3]}</a>'],
                "Win%": [64, 39, 21, 0],
                "Motivatie": ["readablility, clarity, accuracy, consistency", "accuracy, conciseness, engagement", "conciseness, clarity, comprehensiveness", "lack of accuracy"],
                "€/M": [0.20, 0.52, 0.13, 0.20],
                "Token s/s": [624, 238, 1086, 527],
                "ping (ms)": [75, 105, 40, 75],
                "Race bias": [42.1, 48.6, 35.6, 41.8],
                "Political bias": [32.6, 21.4, 19.7, 35.2],
                "Type": ["Self hosted", "Hosted", "Self hosted", "Self hosted"],
                })

                Leaderboard(
                    value=df_samenvatten_leaderboard,
                    # select_columns=["Model"],
                    search_columns=["Model"],
                    # filter_columns=[],
                    datatype=["markdown"]
                )
                export_samenvatting_button = gr.Button("📤 Export Samenvatting leaderboard naar Excel")
        
            # with gr.Accordion(label="Vereenvoudigen Leaderboard", open=False):
            #         model_links = {
            #             "model_name": ["Leesplank Noot", "Llama 3.2-3b", "Claude Sonet", "GPT4o"],
            #             "links": ["link", "link", "link", "link"]
            #         }
                    
            #         df_vereenvoudigen_leaderboard = pd.DataFrame({
            #         "Model": [f'<a target="_blank" href="{model_links["links"][0]}">{model_links["model_name"][0]}</a>', 
            #                     f'<a target="_blank" href="{model_links["links"][1]}">{model_links["model_name"][1]}</a>',
            #                     f'<a target="_blank" href="{model_links["links"][2]}">{model_links["model_name"][2]}</a>',
            #                     f'<a target="_blank" href="{model_links["links"][3]}">{model_links["model_name"][3]}</a>'],
            #         "Win%": [64, 39, 21, 0],
            #         "Motivatie": ["readablility, clarity, accuracy, consistency", "accuracy, conciseness, engagement", "conciseness, clarity, comprehensiveness", "lack of accuracy"],
            #         "€/M": [0.20, 0.52, 0.13, 0.20],
            #         "Token s/s": [624, 238, 1086, 527],
            #         "ping (ms)": [75, 105, 40, 75],
            #         "Race bias": [42.1, 48.6, 35.6, 41.8],
            #         "Political bias": [32.6, 21.4, 19.7, 35.2],
            #         "Type": ["Self hosted", "Hosted", "Self hosted", "Self hosted"],
            #         })

            #         Leaderboard(
            #             value=df_vereenvoudigen_leaderboard,
            #             # select_columns=["Model"],
            #             search_columns=["Model"],
            #             # filter_columns=[],
            #             datatype=["markdown"]
            #         )
            #         export_samenvatting_button = gr.Button("📤 Export Vereenvoudigen leaderboard naar Excel")



# Launch the interface
demo.launch(share=True)
