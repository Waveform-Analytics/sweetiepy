import os
from src.connect_mongodb import DatabaseConnection


def main():
    """
    Demonstration of how to use the DatabaseConnection library with environment variables,
    tailored to the DIY Loop system.
    """

    # Fetch credentials from environment variables
    env_uri = os.getenv("MONGODB_URI")
    env_username = os.getenv("MONGODB_USERNAME")
    env_password = os.getenv("MONGODB_PASSWORD")

    if not env_uri or not env_username or not env_password:
        print("Environment variables not fully configured.")
        print("Falling back to manual input.")

        # Prompt user for URI, username, and password manually
        env_uri = input("Enter MongoDB URI (with <db_username> and <db_password> placeholders): ")
        env_username = input("Enter MongoDB username: ")
        env_password = input("Enter MongoDB password: ")

        print("⚠️ Avoid hardcoding sensitive credentials in scripts. Environment variables are recommended.")

    # Use DatabaseConnection from the library
    db_connection = DatabaseConnection(
        uri=env_uri,
        username=env_username,
        password=env_password,
    )

    try:
        # Connect to the database
        db_connection.connect()

        # Fetch and display glucose readings
        glucose_data = db_connection.get_glucose_readings()
        print("\nGlucose Readings:")
        for reading in glucose_data:
            print(reading)

        # Fetch and display device status
        device_status = db_connection.get_device_status()
        print("\nDevice Status:")
        for status in device_status:
            print(status)

        # Fetch and display user settings
        settings = db_connection.get_settings()
        print("\nSettings:")
        for setting in settings:
            print(setting)

    except Exception as error:
        print("Error:", error)
    finally:
        # Ensure the connection is closed
        db_connection.close()


if __name__ == "__main__":
    main()
