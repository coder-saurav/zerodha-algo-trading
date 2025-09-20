# Python Algorithmic Trading System for Zerodha Kite

This project is a simple, command-line-based algorithmic trading system for executing intraday sell strategies on options/futures using the Zerodha Kite Connect API. It is designed with modularity, security, and the latest 2025 API standards in mind.

The core functionality allows a user to specify a strike price, number of lots, stop loss, and target for an NFO instrument. The system then places a Bracket Order (BO) to automate the trade execution and risk management.

---

## Table of Contents
1.  [Features](#features)
2.  [Project Structure](#project-structure)
3.  [Setup and Installation](#setup-and-installation)
4.  [How to Run](#how-to-run)
5.  [Future Enhancements](#future-enhancements)
6.  [Maintenance Best Practices](#maintenance-best-practices)

---

## Features
- **Secure API Connection**: Connects to the Kite API using credentials stored securely in a `.env` file.
- **Dynamic Instrument Handling**: Automatically constructs trading symbols and fetches the correct lot size at runtime.
- **Bracket Order Execution**: Places sell-side Bracket Orders to ensure a stop loss and target are always attached to the primary order.
- **Command-Line Interface**: Accepts all trading parameters as command-line arguments for easy scripting and automation.
- **Dry Run Mode**: A `--dry-run` flag allows for simulating trade execution without risking real capital.
- **Comprehensive Logging**: Logs all actions, errors, and trade events to both the console and a persistent `app.log` file.
- **Unit Tested**: Core logic is verified with a suite of `pytest` unit tests.

---

## Project Structure
```
.
├── PRD_v1.0.md         # Product Requirements Document
├── README.md           # This file
├── app.log             # Log output file (generated on run)
├── main.py             # Main entry point of the application
├── planning.log        # Initial project goals
├── requirements.txt    # Python dependencies
├── .env                # API credentials (must be created manually)
├── config/             # Configuration files (if any)
│   └── __init__.py
├── strategy/           # Core trading logic
│   ├── __init__.py
│   └── strategy.py
├── tests/              # Unit tests
│   ├── __init__.py
│   ├── test_connection.py
│   └── test_strategy.py
└── utils/              # Utility functions
    ├── __init__.py
    └── connection.py
```

---

## Setup and Installation

### 1. Prerequisites
- Python 3.10+
- A Zerodha Kite Developer account with API access.

### 2. Clone the Repository
```bash
git clone <repository-url>
cd <repository-folder>
```

### 3. Install Dependencies
It is highly recommended to use a Python virtual environment.
```bash
# Create and activate a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install required packages
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a file named `.env` in the root of the project directory and populate it with your Kite API credentials.

```ini
# .env file
KITE_API_KEY="your_api_key"
KITE_API_SECRET="your_api_secret"
KITE_ACCESS_TOKEN="your_access_token"
```
**IMPORTANT**: The `KITE_ACCESS_TOKEN` must be generated daily. Refer to the [Kite Connect documentation](https://kite.trade/docs/connect/v3/user/) for the process of generating an access token.

---

## How to Run
The application is run from the command line, providing all trade parameters as arguments.

### Example Usage
To execute a **dry run** for selling 1 lot of a NIFTY PE option at a strike of 25000 with a 50-point stop loss and 100-point target:
```bash
python main.py --strike 25000 --lots 1 --sl 50 --target 100 --dry-run
```

To execute a **live trade** (remove the `--dry-run` flag):
```bash
python main.py --strike 25000 --lots 1 --sl 50 --target 100
```
**Disclaimer**: Live trading involves significant financial risk. Always test thoroughly in dry-run mode before deploying with real capital.

---

## Future Enhancements
This system is designed as a foundation. Here are some potential ways to extend its functionality:
- **WebSocket Integration**: Upgrade the polling-based position monitor to use the KiteTicker WebSocket for real-time, low-latency updates on ticks and order status.
- **AI/ML Signal Integration**: Incorporate a machine learning model (e.g., using scikit-learn or TensorFlow) to generate trading signals instead of relying on manual inputs.
- **Cloud Deployment**: Dockerize the application and deploy it to a cloud service (AWS, GCP, Azure) for continuous, reliable operation.
- **Advanced Indicators**: Add logic to calculate and trade based on technical indicators like RSI, MACD, or Bollinger Bands.
- **Backtesting Engine**: Build a proper backtesting module to test strategies against historical data, providing insights into their potential performance.

---

## Maintenance Best Practices
- **Monitor API Changes**: Regularly check the [Zerodha Developer Changelog](https://kite.trade/docs/connect/v3/changelog/) for any updates or deprecations that might affect the system.
- **Rotate Credentials**: For enhanced security, periodically regenerate your `KITE_API_SECRET` and update it in your environment.
- **Code Optimization**: As the strategy becomes more complex, profile the code to identify and eliminate performance bottlenecks.
- **Version Control**: Keep the codebase under Git version control and maintain a backup of your repository.
- **Periodic Testing**: Re-run the test suite periodically, especially after making changes or updating dependencies, to ensure everything remains functional.
