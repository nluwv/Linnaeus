import os
from db import BaseDB
from utils import persistent_path


class FeedbackDB(BaseDB):
    """
    A class to interact with the feedback database.

    Note: make sure to update _setup_database() when changing the database
    schema in the Feedback model.
    """

    def __init__(
        self,
        table_name: str = "feedback",
        db_path: str = persistent_path("feedback/database.db"),
    ):
        """
        Initializes the FeedbackDB class.
        """
        super().__init__(table_name=table_name, db_path=db_path)
        self._setup_database()

    def _setup_database(self) -> None:
        """
        Creates a database to save any feedback given by the user.
        """
        
        # Connect to SQLite database (if it doesn't exist, it will be created)
        db_dir = os.path.dirname(self._db_path)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
            
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {self._table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            use_case TEXT,
            user_prompt TEXT,
            model_A TEXT,
            model_b TEXT,
            model_A_response TEXT,
            model_b_response TEXT,
            feedback TEXT,
            feedback_motivation TEXT
        );
        """

        self.query(create_table_query)
