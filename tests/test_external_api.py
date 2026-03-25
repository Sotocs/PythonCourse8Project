import pytest
from unittest.mock import Mock, patch
from scr.external_api import convertation

# --- Тест для RUB ---
def test_rub_returns_same():
    transaction = {
        "operationAmount": {"amount": "1000", "currency": {"code": "RUB"}}
    }
    assert convertation(transaction) == 1000.0


# --- Тест для USD с mock ---
@patch("scr.external_api.requests.get")
def test_usd_conversion(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {"result": 9200.0}
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    transaction = {
        "operationAmount": {"amount": "100", "currency": {"code": "USD"}}
    }
    result = convertation(transaction)
    assert result == 9200.0
    mock_get.assert_called_once()


# --- Тест для EUR с mock ---
@patch("scr.external_api.requests.get")
def test_eur_conversion(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {"result": 11000.0}
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    transaction = {
        "operationAmount": {"amount": "100", "currency": {"code": "EUR"}}
    }
    result = convertation(transaction)
    assert result == 11000.0


# --- Тест неизвестной валюты ---
def test_unknown_currency_raises():
    transaction = {
        "operationAmount": {"amount": "100", "currency": {"code": "GBP"}}
    }
    with pytest.raises(ValueError):
        convertation(transaction)