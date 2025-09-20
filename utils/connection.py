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
    print("1. Copy the URL below and paste it into your browser.")
    print(f"   Login URL: {kite.login_url()}")
    print("2. Log in to your Zerodha account and grant permissions.")
    print("3. You will be redirected to a new page. The URL of this new page will look something like this:")
    print("   https://your-redirect-url.com/?status=success&request_token=THIS_IS_THE_TOKEN_YOU_NEED")
    print("4. Copy the value of the 'request_token' from that URL.")

    # 2. Prompt user for the request_token
    request_token = input("\nPaste the request_token here and press Enter: ")

    if not request_token or len(request_token) < 10:
        raise ValueError("The provided request_token is empty or too short. Please try again.")

    try:
        # 3. Generate session and get access_token
        logger.info("Generating session with the provided request_token...")
        user_data = kite.generate_session(request_token.strip(), api_secret=api_secret)
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
        logger.error("This could be due to an invalid API Key/Secret in your .env file or an expired/incorrect request_token.")
        raise
