import pytest
from scr import generators


@pytest.fixture
def transactions_fixture():
    return [
        {
            "id": 939719570,
            "operationAmount": {"currency": {"code": "USD"}},
            "description": "Перевод организации",
        },
        {
            "id": 142264268,
            "operationAmount": {"currency": {"code": "USD"}},
            "description": "Перевод со счета на счет",
        },
        {
            "id": 873106923,
            "operationAmount": {"currency": {"code": "RUB"}},
            "description": "Покупка",
        },
    ]


# --- filter_by_currency ---

def test_filter_by_currency_empty_list():
    result = list(generators.filter_by_currency([], "USD"))
    assert result == []


def test_filter_by_currency_no_matches(transactions_fixture):
    result = list(generators.filter_by_currency(transactions_fixture, "EUR"))
    assert result == []


def test_filter_by_currency_stop_iteration(transactions_fixture):
    gen = generators.filter_by_currency(transactions_fixture, "USD")

    next(gen)
    next(gen)

    with pytest.raises(StopIteration):
        next(gen)


# --- transaction_descriptions ---

def test_transaction_descriptions_full_list(transactions_fixture):
    result = list(generators.transaction_descriptions(transactions_fixture))
    assert result == [
        "Перевод организации",
        "Перевод со счета на счет",
        "Покупка",
    ]


def test_transaction_descriptions_empty():
    result = list(generators.transaction_descriptions([]))
    assert result == []


def test_transaction_descriptions_stop_iteration(transactions_fixture):
    gen = generators.transaction_descriptions(transactions_fixture)

    next(gen)
    next(gen)
    next(gen)

    with pytest.raises(StopIteration):
        next(gen)

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
