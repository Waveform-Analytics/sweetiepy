from sweetiepy.connect_mongodb import MongoConnection


def test_mongo_connection_initialization():
    """
    Test that the MongoConnection initializes with the correct attributes.
    """
    # Setup test parameters
    fake_uri = "mongodb+srv://<db_username>:<db_password>@cluster.example.com"
    fake_username = "test_user"
    fake_password = "test_password"

    # Act
    connection = MongoConnection(uri=fake_uri, username=fake_username, password=fake_password)

    # Assert
    assert connection.uri == "mongodb+srv://test_user:test_password@cluster.example.com"
    assert connection.client is None
    assert connection.db is None
    assert connection.db_name == "myCGMitc"  # Default hardcoded database name
