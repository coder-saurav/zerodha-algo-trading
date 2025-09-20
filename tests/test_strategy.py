import pytest
from unittest.mock import Mock, patch
from strategy.strategy import get_trading_symbol, place_sell_order

# --- Mock Data ---
MOCK_INSTRUMENTS = [
    {
        'instrument_token': 12345,
        'tradingsymbol': 'NIFTY25SEP25000PE',
        'name': 'NIFTY',
        'strike': 25000.0,
        'lot_size': 75,
        'instrument_type': 'PE',
        'expiry': '2025-09-25'
    },
    {
        'instrument_token': 67890,
        'tradingsymbol': 'BANKNIFTY25SEP50000CE',
        'name': 'BANKNIFTY',
        'strike': 50000.0,
        'lot_size': 35,
        'instrument_type': 'CE',
        'expiry': '2025-09-25'
    }
]

@pytest.fixture
def mock_kite():
    """Pytest fixture to create a mock KiteConnect object."""
    kite = Mock()
    kite.instruments.return_value = MOCK_INSTRUMENTS
    kite.place_order.return_value = 123456789 # Mock order ID
    return kite

# Set a fixed date for consistent testing of expiry string generation
@patch('strategy.strategy.datetime')
def test_get_trading_symbol_success(mock_datetime, mock_kite):
    """
    Tests that get_trading_symbol correctly finds a valid instrument.
    """
    # Arrange
    mock_datetime.now.return_value = Mock(strftime=Mock(return_value='25SEP'))

    # Act
    symbol, token, lot_size = get_trading_symbol(mock_kite, "NIFTY", 25000.0, "PE")

    # Assert
    assert symbol == 'NIFTY25SEP25000PE'
    assert token == 12345
    assert lot_size == 75
    mock_kite.instruments.assert_called_with('NFO')

@patch('strategy.strategy.datetime')
def test_get_trading_symbol_not_found(mock_datetime, mock_kite):
    """
    Tests that get_trading_symbol returns None when no instrument is found.
    """
    # Arrange
    mock_datetime.now.return_value = Mock(strftime=Mock(return_value='25SEP'))

    # Act
    symbol, token, lot_size = get_trading_symbol(mock_kite, "NIFTY", 99999.0, "PE") # Non-existent strike

    # Assert
    assert symbol is None
    assert token is None
    assert lot_size is None

def test_place_sell_order_dry_run(mock_kite, caplog):
    """
    Tests that place_sell_order in dry_run mode logs correctly and does not place an order.
    """
    # Arrange (caplog is a pytest fixture to capture log output)
    caplog.set_level("INFO")

    # Act
    order_id = place_sell_order(mock_kite, "TESTSYMBOL", 100, 50, 100, dry_run=True)

    # Assert
    assert order_id == 0
    assert "DRY RUN" in caplog.text
    assert "Simulating SELL Bracket Order for TESTSYMBOL" in caplog.text
    mock_kite.place_order.assert_not_called()

def test_place_sell_order_live(mock_kite):
    """
    Tests that place_sell_order calls the Kite API with the correct parameters in live mode.
    """
    # Act
    order_id = place_sell_order(mock_kite, "TESTSYMBOL", 100, 50, 100, dry_run=False)

    # Assert
    assert order_id == 123456789
    mock_kite.place_order.assert_called_once_with(
        variety=mock_kite.VARIETY_BO,
        exchange=mock_kite.EXCHANGE_NFO,
        tradingsymbol="TESTSYMBOL",
        transaction_type=mock_kite.TRANSACTION_TYPE_SELL,
        quantity=100,
        product=mock_kite.PRODUCT_MIS,
        order_type=mock_kite.ORDER_TYPE_MARKET,
        stoploss=50,
        squareoff=100
    )
