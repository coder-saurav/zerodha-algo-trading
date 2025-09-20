# Product Requirements Document (PRD): Algorithmic Trading System
**Version: 1.0**

## 1. Introduction
This document specifies the requirements for a Python-based algorithmic trading system designed for intraday trading on the Zerodha platform. The system is engineered for simplicity and modularity, leveraging the Zerodha Kite Connect API (v4). All specifications are aligned with market and API conditions as of September 2025, including Zerodha's free personal trading API, updated NSE lot sizes, and enhanced GTT/WebSocket features.

## 2. Objectives
- **Secure Connection:** Establish a secure, reliable, and version-aware connection to the Kite API.
- **Dynamic Inputs:** Accept and validate user-defined trading parameters at runtime.
- **Automated Execution:** Automate the placement of sell-side bracket orders (or GTT as a fallback) for intraday trading.
- **Real-time Monitoring:** Provide a mechanism for monitoring open positions and profit/loss.
- **Extensible Architecture:** Build a modular codebase that facilitates future enhancements.
- **Regulatory Compliance:** Adhere to 2025 market regulations by dynamically fetching instrument data like lot sizes and quantity freeze limits.

## 3. Scope
**In Scope:**
- A single-instrument, sell-side strategy for NFO-traded options/futures.
- Use of Bracket Orders (BO) for automated Stop Loss (SL) and Target (TP).
- A command-line interface (CLI) for user interaction.
- Position monitoring via API polling, with a defined upgrade path to WebSockets.
- Secure credential management via `.env` files.
- Comprehensive event and error logging.

**Out of Scope:**
- A historical backtesting engine.
- Complex technical indicators or predictive AI models.
- Multi-asset, multi-strategy, or multi-exchange trading.
- A graphical user interface (GUI).
- Fully automated cloud deployment pipelines.

## 4. Functional Requirements
- **API Connection:** The system must connect to Kite API using a pre-generated `access_token` and the `X-Kite-Version: 3` header for 2025 backend compatibility.
- **User Inputs:** The system will prompt for:
    - `strike_price` (float): The strike price of the instrument.
    - `lots` (int): The number of lots to trade.
    - `stop_loss` (float): The absolute stop loss value.
    - `target` (float): The absolute target value.
- **Input Validation:** All inputs must be validated to be positive numerical values. The final quantity will be checked against quantity freeze limits.
- **Trading Logic:**
    1. Dynamically fetch the `tradingsymbol` and `lot_size` from `kite.instruments('NFO')`.
    2. Calculate `quantity = lots * lot_size`.
    3. Place a `SELL` bracket order with `product='MIS'` and `order_type='MARKET'`.
    4. **2025 Enhancement:** If BO is not supported for an instrument, log a warning and attempt to place a GTT order as a fallback.
- **Position Monitoring:** Poll `kite.positions()` every 60 seconds to display the current PNL.

## 5. Non-Functional Requirements
- **Performance:** API call latency should be minimized, ideally under 1 second.
- **Security:** API credentials must be loaded from an external `.env` file and never be committed to version control.
- **Reliability:** Implement retry logic with exponential backoff for critical API calls to handle transient failures.
- **Maintainability:** Code must be organized into a clean, modular structure (e.g., `utils/`, `strategy/`) with clear separation of concerns.

## 6. Tech Stack
- **Language:** Python 3.10+
- **Libraries:**
    - `kiteconnect==4.2.0`
    - `python-dotenv==1.0.1`
    - `pandas==2.1.0`
    - `websockets==12.0` (for real-time streaming)
- **Environment:** A dedicated virtual environment (`venv`) is required.

## 7. Assumptions and Risks
- **Assumptions:**
    - User possesses an active Zerodha account with Kite API access enabled.
    - A valid, daily-generated `access_token` is available in the `.env` file.
    - Trading operations are conducted within NSE market hours.
- **Risks:**
    - **Market Risk:** High volatility may cause slippage or unexpected losses. Mitigation: Enforced SL/TP via bracket orders and extensive paper trading before live deployment.
    - **API Risk:** Future breaking changes in the Kite API. Mitigation: Adherence to API versioning and active monitoring of Zerodha's developer changelog.
    - **Technical Risk:** Internet connectivity failure. Mitigation: Robust connection retry mechanisms.

## 8. High-Level Architecture
The system employs a linear execution flow:
`Initialize & Connect -> Get User Inputs -> Validate Inputs -> Fetch Instrument Data -> Place Order (BO/GTT) -> Monitor Position`

---
## Appendix A: Glossary
- **API:** Application Programming Interface
- **BO:** Bracket Order
- **GTT:** Good Till Triggered
- **MIS:** Margin Intraday Square off
- **NFO:** NSE Futures & Options
- **SL:** Stop Loss
- **TP:** Target Profit

## Appendix B: References
- **Kite Connect API Docs (v3):** https://kite.trade/docs/connect/v3/
- **Zerodha Developer Portal:** https://developers.kite.trade/
- **NSE India Website:** https://www.nseindia.com/
