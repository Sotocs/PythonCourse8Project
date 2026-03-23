import pytest
from scr import generators



@pytest.fixture
def transactions_fixture():
    return (
    [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188"
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160"
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {
                "amount": "56883.54",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229"
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {
                "amount": "67314.70",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657"
        }
    ]
)


# Тесты для filter_by_currency
def test_filter_by_currency_usd(transactions_fixture):
    """Проверяет фильтрацию по USD — должно быть 3 транзакции."""
    result = list(generators.filter_by_currency(transactions_fixture, "USD"))
    assert len(result) == 3
    assert all(tx["operationAmount"]["currency"]["code"] == "USD" for tx in result)

def test_filter_by_currency_rub(transactions_fixture):
    """Проверяет фильтрацию по RUB — должно быть 2 транзакции."""
    result = list(generators.filter_by_currency(transactions_fixture, "RUB"))
    assert len(result) == 2
    assert all(tx["operationAmount"]["currency"]["code"] == "RUB" for tx in result)

def test_filter_by_currency_no_matches(transactions_fixture):
    """Проверяет отсутствие совпадений (например, для 'EUR')."""
    result = list(generators.filter_by_currency(transactions_fixture, "EUR"))
    assert result == []

def test_filter_by_currency_empty_list():
    """Проверяет обработку пустого списка."""
    result = list(generators.filter_by_currency([], "USD"))
    assert result == []

def test_filter_by_currency_stop_iteration(transactions_fixture):
    """Проверяет корректное завершение итератора (StopIteration)."""
    gen = generators.filter_by_currency(transactions_fixture, "USD")
    for _ in range(3):  # 3 транзакции с USD
        next(gen)
    with pytest.raises(StopIteration):
        next(gen)

# Тесты для transaction_descriptions
def test_transaction_descriptions_full_list(transactions_fixture):
    """Проверяет генерацию всех описаний транзакций."""
    expected = [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
        "Перевод организации"
    ]
    result = list(generators.transaction_descriptions(transactions_fixture))
    assert result == expected

def test_transaction_descriptions_empty():
    """Проверяет обработку пустого списка."""
    result = list(generators.transaction_descriptions([]))
    assert result == []

def test_transaction_descriptions_stop_iteration(transactions_fixture):
    """Проверяет корректное завершение итератора (StopIteration)."""
    gen = generators.transaction_descriptions(transactions_fixture)
    for _ in range(5):  # 5 транзакций в фикстуре
        next(gen)
    with pytest.raises(StopIteration):
        next(gen)

def test_transaction_descriptions_missing_description():
    """Проверяет обработку транзакции без поля 'description'."""
    broken_tx = [
        {
            "id": 123,
            "state": "EXECUTED",
            "operationAmount": {"currency": {"code": "USD"}},
            # 'description' отсутствует!
            "from": "Счет 1234567890",
            "to": "Счет 0987654321"
        },
        {}
    ]
    with pytest.raises(KeyError):
        next(generators.transaction_descriptions(broken_tx))

def test_default_range_first_numbers():
    # Проверяет генерацию первых нескольких номеров карт
    generator = generators.card_number_generator(1, 3)
    result = list(generator)

    expected = ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]
    assert result == expected

    # Проверяет генерацию одного номера карты
    generator = generators.card_number_generator(9876543210987654, 9876543210987654)
    result = list(generator)
    expected = ["9876 5432 1098 7654"]
    assert result == expected
