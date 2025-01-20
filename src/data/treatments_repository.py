from data.mongo_connection import MongoConnection
from data.utils import parse_time_range, normalize_timestamp


class TreatmentsRepository:
    """
    A repository for retrieving treatment data from the MongoDB database.
    """

    def __init__(self, mongo_connection: MongoConnection):
        """
        Initializes TreatmentsRepository with a MongoConnection instance.

        Args:
            mongo_connection (MongoConnection): An instance of MongoConnection.
        """
        self.db = mongo_connection.db

    def get_treatments(self, start_time: str = None, end_time: str = None):
        """
        Retrieve treatments from the `treatments` collection based on a time range.

        Args:
            start_time (str): Start time for the query in ISO 8601 format. Defaults to None.
            end_time (str): End time for the query in ISO 8601 format. Defaults to None.

        Returns:
            List[Dict]: A list of dictionaries containing treatment data with normalized timestamps.

        Raises:
            RuntimeError: If the database is not connected or if the query fails.
        """
        if self.db is None:
            raise RuntimeError("Database not connected.")

        # Parse the time range
        start_time_dt, end_time_dt = parse_time_range(start_time, end_time)

        # Query the database
        query = {
            "created_at": {"$gte": start_time_dt.isoformat(), "$lte": end_time_dt.isoformat()}
        }
        fields = {
            "_id": 0,
            "insulinType": 1,
            "amount": 1,
            "duration": 1,
            "created_at": 1,
            "eventType": 1
        }

        try:
            results = list(self.db["treatments"].find(query, fields))
            for result in results:
                if "created_at" in result:
                    result["created_at"] = normalize_timestamp(result["created_at"]).isoformat()
            return results
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve treatment data: {e}")
