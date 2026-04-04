import pytest

from scr import processing


@pytest.mark.parametrize(
    "list_of_dicts, argument, expected",
    [
        # Тест 1: фильтрация по умолчанию (EXECUTED)
        (
            [{"id": 1, "state": "EXECUTED"}, {"id": 2, "state": "PENDING"}, {"id": 3, "state": "EXECUTED"}],
            "EXECUTED",
            [{"id": 1, "state": "EXECUTED"}, {"id": 3, "state": "EXECUTED"}],
        ),
        # Тест 2: фильтрация по PENDING
        (
            [{"id": 1, "state": "EXECUTED"}, {"id": 2, "state": "PENDING"}, {"id": 3, "state": "PENDING"}],
            "PENDING",
            [{"id": 2, "state": "PENDING"}, {"id": 3, "state": "PENDING"}],
        ),
        # Тест 3: пустой список
        ([], "EXECUTED", []),
        # Тест 4: нет подходящих элементов
        ([{"id": 1, "state": "EXECUTED"}, {"id": 2, "state": "CANCELED"}], "PENDING", []),
        # Тест 5: все элементы подходят
        (
            [{"id": 1, "state": "EXECUTED"}, {"id": 2, "state": "EXECUTED"}],
            "EXECUTED",
            [{"id": 1, "state": "EXECUTED"}, {"id": 2, "state": "EXECUTED"}],
        ),
        # Тест 6: один элемент, подходящий под фильтр
        ([{"id": 1, "state": "PENDING"}], "PENDING", [{"id": 1, "state": "PENDING"}]),
        # Тест 7: словари с разными ключами
        (
            [
                {"id": 1, "state": "EXECUTED", "amount": 100},
                {"id": 2, "state": "PENDING", "amount": 200},
                {"id": 3, "state": "EXECUTED", "description": "payment"},
            ],
            "EXECUTED",
            [{"id": 1, "state": "EXECUTED", "amount": 100}, {"id": 3, "state": "EXECUTED", "description": "payment"}],
        ),
    ],
)
def test_filter_by_state_2(list_of_dicts: list[dict], argument: str, expected: list[dict]) -> None:
    assert processing.filter_by_state(list_of_dicts, argument) == expected


@pytest.mark.parametrize(
    "list_of_dicts, sort_type_forward, expected",
    [
        # Тест 1: сортировка по убыванию (sort_type_forward=True) — по умолчанию
        (
            [{"id": 1, "date": "2023-01-01"}, {"id": 2, "date": "2023-03-15"}, {"id": 3, "date": "2023-02-10"}],
            True,
            [{"id": 2, "date": "2023-03-15"}, {"id": 3, "date": "2023-02-10"}, {"id": 1, "date": "2023-01-01"}],
        ),
        # Тест 2: сортировка по возрастанию (sort_type_forward=False)
        (
            [{"id": 1, "date": "2023-01-01"}, {"id": 2, "date": "2023-03-15"}, {"id": 3, "date": "2023-02-10"}],
            False,
            [{"id": 1, "date": "2023-01-01"}, {"id": 3, "date": "2023-02-10"}, {"id": 2, "date": "2023-03-15"}],
        ),
        # Тест 3: пустой список
        ([], True, []),
        # Тест 4: один элемент
        ([{"id": 1, "date": "2023-05-20"}], True, [{"id": 1, "date": "2023-05-20"}]),
        # Тест 5: одинаковые даты
        (
            [{"id": 1, "date": "2023-01-01"}, {"id": 2, "date": "2023-01-01"}, {"id": 3, "date": "2023-01-01"}],
            True,
            [
                {"id": 1, "date": "2023-01-01"},
                {"id": 2, "date": "2023-01-01"},
                {"id": 3, "date": "2023-01-01"},
            ],  # порядок может сохраниться или измениться — sorted стабилен
        ),
        # Тест 6: разные форматы дат (если ожидается ISO формат)
        (
            [{"id": 1, "date": "2022-12-31"}, {"id": 2, "date": "2023-01-01"}, {"id": 3, "date": "2021-06-15"}],
            True,
            [{"id": 2, "date": "2023-01-01"}, {"id": 1, "date": "2022-12-31"}, {"id": 3, "date": "2021-06-15"}],
        ),
        # Тест 7: словари с дополнительными полями
        (
            [
                {"id": 1, "date": "2023-03-01", "amount": 100},
                {"id": 2, "date": "2023-01-15", "amount": 200},
                {"id": 3, "date": "2023-02-20", "description": "payment"},
            ],
            True,
            [
                {"id": 1, "date": "2023-03-01", "amount": 100},
                {"id": 3, "date": "2023-02-20", "description": "payment"},
                {"id": 2, "date": "2023-01-15", "amount": 200},
            ],
        ),
    ],
)
def test_sort_by_date(list_of_dicts: list[dict], sort_type_forward: bool, expected: list[dict]) -> None:
    result = processing.sort_by_date(list_of_dicts, sort_type_forward)
    assert result == expected


# =========================
# ТЕСТЫ ДЛЯ process_bank_search
# =========================

@pytest.fixture
def sample_data():
    return [
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
        {"description": "Перевод частному лицу"},
        {"description": "ПОКУПКА В МАГАЗИНЕ"},
        {"no_description": "что-то"},  # битый кейс
    ]


def test_search_found(sample_data):
    result = processing.process_bank_search(sample_data, "организации")

    assert len(result) == 1
    assert result[0]["description"] == "Перевод организации"


def test_search_case_insensitive(sample_data):
    result = processing.process_bank_search(sample_data, "покупка")

    assert len(result) == 1
    assert result[0]["description"] == "ПОКУПКА В МАГАЗИНЕ"


def test_search_not_found(sample_data):
    result = processing.process_bank_search(sample_data, "ипотека")

    assert result == []


def test_search_partial_match(sample_data):
    result = processing.process_bank_search(sample_data, "перевод")

    assert len(result) == 2


def test_search_missing_description(sample_data):
    # не должен падать
    result = processing.process_bank_search(sample_data, "что-то")

    assert isinstance(result, list)


# =========================
# ТЕСТЫ ДЛЯ process_bank_operations
# =========================

@pytest.fixture
def operations_data():
    return [
        {"description": "Перевод организации"},
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
        {"description": "Покупка"},
        {"no_description": "битый кейс"},
    ]


def test_operations_count_basic(operations_data):
    categories = ["Перевод организации", "Открытие вклада"]

    result = processing.process_bank_operations(operations_data, categories)

    assert result == {
        "Перевод организации": 2,
        "Открытие вклада": 1,
    }


def test_operations_missing_category(operations_data):
    categories = ["Перевод организации", "Ипотека"]

    result = processing.process_bank_operations(operations_data, categories)

    assert result == {
        "Перевод организации": 2,
    }


def test_operations_empty_data():
    result = processing.process_bank_operations([], ["Перевод организации"])

    assert result == {}


def test_operations_no_matches():
    data = [{"description": "Покупка"}]
    categories = ["Перевод организации"]

    result = processing.process_bank_operations(data, categories)

    assert result == {}


def test_operations_ignore_missing_description():
    data = [
        {"description": "Перевод организации"},
        {"bad_key": "что-то"},
    ]
    categories = ["Перевод организации"]

    result = processing.process_bank_operations(data, categories)

    assert result == {"Перевод организации": 1}