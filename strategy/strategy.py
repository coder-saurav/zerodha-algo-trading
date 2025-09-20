import logging
import time
from datetime import datetime
from kiteconnect import KiteConnect, KiteTicker

# Configure logging
logger = logging.getLogger(__name__)

def get_trading_symbol(kite, underlying, strike_price, instrument_type="PE"):
    """
    Constructs the trading symbol and finds its instrument token and lot size.
    This version dynamically determines the expiry for the current month.

    Args:
        kite (KiteConnect): Authenticated Kite client.
        underlying (str): The underlying index/stock (e.g., 'NIFTY').
        strike_price (float): The strike price.
        instrument_type (str): 'PE' for Put Option, 'CE' for Call Option.

    Returns:
        tuple: (tradingsymbol, instrument_token, lot_size) or (None, None, None)
    """
    # This is a simplified logic for expiry. A robust system would handle monthly/weekly expiries precisely.
    # For this example, we assume monthly expiry, formatted as YYMON.
    # E.g., September 2025 -> 25SEP
    now = datetime.now()
    # This format is a simplification. Zerodha uses specific dates for expiry.
    # A production system should fetch the exact expiry dates from the instruments list.
    expiry_str = now.strftime("%y%b").upper() # e.g., '25SEP'

    # Construct a potential symbol prefix to search for
    symbol_prefix = f"{underlying}{expiry_str}{int(strike_price)}{instrument_type}"
    logger.info(f"Searching for instrument like: {symbol_prefix}")

    try:
        instruments = kite.instruments('NFO')
        target_instrument = next(
            (i for i in instruments if i['tradingsymbol'].startswith(symbol_prefix)), None
        )

        if target_instrument:
            symbol = target_instrument['tradingsymbol']
            token = target_instrument['instrument_token']
            lot_size = target_instrument['lot_size']
            logger.info(f"Found symbol: {symbol} (Token: {token}, Lot Size: {lot_size})")
            return symbol, token, lot_size
        else:
            logger.error(f"Could not find any instrument for prefix '{symbol_prefix}'")
            return None, None, None

    except Exception as e:
        logger.error(f"Failed to fetch or find instrument: {e}")
        raise

def place_sell_order(kite, symbol, quantity, sl, target, dry_run=False):
    """
    Places a sell-side bracket order.

    Args:
        kite (KiteConnect): Authenticated Kite client.
        symbol (str): The trading symbol.
        quantity (int): The order quantity.
        sl (float): The stoploss points.
        target (float): The target points.
        dry_run (bool): If True, simulate order placement.

    Returns:
        int: The order ID if placed successfully, or 0 for a dry run.
    """
    if dry_run:
        logger.info("--- DRY RUN ---")
        logger.info(f"Simulating SELL Bracket Order for {symbol}")
        logger.info(f"Quantity: {quantity}, SL: {sl} pts, Target: {target} pts")
        logger.info("--- END DRY RUN ---")
        return 0

    try:
        order_id = kite.place_order(
            variety=kite.VARIETY_BO,  # Bracket Order
            exchange=kite.EXCHANGE_NFO,
            tradingsymbol=symbol,
            transaction_type=kite.TRANSACTION_TYPE_SELL,
            quantity=quantity,
            product=kite.PRODUCT_MIS,  # Intraday
            order_type=kite.ORDER_TYPE_MARKET,
            stoploss=sl,  # Absolute stoploss points
            squareoff=target  # Absolute target points
        )
        logger.info(f"Bracket order placed successfully for {symbol}. Order ID: {order_id}")
        return order_id
    except Exception as e:
        logger.error(f"Failed to place bracket order for {symbol}: {e}")
        # Note: Task 5.2 suggests using GTT as a fallback if BO fails.
        # This logic can be added here.
        raise

def monitor_positions_polling(kite, order_id):
    """
    Monitors open positions using basic polling.
    NOTE: This is inefficient. WebSocket is the recommended approach.
    """
    logger.info("Starting position monitoring via polling (60s interval)...")
    try:
        while True:
            positions = kite.positions().get('net', [])
            if not any(p['quantity'] != 0 for p in positions):
                logger.info("All positions have been closed. Stopping monitor.")
                break

            for pos in positions:
                if pos['quantity'] != 0:
                    logger.info(f"Open Position: {pos['tradingsymbol']}, Qty: {pos['quantity']}, PNL: {pos['pnl']:.2f}")

            time.sleep(60)
    except KeyboardInterrupt:
        logger.info("Position monitoring stopped by user.")
    except Exception as e:
        logger.error(f"An error occurred during position monitoring: {e}")

# --- 2025 Enhancement: WebSocket Monitoring (as per task5.3) ---
def start_websocket_monitoring(kite, instrument_token, sl_price, target_price):
    """
    Monitors ticks in real-time using KiteTicker WebSocket.
    This is the preferred method for 2025.
    """
    api_key = kite.api_key
    access_token = kite.access_token
    kws = KiteTicker(api_key, access_token)

    def on_ticks(ws, ticks):
        for tick in ticks:
            if tick['instrument_token'] == instrument_token:
                ltp = tick['last_price']
                logger.info(f"Tick for {instrument_token}: LTP = {ltp}")
                if ltp <= sl_price or ltp >= target_price:
                    logger.info(f"SL or Target hit at {ltp}. Closing position...")
                    # Add logic here to exit the position
                    ws.close()

    def on_connect(ws, response):
        logger.info("WebSocket connected. Subscribing to ticks.")
        ws.subscribe([instrument_token])
        ws.set_mode(ws.MODE_LTP, [instrument_token])

    def on_close(ws, code, reason):
        logger.info(f"WebSocket connection closed: {reason} (Code: {code})")

    kws.on_ticks = on_ticks
    kws.on_connect = on_connect
    kws.on_close = on_close

    logger.info("Connecting to WebSocket...")
    kws.connect(threaded=True)
    # Keep the main thread alive while the WebSocket runs in the background
    # In a real app, you might manage this with a more robust loop.
    while kws.is_connected():
        time.sleep(1)


def execute_strategy(kite, strike_price, quantity, stop_loss, target, dry_run=True):
    """
    Executes the full trading strategy for a given instrument.
    """
    logger.info(f"\nExecuting strategy for strike {strike_price}...")
    try:
        # Step 1: Get trading symbol and details
        symbol, token, lot_size = get_trading_symbol(kite, "NIFTY", strike_price, "PE")
        if not symbol:
            raise ValueError("Could not determine trading symbol. Exiting strategy.")

        # Recalculate quantity based on fetched lot_size to be certain
        # This part assumes 'quantity' was just a placeholder if lots were known
        # Or, we can assume the quantity passed in is already correct.
        # For simplicity, we trust the quantity from main.py

        # Step 2: Place the bracket order
        order_id = place_sell_order(kite, symbol, quantity, stop_loss, target, dry_run)

        if not dry_run and order_id:
            # Step 3: Monitor the position
            # We'll use the polling method for now as per the baseline requirement.
            # The WebSocket method is provided for the 2025 enhancement path.
            monitor_positions_polling(kite, order_id)

        logger.info("Strategy execution complete.")

    except Exception as e:
        logger.error(f"Strategy execution failed: {e}")
