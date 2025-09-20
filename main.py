import logging
import argparse
from utils.connection import establish_interactive_connection
from strategy.strategy import execute_strategy

# Configure logging
def setup_logging():
    """Configures logging to file and console."""
    logging.basicConfig(
        level=logging.DEBUG, # Set the root logger level to DEBUG
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("app.log", mode='w'), # Log to file
            logging.StreamHandler() # Log to console
        ]
    )

logger = logging.getLogger(__name__)

def get_user_inputs():
    """
    Parses command-line arguments for trading inputs.
    Using argparse is a best practice for CLI applications.
    """
    parser = argparse.ArgumentParser(description="Simple Algorithmic Trading Bot")
    parser.add_argument("--strike", type=float, required=True, help="Strike price (e.g., 25000.0)")
    parser.add_argument("--lots", type=int, required=True, help="Number of lots (e.g., 1)")
    parser.add_argument("--sl", type=float, required=True, help="Stop loss in points (e.g., 50.0)")
    parser.add_argument("--target", type=float, required=True, help="Target in points (e.g., 100.0)")
    parser.add_argument("--dry-run", action="store_true", help="Run in simulation mode without placing real orders.")

    args = parser.parse_args()

    # Validation
    if args.lots <= 0:
        raise ValueError("Number of lots must be a positive integer.")
    if args.sl < 0 or args.target < 0:
        raise ValueError("Stop loss and target cannot be negative.")

    return args.strike, args.lots, args.sl, args.target, args.dry_run


def main():
    """
    Main function to run the trading bot.
    """
    setup_logging()
    logger.info("Starting the algorithmic trading system...")

    try:
        # Get user inputs from command line
        strike_price, lots, stop_loss, target, dry_run = get_user_inputs()

        # Establish API connection
        kite = establish_interactive_connection()

        # The lot size fetching is now handled inside the strategy,
        # so we calculate initial quantity here and let the strategy refine it.
        # A placeholder lot size; the strategy will find the real one.
        placeholder_lot_size = 75
        quantity = lots * placeholder_lot_size

        logger.info("\n--- Trade Parameters Confirmed ---")
        logger.info(f"Strike Price: {strike_price}, Lots: {lots}")
        logger.info(f"Stop Loss: {stop_loss}, Target: {target}")
        logger.info(f"Dry Run Mode: {'Enabled' if dry_run else 'Disabled'}")
        logger.info("----------------------------------\n")

        # Execute the trading strategy
        execute_strategy(
            kite=kite,
            strike_price=strike_price,
            quantity=quantity, # This will be recalculated inside the strategy
            stop_loss=stop_loss,
            target=target,
            dry_run=dry_run
        )

    except ValueError as e:
        logger.critical(f"Input or credential error: {e}")
    except Exception as e:
        logger.critical(f"A critical error stopped the system: {e}")


if __name__ == "__main__":
    main()
