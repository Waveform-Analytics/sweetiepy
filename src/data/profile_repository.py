from data.mongo_connection import MongoConnection
from data.utils import parse_time_range, normalize_timestamp


class ProfileRepository:
    """
    A repository for retrieving profile data from the MongoDB database.

    This class provides methods to query the `profile` collection based on an optional
    time range. It also retrieves the record immediately prior to the specified `start_time`
    if any exist.
    """

    def __init__(self, mongo_connection: MongoConnection):
        """
        Initializes ProfileRepository with a MongoConnection instance.

        Args:
            mongo_connection (MongoConnection): An instance of MongoConnection.
        """
        self.db = mongo_connection.db

    def get_profiles(self, start_time: str = None, end_time: str = None):
        """
        Retrieve profiles from the `profile` collection based on the given time range.

        Args:
            start_time (str): Start time for the query in ISO 8601 format. Defaults to None.
            end_time (str): End time for the query in ISO 8601 format. Defaults to None.

        Returns:
            Dict[str, any]: A list of profiles with normalized timestamps, including the
            one immediately before the given `start_time`.

        Raises:
            RuntimeError: If the database is not connected or if the query fails.
        """
        if self.db is None:
            raise RuntimeError("Database not connected.")

        # Parse the time range
        start_time_dt, end_time_dt = parse_time_range(start_time, end_time)

        try:
            # Query for profiles in the date range
            query = {
                "created_at": {"$gte": start_time_dt.isoformat(), "$lte": end_time_dt.isoformat()}
            }

            # Fetch main range profiles
            profiles_in_range = list(self.db["profile"].find(query).sort("created_at", 1))

            # Query for the single record immediately before the start time
            previous_profile = self.db["profile"].find_one(
                {"created_at": {"$lt": start_time_dt.isoformat()}},
                sort=[("created_at", -1)]
            )

            if previous_profile:
                profiles_in_range.insert(0, previous_profile)  # Add the prior record to the start of the list

            # Normalize timestamps
            for profile in profiles_in_range:
                if "created_at" in profile:
                    profile["created_at"] = normalize_timestamp(profile["created_at"]).isoformat()
            return profiles_in_range
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve profile data: {e}")
