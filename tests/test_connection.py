import pytest
from unittest.mock import patch, Mock
from utils.connection import establish_interactive_connection

@patch('utils.connection.KiteConnect')
@patch('utils.connection.os.getenv')
@patch('builtins.input')
def test_establish_interactive_connection_success(mock_input, mock_getenv, mock_kiteconnect):
    """
    Tests the successful interactive connection flow.
    """
    # Arrange
    # Mock environment variables
    mock_getenv.side_effect = ['my_api_key', 'my_api_secret']

    # Mock the input() call to return a fake request token
    mock_input.return_value = 'my_request_token'

    # Mock the KiteConnect instance and its methods
    mock_kite_instance = mock_kiteconnect.return_value
    mock_kite_instance.login_url.return_value = "http://fake-login-url.com"
    mock_kite_instance.generate_session.return_value = {
        'access_token': 'my_access_token',
        'user_id': 'AB1234'
    }
    mock_kite_instance.profile.return_value = {'user_id': 'AB1234'}

    # Act
    kite = establish_interactive_connection()

    # Assert
    # Check that KiteConnect was initialized correctly
    mock_kiteconnect.assert_called_with(api_key='my_api_key')

    # Check that the login URL was requested
    mock_kite_instance.login_url.assert_called_once()

    # Check that input was called
    mock_input.assert_called_once_with("Enter the request_token here: ")

    # Check that generate_session was called with the correct parameters
    mock_kite_instance.generate_session.assert_called_with(
        'my_request_token', api_secret='my_api_secret'
    )

    # Check that the access token was set
    mock_kite_instance.set_access_token.assert_called_with('my_access_token')

    # Check that the connection was verified
    mock_kite_instance.profile.assert_called_once()

    # Check that the final kite object is returned
    assert kite is not None
    assert kite == mock_kite_instance

@patch('utils.connection.os.getenv')
@patch('builtins.input')
def test_establish_interactive_connection_empty_token(mock_input, mock_getenv):
    """
    Tests that a ValueError is raised if the user provides an empty request token.
    """
    # Arrange
    mock_getenv.side_effect = ['my_api_key', 'my_api_secret']
    mock_input.return_value = '' # Empty input

    # Act & Assert
    with pytest.raises(ValueError) as excinfo:
        establish_interactive_connection()

    assert "Request token cannot be empty" in str(excinfo.value)
