# Simple Algo Trading Bot for Zerodha Kite

This project is a simple algorithmic trading bot that uses the Zerodha Kite Connect API to place trades. It is designed to demonstrate how to programmatically place complex orders, specifically Bracket Orders with a trailing stop-loss.

**Disclaimer:** This is a proof-of-concept and for educational purposes only. Trading in financial markets involves significant risk. You are solely responsible for any trades placed by this bot. Use it at your own risk. It is highly recommended to test this bot extensively in a simulated environment or with very small amounts before using it for any real trading.

## Features

-   Connects to the Zerodha Kite API.
-   Handles the API authentication flow.
-   Places Bracket Orders, which include:
    -   An initial entry order (LIMIT order).
    -   A target (take-profit) order.
    -   A stop-loss order.
-   Supports **trailing stop-loss** on the placed orders.

## Getting Started

### Prerequisites

-   Python 3.7+
-   A Zerodha account with API access enabled. You will need an `API_KEY` and `API_SECRET` from the [Kite Developer Console](https://developers.kite.trade/).

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Install the required Python packages:**
    ```bash
    pip install -r requirements.txt
    ```

### Configuration

1.  **Create a `.env` file** for your credentials. You can do this by copying the example file:
    ```bash
    cp .env.example .env
    ```

2.  **Edit the `.env` file** with your favorite text editor and add your Zerodha `API_KEY` and `API_SECRET`.
    ```
    API_KEY="YOUR_API_KEY"
    API_SECRET="YOUR_API_SECRET"
    ACCESS_TOKEN=""
    ```
    (Leave `ACCESS_TOKEN` blank, the application will handle it).

## Usage

1.  **Run the main application:**
    ```bash
    python main.py
    ```

2.  **Follow the on-screen instructions for authentication:**
    -   The script will print a login URL. Copy and paste this URL into your web browser.
    -   Log in with your Zerodha credentials.
    -   After logging in, you will be redirected to a new URL. This URL will contain a `request_token`.
    -   Copy the `request_token` from the URL and paste it back into the terminal when prompted.

3.  **Placing an Order:**
    -   By default, the order placement logic in `main.py` is **commented out** to prevent accidental live trades.
    -   To place a real trade, you must edit the `main.py` file:
        -   Change the `trading_symbol`, `limit_price`, `quantity`, and other parameters to your desired values.
        -   Uncomment the lines that call the `trader.place_bracket_order` method.
    -   Run the script again (`python main.py`).

**Important:** Always double-check the parameters in `main.py` before uncommenting the order placement code.
