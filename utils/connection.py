import logging
import os
from kiteconnect import KiteConnect
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def establish_interactive_connection():
    """
    Establishes a connection to the Kite API by interactively prompting the
    user for a request_token.

    Returns:
        KiteConnect object if successful.

    Raises:
        ValueError: If API key/secret are not found in the environment.
        Exception: For other Kite Connect API exceptions during session generation.
    """
    api_key = os.getenv('KITE_API_KEY')
    api_secret = os.getenv('KITE_API_SECRET')

    if not all([api_key, api_secret]) or "your_" in api_key:
        logger.error("API key/secret not found or are placeholders in .env file.")
        raise ValueError("Missing or placeholder API key/secret. Please update your .env file.")

    kite = KiteConnect(api_key=api_key)

    # 1. Generate and print the login URL
    print("\n--- Interactive Login Required ---")
    print("1. Please login to Kite and authorize the app to get the request_token.")
    print(f"2. Login URL: {kite.login_url()}")
    print("3. After successful login, you will be redirected to a URL.")
    print("4. Copy the 'request_token' value from that redirect URL.\n")

    # 2. Prompt user for the request_token
    request_token = input("Enter the request_token here: ")

    if not request_token:
        raise ValueError("Request token cannot be empty.")

    try:
        # 3. Generate session and get access_token
        logger.info("Generating session with the provided request_token...")
        user_data = kite.generate_session(request_token, api_secret=api_secret)
        access_token = user_data['access_token']

        # 4. Set the access token for the current session
        kite.set_access_token(access_token)

        # 5. Set header for 2025 compatibility
        kite.req.headers.update({'X-Kite-Version': '3'})

        # 6. Verify connection
        profile = kite.profile()
        logger.info(f"\nConnection successful! Authenticated as user: {profile['user_id']}\n")
        return kite

    except Exception as e:
        logger.error(f"Authentication failed: {e}")
        raise
