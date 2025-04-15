from abc import abstractmethod
import sqlite3
import os
import pandas as pd


class BaseDB:
    """
    A class to interact with the database.

    Note: make sure to update _setup_database() when changing the database
    schema in the Feedback model.
    """

    _table_name: str = ""
    _db_path: str = ""

    def __init__(self, table_name: str = "", db_path: str = ""):
        """
        Initializes the Base DB class.
        """
        self._table_name = table_name
        self._db_path = db_path
        self._setup_database()

    @abstractmethod
    def _setup_database(self):
        """
        Creates a database to save any feedback given by the user.
        """
        # Connect to SQLite database (if it doesn't exist, it will be created)
        db_dir = os.path.dirname(self._db_path)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)

    def create_entry(self, table):
        """
        Creates a new entry in the database.
        """

        # Get the properties of the Feedback class
        properties = [prop for prop in dir(table) if not prop.startswith("__")]

        # Generate the column names and placeholders for the SQL query
        columns = ", ".join(properties)
        placeholders = ", ".join(["?"] * len(properties))

        # Generate the insert query
        insert_query = f"""
        INSERT INTO {self._table_name} ({columns})
        VALUES ({placeholders});
        """

        # Get the values of the properties
        values = [getattr(table, prop) for prop in properties]

        return self.query(insert_query, tuple(values))

    def get_entry_by(self, column: str, value: str):
        """
        Retrieves a feedback entry from the database by a given column and value.
        """

        # Generate the select query
        select_query = f"""
        SELECT * FROM {self._table_name}
        WHERE {column} = ?;
        """

        result = self.query(select_query, (value,))
        if len(result) == 0:
            return None
        else:
            return result[0]

    def get_all_entries(self) -> pd.DataFrame:
        """
        Retrieves all feedback entries from the database and returns a pandas DataFrame.

        Example:
        >>> feedback_db = FeedbackDB()
        >>> df = feedback_db.get_all_feedback()
        >>> st.dataframe(df, hide_index=True)
        """

        # Generate the select query
        select_query = f"""
        SELECT * FROM {self._table_name}
        ORDER BY date_created DESC;
        """

        result = self.query(select_query)

        # Get the column names of the feedback table
        columns = [
            description[1]
            for description in self.query(f"PRAGMA table_info({self._table_name});")
        ]

        return pd.DataFrame(result, columns=columns)

    def query(self, query: str, params: tuple = ()) -> list:
        """
        Executes a query on the database and returns the result.
        """
        # Connect to SQLite database
        conn = sqlite3.connect(self._db_path)

        # Create a cursor object using the cursor() method
        cursor = conn.cursor()

        # Execute the SQL query
        cursor.execute(query, params)

        # Get the result of the query
        result = cursor.fetchall()

        # Commit the transaction
        conn.commit()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        return result
