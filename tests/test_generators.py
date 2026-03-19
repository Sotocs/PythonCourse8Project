import pytest
from scr import generators


@pytest.fixture
def transactions_fixture():
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2020-01-15T14:30:12.123456",
            "operationAmount": {"amount": "5000.00", "currency": {"name": "EUR", "code": "EUR"}},
            "description": "Покупка в магазине",
            "from": "Счет 12345678901234567890",
            "to": "Счет 09876543210987654321",
        },
        {
            "id": 555123456,
            "state": "PENDING",
            "date": "2021-03-22T10:15:30.987654",
            "operationAmount": {"amount": "1500.50", "currency": {"name": "USD", "code": "USD"}},
            "description": "Онлайн-оплата",
            "from": "Счет 55554444333322221111",
            "to": "Счет 66667777888899990000",
        },
    ]


def test_generator_filter_by_currency(transactions_fixture):
    f = generators.filter_by_currency(transactions_fixture, "USD")
    assert next(f) == {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702",
    }
    assert next(f) == {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188",
    }
    assert next(f) == {
        "id": 555123456,
        "state": "PENDING",
        "date": "2021-03-22T10:15:30.987654",
        "operationAmount": {"amount": "1500.50", "currency": {"name": "USD", "code": "USD"}},
        "description": "Онлайн-оплата",
        "from": "Счет 55554444333322221111",
        "to": "Счет 66667777888899990000",
    }


def test_transaction_descriptions(transactions_fixture):
    f = generators.transaction_descriptions(transactions_fixture)
    assert next(f) == "Перевод организации"
    assert next(f) == "Перевод со счета на счет"
    assert next(f) == "Покупка в магазине"
    assert next(f) == "Онлайн-оплата"


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
