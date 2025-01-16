from datetime import datetime, timedelta
from pymongo import MongoClient
from pymongo.server_api import ServerApi


class DatabaseConnection:
    def __init__(self, uri: str, username: str, password: str):
        """
        Initialize the database connection.

        :param uri: MongoDB connection URI with placeholders for <db_username> and <db_password>
        :param username: Username for authentication
        :param password: Password for authentication
        """
        self.uri = uri.replace("<db_username>", username).replace("<db_password>", password)
        self.client = None
        self.db = None

    def connect(self):
        """
        Establish a connection to the MongoDB database.
        """
        try:
            self.client = MongoClient(self.uri, server_api=ServerApi('1'))
            # Hardcode the database name as 'myCGMitc'
            self.db = self.client["myCGMitc"]
            print(f"Connected to database: myCGMitc")
        except Exception as e:
            raise RuntimeError(f"Failed to connect to MongoDB: {e}")

    def close(self):
        """
        Close the connection to the database.
        """
        if self.client:
            self.client.close()
            print("Connection closed.")

    def get_glucose_readings(self, start_time: str = None, end_time: str = None):
        """
        Retrieve glucose readings (CGM values) from the `myCGMitc.entries` collection.

        :param start_time: Start time for the query (in ISO 8601 format: yyyy-mm-ddTHH:MM:SS),
                           optional, defaults to two weeks ago.
        :param end_time: End time for the query (in ISO 8601 format: yyyy-mm-ddTHH:MM:SS),
                         optional, defaults to the current time.
        :return: A list of dictionaries with keys: 'sgv', 'dateString', 'trend', 'direction'.

        Example Output:
        [
            {"sgv": 110, "dateString": "2023-10-01T12:34:56.000Z", "trend": 4, "direction": "Flat"},
            ...
        ]
        """
        if self.db is None:
            raise RuntimeError("Database not connected. Call `connect` first.")

        # Default to the most recent two weeks
        if not end_time:
            end_time = datetime.utcnow()  # Current UTC time
        else:
            try:
                end_time = datetime.fromisoformat(end_time.replace("Z", "+00:00"))
            except ValueError:
                raise ValueError("Invalid end_time format. Use ISO 8601 format (e.g., 2023-10-01T12:34:56Z).")

        if not start_time:
            start_time = end_time - timedelta(weeks=2)  # 2 weeks before the end time
        else:
            try:
                start_time = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
            except ValueError:
                raise ValueError("Invalid start_time format. Use ISO 8601 format (e.g., 2023-10-01T12:34:56Z).")

        # Validate that start_time is before end_time
        if start_time >= end_time:
            raise ValueError("Start time must be earlier than end time.")

        # Query preparation
        query = {
            "date": {"$gte": start_time.timestamp() * 1000, "$lte": end_time.timestamp() * 1000}
            # Dates in milliseconds
        }
        fields = {
            "_id": 0,  # Exclude the MongoDB ID
            "sgv": 1,  # Blood glucose value
            "dateString": 1,  # ISO 8601 formatted timestamp
            "trend": 1,  # Integer trend value (e.g., 4 = Flat)
            "direction": 1  # Text trend direction (e.g., "Flat")
        }

        try:
            # Perform the query with filters and projections
            results = list(self.db["entries"].find(query, fields))  # Access the 'entries' collection
            return results
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve glucose readings: {e}")

    def get_device_status(self):
        """
        Retrieve device status data from the `myCGMitc.device_status` collection.

        Example: Device-specific settings, battery status, etc.
        """
        if not self.db:
            raise RuntimeError("Database not connected. Call `connect` first.")
        return list(self.db["device_status"].find({}, {"_id": 0}))

    def get_settings(self):
        """
        Retrieve user/Loop system settings from the `myCGMitc.settings` collection.

        Example: This may include basal rate configurations, carb ratios, etc.
        """
        if not self.db:
            raise RuntimeError("Database not connected. Call `connect` first.")
        return list(self.db["settings"].find({}, {"_id": 0}))


if __name__ == "__main__":
    print("This script is intended to be imported as a library.")