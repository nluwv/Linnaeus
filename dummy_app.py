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
data = {
    '': ['Aangedragen door: ', aangedragen_door, 'Lijn: ', lijn], 
    '': ['Beoordelingen: ', beoordelingen, 'Specialisatie: ', specialisatie], 
    '': ['Uniek: ', uniek, 'Type: ', _type],
    '': ['Impact: ', impact, 'Sensitiviteit: ', sensitiviteit]
}
data_df = pd.DataFrame(data)
metadata_df = gr.DataFrame(data_df, datatype=["markdown"])


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
    print(value)
    global prompt, stored_usecase, aangedragen_door, beoordelingen, uniek, best, forks, lijn, specialisatie, _type, impact, sensitiviteit
    
    # Set the use case to "samenvatten" and assign the corresponding prompt
    if value == "samenvatten":
        stored_usecase = "samenvatten"
        prompt = samenvatten_prompt

        # dummy
        # aangedragen_door = "SVB"
        # beoordelingen = 154
        # uniek = 13
        # forks = 2
        # best = 5
        # lijn = 2
        # specialisatie = 1
        # _type = "Summ"
        # impact = 2
        # sensitiviteit = "S"

    # Set the use case to "vereenvoudigen" and assign the corresponding prompt
    elif value == "vereenvoudigen":
        stored_usecase = "vereenvoudigen"
        prompt = vereenvoudigen_prompt

        # dummy
        # aangedragen_door = "SVB"
        # beoordelingen = 210
        # uniek = 18
        # forks = 2
        # best = 9
        # lijn = 1
        # specialisatie = 1
        # _type = "Rewrite"
        # impact = 3
        # sensitiviteit = "S"
    
    elif value in list_other_use_cases:
        stored_usecase = "anders"
        prompt = anders_prompt
    
    # Raise an error if an unsupported use case is provided
    else:
        raise ValueError("Ongeldige usecase waarde")
    
    # data = {
    #     '': ['Aangedragen door: ', aangedragen_door, 'Lijn: ', lijn], 
    #     '': ['Beoordelingen: ', beoordelingen, 'Specialisatie: ', specialisatie], 
    #     '': ['Uniek: ', uniek, 'Type: ', _type],
    #     '': ['Impact: ', impact, 'Sensitiviteit: ', sensitiviteit]
    # }
    # return data


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
    print(f"Gegeven feedback: {feedback}")


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
        print("Feedback succesvol geregistreerd.")

def on_select(value, evt: gr.SelectData) -> None:
    value = pd.DataFrame(value)
    row_index = evt.index[0]
    selected_element = value.loc[row_index,"Titel"]
    # data = set_usecase(selected_element.lower()) # hier outputs meegeven
    set_usecase(selected_element.lower())
    # data_df = pd.DataFrame(data)
    # return f"Wilt u de use case '{selected_element}' selecteren?", data_df
    return f"Wilt u de use case '{selected_element}' selecteren?"

def clear_statement(statement):
    statement = ""
    return statement

# Create interface
with (gr.Blocks(css="""
                .gr-dataframe table {border: none; backgorund-color: #f0f0f0;}
                .gr-dataframe th, .gr-dataframe td {border: none; padding: 0px;}
                .gr-dataframe th {display: none;}
                """) as demo):
    gr.Markdown("## UWV Linneaus")

    # Create tabs to switch between different sections of the interfac
    with gr.Tabs() as tabs:

        # First tab for selecting the use case
        with gr.TabItem(" Selecteer Usecase 🔎", id="Select_Usecases"):
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
            dropdown.change(fn=filter_data, inputs=dropdown, outputs=dataframe_output)
            statement = gr.Textbox(label="Usecase selecteren")
            dataframe_output.select(on_select, [dataframe_output], outputs=[statement])

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
                'h4': ['1', '2', 'Summarize', '1', 'S']
            }

            with gr.Accordion(label="Omschrijving en metadata", open=False):
                df_meta = pd.DataFrame(data)
                gr.DataFrame(df_meta,
                             elem_classes='gr-dataframe',
                             datatype=["markdown"] * len(df_meta.columns),
                             interactive=False)
                gr.Button("Open in JupterLab", icon="img/jupyter-svgrepo-com.png", variant='huggingface')


            # Two Text boxes to display the models output
            with gr.Row():
                model_a_output = gr.Textbox(label="Model A Output", lines=10, interactive=False)
                model_b_output = gr.Textbox(label="Model B Output", lines=10, interactive=False)

            # Textbox for user input
            use_case_input = gr.Textbox(label="Invoer Usecase", interactive=True, lines=2, placeholder="Type bericht hier...")

            # Button action to start generating model responses when user submits their input
            use_case_input.submit(fn=lambda user_message: handle_submit(user_message),
                                inputs=[use_case_input],
                                outputs=[model_a_output, model_b_output])
            
            # Add the feedback buttons
            with gr.Row():
                model_a_better_button = gr.Button("👈 Model A is beter")
                tie_button = gr.Button("Gelijkspel 🤝")
                model_b_better_button = gr.Button("Model B is beter 👉")

            # # Feedback text field
            # user_feedback_motivation = gr.Textbox(label="Feedback", lines=2, placeholder="Type feedback hier...")

            # Feedback button actions
            model_a_better_button.click(fn=lambda: set_feedback("Model A is beter"), inputs=[], outputs=[])
            model_b_better_button.click(fn=lambda: set_feedback("Model B is beter"), inputs=[], outputs=[])
            tie_button.click(fn=lambda: set_feedback("Gelijkspel"), inputs=[], outputs=[])
            # both_bad_button.click(fn=lambda: set_feedback("Both are bad"), inputs=[], outputs=[])

            # Feedback text field
            user_feedback_motivation = gr.Textbox(label="Feedback", lines=2, placeholder="Type feedback hier...")

            # Button action to intiate the saving of all global variables to the database
            submit_feedback_button = gr.Button("Verstuur Feedback 📝")
            submit_feedback_button.click(fn=handle_feedback, inputs=[user_feedback_motivation], outputs=[])

        with gr.Tab("Leaderboard 🏆", id=2):
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
                "Type": ["Self hosted", "Hosted online", "Self hosted", "Self hosted"],
                })

                Leaderboard(
                    value=df_samenvatten_leaderboard,
                    search_columns=["Model"],
                    datatype=["markdown"]
                )
                export_samenvatting_button = gr.Button("📤 Export Samenvatten leaderboard naar Excel")
        
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
