from sweetiepy.data.device_status_repository import DeviceStatusRepository
from sweetiepy.data.glucose_readings_repository import GlucoseReadingsRepository
from sweetiepy.data.mongo_connection import MongoConnection
from sweetiepy.data.profile_repository import ProfileRepository
from sweetiepy.data.treatments_repository import TreatmentsRepository


class DiabetesDataService:
    """
    A service layer that acts as a unified interface for interacting with glucose readings
    and device status data, using the underlying repository pattern.
    """

    def __init__(self, connection: MongoConnection):
        """
        Initializes the class and sets up repositories for glucose readings and device status
        using the provided database connection.

        Args:
            connection (MongoConnection): The database connection used to initialize the
                repositories.
        """
        self.glucose_repo = GlucoseReadingsRepository(connection)
        self.device_repo = DeviceStatusRepository(connection)
        self.profile_repo = ProfileRepository(connection)
        self.treatments_repo = TreatmentsRepository(connection)

    def get_glucose_readings(self, start_time: str = None, end_time: str = None):
        """
        Fetch glucose readings within the specified time range.

        This method retrieves glucose readings from the glucose repository,
        optionally filtered by a defined start and/or end time. If no time range is
        are provided, the most recent two weeks of readings are retrieved.

        Args:
            start_time (str, optional): The starting point of the time range in ISO 8601 format.
                If None, the start time is not limited.
            end_time (str, optional): The ending point of the time range in ISO 8601 format.
                If None, the end time is not limited.

        Returns:
            List[Dict]: A list of dictionaries containing glucose reading data.
        """
        return self.glucose_repo.get_glucose_readings(start_time, end_time)

    def get_device_status(self, start_time: str = None, end_time: str = None):
        """
        Retrieves the status of the device for a specified time range.

        This method fetches the device status from the repository using the
        given time range. If no time range is provided, it retrieves the
        most recent 2 weeks of device status data.

        Args:
            start_time (str, optional): The starting point of the time range in ISO 8601 format.
                If None, the start time is not limited.
            end_time (str, optional): The ending point of the time range in ISO 8601 format.
                If None, the end time is not limited.

        Returns:
            List[Dict]: A list of dictionaries containing device status data for the specified time range.
        """
        return self.device_repo.get_device_status(start_time, end_time)

    def get_profiles(self, start_time: str = None, end_time: str = None):
        """
        Fetch profile data within the specified time range.

        This method retrieves profiles from the profile repository,
        optionally filtered by a defined start and/or end time. If no time range 
        is provided, the repository default behavior will be used.

        Args:
            start_time (str, optional): The starting point of the time range in ISO 8601 format.
                If None, the start time is not limited.
            end_time (str, optional): The ending point of the time range in ISO 8601 format.
                If None, the end time is not limited.

        Returns:
            List[Dict]: A list of dictionaries containing profile data.
        """
        return self.profile_repo.get_profiles(start_time, end_time)

    def get_treatments(self, start_time: str = None, end_time: str = None):
        """
        Fetch treatment data within the specified time range.

        This method retrieves treatments from the treatments repository,
        optionally filtered by a defined start and/or end time. If no time range 
        is provided, the repository default behavior will be used.

        Args:
            start_time (str, optional): The starting point of the time range in ISO 8601 format.
                If None, the start time is not limited.
            end_time (str, optional): The ending point of the time range in ISO 8601 format.
                If None, the end time is not limited.

        Returns:
            List[Dict]: A list of dictionaries containing treatment data.
        """
        return self.treatments_repo.get_treatments(start_time, end_time)


def main():
    """
    Example usage of the DiabetesDataService, demonstrating how a user might interact
    with this module.
    """
    # Database connection configuration
    uri = "mongodb+srv://<db_username>:<db_password>@cluster.example.com"
    username = "username"  # Replace with actual username
    password = "password"  # Replace with actual password

    # Initialize the database connection
    connection = MongoConnection(uri, username, password)
    connection.connect()  # Establish the connection

    try:
        # Initialize the service layer
        service = DiabetesDataService(connection)

        # Fetch and display glucose readings
        print("Fetching glucose readings...")
        glucose_readings = service.get_glucose_readings()
        for reading in glucose_readings:
            print(reading)

        # Fetch and display device statuses
        print("\nFetching device statuses...")
        device_statuses = service.get_device_status()
        for status in device_statuses:
            print(status)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Always close the database connection
        connection.close()


if __name__ == "__main__":
    main()
