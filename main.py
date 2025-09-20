import logging
from trader import KiteTrader

def main():
    """
    Main function to run the trading bot.
    This function orchestrates the entire process:
    1. Initializes the trader.
    2. Handles user authentication.
    3. Places a pre-defined bracket order (commented out by default for safety).
    """
    logging.basicConfig(level=logging.INFO)
    logging.info("--- Starting Algo Trading Bot ---")

    try:
        # Step 1: Initialize the KiteTrader
        # This will load API credentials from your .env file.
        trader = KiteTrader()

        # Step 2: Authenticate the user
        # This will trigger the manual login flow to get a valid session.
        trader.authenticate()
        logging.info("Authentication successful. Ready to trade.")

        # Step 3: Define Trading Parameters
        # =================================================================
        # IMPORTANT: These are placeholder values for demonstration.
        # You MUST change these to a valid trading symbol and your desired prices/quantities.
        # Using an invalid or expired symbol will result in an error from the API.
        # =================================================================
        trading_symbol = "BANKNIFTY24OCT50000CE"  # <--- CHANGE THIS to a valid symbol
        limit_price = 10.0                        # <--- CHANGE THIS to your desired entry price
        quantity = 15                             # <--- CHANGE THIS to the correct lot size
        target_points = 40.0                      # <--- CHANGE THIS to your target in points
        stoploss_points = 20.0                    # <--- CHANGE THIS to your stop-loss in points
        trailing_stoploss_points = 5.0            # <--- CHANGE THIS to your trailing stop-loss in points

        # Step 4: Place the Bracket Order
        # =================================================================
        # WARNING: LIVE TRADING AHEAD
        # Uncommenting the following lines will attempt to place a REAL order
        # in your Zerodha account. Use with extreme caution.
        # =================================================================
        logging.info("--- Preparing to place order ---")
        logging.warning("Order placement is commented out by default in main.py to prevent accidental trades.")

        # --- UNCOMMENT BELOW TO PLACE A LIVE ORDER ---
        # order_id = trader.place_bracket_order(
        #     tradingsymbol=trading_symbol,
        #     transaction_type=trader.kite.TRANSACTION_TYPE_BUY,
        #     quantity=quantity,
        #     price=limit_price,
        #     target=target_points,
        #     stoploss=stoploss_points,
        #     trailing_stoploss=trailing_stoploss_points
        # )
        #
        # if order_id:
        #     logging.info(f"Successfully placed order with ID: {order_id}. Check your Kite account.")
        # else:
        #     logging.error("Order placement failed. Check the logs for more details.")

        logging.info("--- Main execution finished. Bot is shutting down. ---")

    except Exception as e:
        logging.error(f"An error occurred during the bot's execution: {e}", exc_info=True)


if __name__ == "__main__":
    main()
