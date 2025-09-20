import logging
from kiteconnect import KiteConnect
import config

class KiteTrader:
    def __init__(self):
        """Initializes the KiteTrader class."""
        # Initialize logging
        logging.basicConfig(level=logging.INFO)

        # Load credentials from config
        self.api_key = config.API_KEY
        self.api_secret = config.API_SECRET

        # We will fetch the access token during authentication
        self.access_token = None

        if not self.api_key or not self.api_secret:
            logging.error("API_KEY and API_SECRET must be set in the .env file.")
            raise ValueError("API_KEY and API_SECRET are not configured.")

        # Initialize KiteConnect client
        self.kite = KiteConnect(api_key=self.api_key)
        logging.info("KiteTrader initialized.")

    def authenticate(self):
        """
        Handles the authentication flow for the Kite Connect API.
        It prompts the user to log in via a URL and provide the request_token.
        """
        logging.info("Starting authentication process...")

        # Generate the login URL
        login_url = self.kite.login_url()

        # Print instructions for the user
        print("\n" + "="*80)
        print("MANUAL AUTHENTICATION REQUIRED")
        print("1. Go to the following URL in your browser:")
        print(f"   {login_url}")
        print("2. Log in with your Zerodha credentials.")
        print("3. After successful login, you will be redirected to your redirect_url.")
        print("4. The URL in your browser will look like: https://your-redirect-url.com/?request_token=YOUR_TOKEN&action=login&status=success")
        print("5. Copy the `request_token` value (the part that says 'YOUR_TOKEN').")
        print("="*80 + "\n")

        # Prompt user for the request_token
        request_token = input("Please paste the request_token here: ")

        if not request_token:
            logging.error("Request token cannot be empty.")
            raise ValueError("Invalid request_token provided.")

        try:
            # Generate session and get the access token
            logging.info("Generating session with the provided request_token...")
            data = self.kite.generate_session(request_token.strip(), api_secret=self.api_secret)

            # Set the access token on the KiteConnect instance
            self.access_token = data["access_token"]
            self.kite.set_access_token(self.access_token)

            profile = self.kite.profile()
            logging.info(f"Authentication successful! Welcome, {profile.get('user_name')}.")

        except Exception as e:
            logging.error(f"Authentication failed: {e}")
            # Re-raise the exception to halt execution if authentication fails
            raise

    def place_bracket_order(self, tradingsymbol, transaction_type, quantity, price, target, stoploss, trailing_stoploss):
        """
        Places a Bracket Order (BO).
        A Bracket Order is a three-legged order that includes an entry, a target, and a stop-loss.

        :param tradingsymbol: e.g., "NIFTYBANK24SEPFUT"
        :param transaction_type: "BUY" or "SELL"
        :param quantity: The quantity to trade.
        :param price: The limit price for the entry order.
        :param target: The absolute target points (e.g., 20.0).
        :param stoploss: The absolute stop-loss points (e.g., 10.0).
        :param trailing_stoploss: The absolute trailing stop-loss points (e.g., 2.0).
        """
        try:
            logging.info(f"Placing Bracket Order for {tradingsymbol} | Qty: {quantity} | Price: {price}")
            order_id = self.kite.place_order(
                variety=self.kite.VARIETY_BO,
                exchange=self.kite.EXCHANGE_NFO,  # Assuming Options/Futures trading
                tradingsymbol=tradingsymbol,
                transaction_type=transaction_type,
                quantity=quantity,
                product=self.kite.PRODUCT_MIS,  # Bracket Orders are Intraday only
                order_type=self.kite.ORDER_TYPE_LIMIT,
                price=round(price, 2),  # Ensure price is rounded to 2 decimal places
                squareoff=round(target, 2),
                stoploss=round(stoploss, 2),
                trailing_stoploss=round(trailing_stoploss, 2)
            )
            logging.info(f"Bracket Order placed successfully. Order ID: {order_id}")
            return order_id
        except Exception as e:
            logging.error(f"Failed to place Bracket Order for {tradingsymbol}: {e}")
            raise


# This block is for testing the functionality directly from this file.
# The final application logic will be in main.py
if __name__ == '__main__':
    try:
        logging.info("--- Starting Trader Test ---")
        trader = KiteTrader()
        trader.authenticate()

        # --- Example: Placing a Bracket Order ---
        # NOTE: This is a test order. Please use a valid, liquid tradingsymbol and adjust parameters.
        # This will place a REAL order if your credentials are correct.
        # Use with extreme caution. For testing, you might want to use a very low-priced stock
        # or a far-out-of-the-money option to avoid accidental execution.

        # Let's define some placeholder parameters for a hypothetical Nifty Bank option
        # IMPORTANT: These values are for demonstration only.
        trading_symbol = "BANKNIFTY24OCT50000CE" # Example, likely invalid. Use a real one.
        buy_price = 100.0  # The price at which you want to buy

        # Place a test order
        logging.info("--- Testing Order Placement ---")
        # To prevent accidental real orders, this part is commented out by default.
        # Uncomment the following lines ONLY if you want to test live order placement.
        # order_id = trader.place_bracket_order(
        #     tradingsymbol=trading_symbol,
        #     transaction_type=trader.kite.TRANSACTION_TYPE_BUY,
        #     quantity=15,  # Lot size for BANKNIFTY is 15
        #     price=buy_price,
        #     target=40.0,  # Target of 40 points (exit at 140.0)
        #     stoploss=20.0,  # Stop-loss of 20 points (exit at 80.0)
        #     trailing_stoploss=5.0  # Trail stop-loss by 5 points
        # )
        # if order_id:
        #     logging.info(f"Test order placed with ID: {order_id}")

        logging.info("--- Test complete. If you uncommented the order placement, check your Kite account. ---")

    except Exception as e:
        logging.error(f"An error occurred in the main execution block: {e}")
