import os
from sweetiepy.connect_mongodb import MongoConnection, DiabetesDataService


def main():
    """
    Demonstration of how to use the DiabetesDataService library with environment variables,
    tailored to the DIY Loop system.
    """

    # Fetch credentials from environment variables
    env_uri = os.getenv("MONGODB_URI")
    env_username = os.getenv("MONGODB_USERNAME")
    env_password = os.getenv("MONGODB_PASSWORD")

    # Fallback to manual input if environment variables are not fully configured
    if not env_uri or not env_username or not env_password:
        print("Environment variables not fully configured. Falling back to manual input.")

        # Prompt user for URI, username, and password manually
        env_uri = input("Enter MongoDB URI (with <db_username> and <db_password> placeholders): ")
        env_username = input("Enter MongoDB username: ")
        env_password = input("Enter MongoDB password: ")

        print("⚠️ Avoid hardcoding sensitive credentials in scripts. Environment variables are recommended.")

    # Use the service-layer-based library
    connection = MongoConnection(uri=env_uri, username=env_username, password=env_password)

    try:
        # Connect to the database
        connection.connect()

        # Create a service instance to interact with the data
        service = DiabetesDataService(connection)

        # Fetch and display glucose readings
        print("\nFetching glucose readings...")
        glucose_data = service.get_glucose_readings()
        for reading in glucose_data:
            print(reading)

        # Fetch and display device statuses
        print("\nFetching device statuses...")
        device_statuses = service.get_device_status()
        for status in device_statuses:
            print(status)

        # Fetch and display profile data
        print("\nFetching profile data...")
        profiles = service.get_profiles()
        for profile in profiles:
            print(profile)

        # Fetch and display treatment data
        print("\nFetching treatments...")
        treatments = service.get_treatments()
        for treatment in treatments:
            print(treatment)

        print('pause here')

    except Exception as error:
        print(f"Error encountered: {error}")
    finally:
        connection.close()


if __name__ == "__main__":
    main()
