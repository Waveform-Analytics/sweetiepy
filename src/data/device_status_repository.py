from datetime import timezone, datetime
from data.mongo_connection import MongoConnection
from data.utils import parse_time_range, normalize_timestamp


class DeviceStatusRepository:
    def __init__(self, mongo_connection: MongoConnection):
        """
        Initializes DeviceStatusRepository with a MongoConnection instance.
        """
        self.db = mongo_connection.db

    def get_device_status(self, start_time: str = None, end_time: str = None):

        if self.db is None:
            raise RuntimeError("Database not connected.")

        # Parse the time range into UTC timezone-aware datetime objects
        start_time_dt, end_time_dt = parse_time_range(start_time, end_time)

        # start_time_iso = start_time_dt.isoformat()
        # end_time_iso = end_time_dt.isoformat()

        pipeline = [
            # 1. $addFields: Convert `created_at` string to an actual datetime object
            {
                "$addFields": {
                    "dt_created_at": {
                        "$dateFromString": {
                            "dateString": "$created_at",
                            "timezone": "UTC",
                            "onError": None,  # Avoids errors if `created_at` is invalid or missing
                            "onNull": None  # Handles null cases gracefully
                        }
                    }
                }
            },
            # 2. $match: Filter documents based on the `dt_created_at` field
            {
                "$match": {
                    "dt_created_at": {
                        "$gte": start_time_dt,
                        "$lte": end_time_dt
                    }
                }
            },
            # 3. $project: Customize the final output to include only the relevant fields
            {
                "$project": {
                    "_id": 0,  # Exclude the default MongoDB `_id` field
                    "created_at": 1,  # Include the `created_at` field
                    "device": 1,  # Include the `device` field
                    "pump": 1,  # Include the `pump` field
                    "uploader": 1  # Include the `uploader` field
                }
            }
        ]

        try:
            print(f"Debug: Pipeline => {pipeline}")

            # Retrieve and debug results
            results = list(self.db["devicestatus"].aggregate(pipeline))
            print(f"Debug: Query Results => {results}")

            for record in results:
                if "created_at" in record:
                    record["created_at"] = normalize_timestamp(record["created_at"]).isoformat()
            return results
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve device status: {e}")
