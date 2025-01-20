from data.mongo_connection import MongoConnection
from data.utils import parse_time_range, normalize_timestamp


class GlucoseReadingsRepository:
    """
    A repository for retrieving glucose reading data from the MongoDB database.

    This class provides methods to query the `entries` collection in the database
    to fetch glucose reading data within a specific time range. The results are 
    normalized and returned as a list of dictionaries.
    
    Attributes:
        db: A reference to the connected MongoDB database.
    
    Methods:
        get_glucose_readings(start_time: str = None, end_time: str = None):
            Retrieve glucose readings from the database within the specified time range.
    """

    def __init__(self, mongo_connection: MongoConnection):
        """
        Initializes GlucoseReadingsRepository with a MongoConnection instance.
        
        Args:
            mongo_connection (MongoConnection): An instance of MongoConnection.
        
        Attributes:
            db: A reference to the connected MongoDB database.
        """
        self.db = mongo_connection.db

    def get_glucose_readings(self, start_time: str = None, end_time: str = None):
        """
        Retrieve glucose readings from the `entries` collection.
        
        Args:
            start_time (str): Start time for the query in ISO 8601 format. Defaults to None.
            end_time (str): End time for the query in ISO 8601 format. Defaults to None.
        
        Returns:
            List[Dict]: A list of dictionaries containing glucose readings with normalized date strings.
        
        Raises:
            RuntimeError: If the database is not connected or if the query fails.
        """
        if self.db is None:
            raise RuntimeError("Database not connected.")

        # Parse the time range
        start_time_dt, end_time_dt = parse_time_range(start_time, end_time)

        # Query the database
        query = {
            "date": {"$gte": start_time_dt.timestamp() * 1000, "$lte": end_time_dt.timestamp() * 1000}
        }
        fields = {
            "_id": 0,
            "sgv": 1,
            "dateString": 1,
            "trend": 1,
            "direction": 1
        }

        try:
            results = list(self.db["entries"].find(query, fields))
            for result in results:
                if "dateString" in result:
                    result["dateString"] = normalize_timestamp(result["dateString"]).isoformat()
            return results
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve glucose readings: {e}")
