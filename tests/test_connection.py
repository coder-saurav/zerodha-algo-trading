import pytest
from unittest.mock import patch
from utils.connection import establish_connection

@patch('utils.connection.os.getenv')
def test_establish_connection_missing_credentials(mock_getenv):
    """
    Tests that establish_connection raises a ValueError if credentials are not set.
    """
    # Arrange: Mock os.getenv to simulate missing credentials
    mock_getenv.return_value = None

    # Act & Assert: Check if ValueError is raised
    with pytest.raises(ValueError) as excinfo:
        establish_connection()

    # Assert that the error message is as expected
    assert "Missing or placeholder API credentials" in str(excinfo.value)

@patch('utils.connection.os.getenv')
def test_establish_connection_placeholder_credentials(mock_getenv):
    """
    Tests that establish_connection raises a ValueError if placeholder credentials are used.
    """
    # Arrange: Mock os.getenv to simulate placeholder values
    mock_getenv.side_effect = ['your_api_key', 'your_api_secret', 'your_access_token']

    # Act & Assert: Check if ValueError is raised
    with pytest.raises(ValueError) as excinfo:
        establish_connection()

    # Assert that the error message is as expected
    assert "Missing or placeholder API credentials" in str(excinfo.value)

@patch('utils.connection.KiteConnect')
@patch('utils.connection.os.getenv')
def test_establish_connection_success(mock_getenv, mock_kiteconnect):
    """
    Tests the success path of establish_connection, mocking the KiteConnect client.
    """
    # Arrange: Mock os.getenv to return valid-looking credentials
    mock_getenv.side_effect = ['myapikey', 'myapisecret', 'myaccesstoken']

    # Arrange: Mock the KiteConnect instance and its profile method
    mock_kite_instance = mock_kiteconnect.return_value
    mock_kite_instance.profile.return_value = {'user_id': 'AB1234'}

    # Act
    kite = establish_connection()

    # Assert
    assert kite is not None
    mock_kiteconnect.assert_called_with(api_key='myapikey')
    kite.set_access_token.assert_called_with('myaccesstoken')
    kite.profile.assert_called_once()
