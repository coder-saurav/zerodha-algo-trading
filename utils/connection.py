import logging
import os
import time
from kiteconnect import KiteConnect
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def establish_connection():
    """
    Establishes a connection to the Kite API using credentials from the .env file.

    Returns:
        KiteConnect object if successful.

    Raises:
        ValueError: If API credentials are not found in the environment.
        Exception: For other Kite Connect API exceptions.
    """
    api_key = os.getenv('KITE_API_KEY')
    api_secret = os.getenv('KITE_API_SECRET')
    access_token = os.getenv('KITE_ACCESS_TOKEN')

    if not all([api_key, api_secret, access_token]) or "your_" in api_key:
        logger.error("API credentials not found or are placeholders in .env file.")
        raise ValueError("Missing or placeholder API credentials. Please update your .env file.")

    try:
        kite = KiteConnect(api_key=api_key)
        kite.set_access_token(access_token)

        # 2025 update: Set header for v3 backend compatibility as per documentation
        kite.req.headers.update({'X-Kite-Version': '3'})

        # Test connection by fetching profile
        profile = kite.profile()
        logger.info(f"Connected successfully to Kite API. User: {profile['user_id']}")
        return kite
    except Exception as e:
        logger.error(f"Connection to Kite API failed: {e}")
        raise

def retry_connection(max_retries=3, delay=5):
    """
    Attempts to establish a connection with retries on failure.

    Args:
        max_retries (int): The maximum number of retry attempts.
        delay (int): The delay in seconds between retries (exponential backoff).

    Returns:
        KiteConnect object if successful, otherwise None.
    """
    for attempt in range(max_retries):
        try:
            return establish_connection()
        except Exception as e:
            logger.warning(f"Connection attempt {attempt + 1} of {max_retries} failed. Retrying in {delay} seconds...")
            time.sleep(delay * (2 ** attempt)) # Exponential backoff

    logger.error("Max retries exceeded. Could not connect to Kite API.")
    raise Exception("Failed to connect to Kite API after multiple retries.")
