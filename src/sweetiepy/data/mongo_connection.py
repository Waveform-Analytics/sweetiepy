from pymongo import MongoClient
from pymongo.server_api import ServerApi


class MongoConnection:
    def __init__(self, uri: str, username: str, password: str):
        """
        Initializes the database connection.
        
        Args:
            uri (str): MongoDB connection URI with placeholders for <db_username> and <db_password>.
            username (str): Username for authentication.
            password (str): Password for authentication.
        """
        self.uri = uri.replace("<db_username>", username).replace("<db_password>", password)
        self.client = None
        self.db = None
        self.db_name = "myCGMitc"  # Hardcoded database name

    def connect(self):
        """Establish a connection to MongoDB."""
        try:
            self.client = MongoClient(self.uri, server_api=ServerApi('1'))
            self.db = self.client[self.db_name]
            print(f"Connected to database: {self.db_name}")
        except Exception as e:
            raise RuntimeError(f"Failed to connect to MongoDB: {e}")

    def close(self):
        """Close the connection to the MongoDB database."""
        if self.client:
            self.client.close()
            print("Database connection closed.")
