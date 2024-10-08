import sqlite3

class Database:
    def __init__(self, db_name='feedback.db'):
        """
        Initializes the Database object and sets up the database connection.

        Parameters:
        db_name (str): The name of the SQLite database file. Defaults to 'feedback.db'.
        """
        self.db_name = db_name
        self._init_db()

    def _init_db(self):
        """
        Initializes the database by creating a table 'feedback_log' if it doesn't already exist.

        The 'feedback_log' table stores feedback data, including model comparisons and user inputs.

        This method commits the changes to the database and closes the connection.
        """
        # Establish connection to the SQLite database
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Create the feedback_log table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedback_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                use_case TEXT,
                user_prompt TEXT,
                model_A TEXT,
                model_b TEXT,
                model_A_response TEXT,
                model_b_response TEXT,
                feedback TEXT,
                feedback_motivation TEXT
            )
        ''')

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

    def log_feedback(self, use_case, user_prompt, model_a, model_b, model_a_response, model_b_response, feedback,
                     feedback_motivation):
        """
        Logs the feedback from a user interaction with two models into the feedback_log table.

        Parameters:
        - use_case (str): A description of the use case or scenario in which the models were used.
        - user_prompt (str): The prompt provided by the user for both models.
        - model_a (str): Name of the first model being evaluated.
        - model_b (str): Name of the second model being evaluated.
        - model_a_response (str): The response generated by model A.
        - model_b_response (str): The response generated by model B.
        - feedback (str): The feedback provided by the user regarding the model responses.
        - feedback_motivation (str): The rationale or motivation behind the given feedback.

        This method inserts a new record into the feedback_log table with the provided parameters and
        commits the transaction to the database.

        Returns:
        None
        """
        # Establish connection to the SQLite database
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Insert the feedback data into the feedback_log table
        cursor.execute('''
            INSERT INTO feedback_log 
            (use_case, user_prompt, model_a, model_b, model_a_response, model_b_response, feedback, feedback_motivation)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
        use_case, user_prompt, model_a, model_b, model_a_response, model_b_response, feedback, feedback_motivation))

        # Commit the changes to the database and close the connection
        conn.commit()
        conn.close()
