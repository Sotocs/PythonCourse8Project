import pytest
from scr import masks, widget, processing

@pytest.fixture()
def card_name_base():
    return 1234564323133456

@pytest.mark.parametrize("card, expected", [('1234 5643 2313 3456', '1234 56** **** 3456'), ('1234 5643 0000 3456', '1234 56** **** 3456'), ('1234 3443 0000 3776', '1234 34** **** 3776')])
def test_add(card, expected):
    assert masks.get_mask_card_number(card) == expected

def test_get_mask_card_number(card_name_base):
    assert masks.get_mask_card_number(card_name_base) == '1234 56** **** 3456'
    assert masks.get_mask_card_number('1234 5643 2313 3456') == '1234 56** **** 3456'
    with pytest.raises(ValueError) as exc_info:
        masks.get_mask_card_number('1234 5643 2313 34564')
        print(exc_info)
    with pytest.raises(ValueError) as exc_info:
        masks.get_mask_card_number('1234 5643 2313 3')
        print(exc_info)
    with pytest.raises(ValueError) as exc_info:
        masks.get_mask_card_number(123456432313345677)
        print(exc_info)
    with pytest.raises(ValueError) as exc_info:
        masks.get_mask_card_number(123231677)
        print(exc_info)


def test_get_mask_account(card_name_base):
    assert masks.get_mask_account(card_name_base) == '**** 3456'
    assert masks.get_mask_account('1234 43443333 3456') == '**** 3456'
    with pytest.raises(ValueError) as exc_info:
        masks.get_mask_account('1234222243443333 3456')
    with pytest.raises(ValueError) as exc_info:
        masks.get_mask_account('123456')


def test_mask_account_card():
    assert widget.mask_account_card('Счет 1234564323133456') == '**** 3456'
    assert widget.mask_account_card('Maestro 1596837868705199') == '1596 83** **** 5199'
    with pytest.raises(ValueError) as exc_info:
        assert widget.mask_account_card('Счет 64686473678894779589')
    with pytest.raises(ValueError) as exc_info:
        widget.mask_account_card('MasterCard 7158 3007 3472 6758')
    with pytest.raises(ValueError) as exc_info:
        widget.mask_account_card('Счет 353830334744478955')
    #           'Visa Classic 6831982476737658',
    #           'Visa Platinum 8990922113665229',
    #           'Visa Gold 5999414228426353',
    #           'Счет 73654108430135874305']:
    #     print(mask_account_card(e))


def test_get_date():
    assert widget.get_date('2024-03-11T02:26:18.671407') == '11.03.2024'
    assert widget.get_date('2025-04-20T02:26:18.671407') == '20.04.2025'
    with pytest.raises(ValueError) as exc_info:
        widget.get_date('2025-04-T02:26:18.671407')
    with pytest.raises(ValueError) as exc_info:
        widget.get_date('2025-04-T02:26:18.6')

@pytest.fixture()
def list_of_dict1():
    return [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}, {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}, {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}, {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]


@pytest.mark.parametrize("list_of_dicts, argument, expected", [
    # Тест 1: фильтрация по умолчанию (EXECUTED)
    (
        [
            {'id': 1, 'state': 'EXECUTED'},
            {'id': 2, 'state': 'PENDING'},
            {'id': 3, 'state': 'EXECUTED'}
        ],
        'EXECUTED',
        [
            {'id': 1, 'state': 'EXECUTED'},
            {'id': 3, 'state': 'EXECUTED'}
        ]
    ),
    # Тест 2: фильтрация по PENDING
    (
        [
            {'id': 1, 'state': 'EXECUTED'},
            {'id': 2, 'state': 'PENDING'},
            {'id': 3, 'state': 'PENDING'}
        ],
        'PENDING',
        [
            {'id': 2, 'state': 'PENDING'},
            {'id': 3, 'state': 'PENDING'}
        ]
    ),
    # Тест 3: пустой список
    (
        [],
        'EXECUTED',
        []
    ),
    # Тест 4: нет подходящих элементов
    (
        [
            {'id': 1, 'state': 'EXECUTED'},
            {'id': 2, 'state': 'CANCELED'}
        ],
        'PENDING',
        []
    ),
    # Тест 5: все элементы подходят
    (
        [
            {'id': 1, 'state': 'EXECUTED'},
            {'id': 2, 'state': 'EXECUTED'}
        ],
        'EXECUTED',
        [
            {'id': 1, 'state': 'EXECUTED'},
            {'id': 2, 'state': 'EXECUTED'}
        ]
    ),
    # Тест 6: один элемент, подходящий под фильтр
    (
        [{'id': 1, 'state': 'PENDING'}],
        'PENDING',
        [{'id': 1, 'state': 'PENDING'}]
    ),
    # Тест 7: словари с разными ключами
    (
        [
            {'id': 1, 'state': 'EXECUTED', 'amount': 100},
            {'id': 2, 'state': 'PENDING', 'amount': 200},
            {'id': 3, 'state': 'EXECUTED', 'description': 'payment'}
        ],
        'EXECUTED',
        [
            {'id': 1, 'state': 'EXECUTED', 'amount': 100},
            {'id': 3, 'state': 'EXECUTED', 'description': 'payment'}
        ]
    )
])
def test_filter_by_state_2(list_of_dicts, argument, expected):
    assert processing.filter_by_state(list_of_dicts, argument) == expected

@pytest.mark.parametrize("list_of_dicts, sort_type_forward, expected", [
    # Тест 1: сортировка по убыванию (sort_type_forward=True) — по умолчанию
    (
        [
            {'id': 1, 'date': '2023-01-01'},
            {'id': 2, 'date': '2023-03-15'},
            {'id': 3, 'date': '2023-02-10'}
        ],
        True,
        [
            {'id': 2, 'date': '2023-03-15'},
            {'id': 3, 'date': '2023-02-10'},
            {'id': 1, 'date': '2023-01-01'}
        ]
    ),
    # Тест 2: сортировка по возрастанию (sort_type_forward=False)
    (
        [
            {'id': 1, 'date': '2023-01-01'},
            {'id': 2, 'date': '2023-03-15'},
            {'id': 3, 'date': '2023-02-10'}
        ],
        False,
        [
            {'id': 1, 'date': '2023-01-01'},
            {'id': 3, 'date': '2023-02-10'},
            {'id': 2, 'date': '2023-03-15'}
        ]
    ),
    # Тест 3: пустой список
    (
        [],
        True,
        []
    ),
    # Тест 4: один элемент
    (
        [{'id': 1, 'date': '2023-05-20'}],
        True,
        [{'id': 1, 'date': '2023-05-20'}]
    ),
    # Тест 5: одинаковые даты
    (
        [
            {'id': 1, 'date': '2023-01-01'},
            {'id': 2, 'date': '2023-01-01'},
            {'id': 3, 'date': '2023-01-01'}
        ],
        True,
        [
            {'id': 1, 'date': '2023-01-01'},
            {'id': 2, 'date': '2023-01-01'},
            {'id': 3, 'date': '2023-01-01'}
        ]  # порядок может сохраниться или измениться — sorted стабилен
    ),
    # Тест 6: разные форматы дат (если ожидается ISO формат)
    (
        [
            {'id': 1, 'date': '2022-12-31'},
            {'id': 2, 'date': '2023-01-01'},
            {'id': 3, 'date': '2021-06-15'}
        ],
        True,
        [
            {'id': 2, 'date': '2023-01-01'},
            {'id': 1, 'date': '2022-12-31'},
            {'id': 3, 'date': '2021-06-15'}
        ]
    ),
    # Тест 7: словари с дополнительными полями
    (
        [
            {'id': 1, 'date': '2023-03-01', 'amount': 100},
            {'id': 2, 'date': '2023-01-15', 'amount': 200},
            {'id': 3, 'date': '2023-02-20', 'description': 'payment'}
        ],
        True,
        [
            {'id': 1, 'date': '2023-03-01', 'amount': 100},
            {'id': 3, 'date': '2023-02-20', 'description': 'payment'},
            {'id': 2, 'date': '2023-01-15', 'amount': 200}
        ]
    )
])
def test_sort_by_date(list_of_dicts, sort_type_forward, expected):
    result = processing.sort_by_date(list_of_dicts, sort_type_forward)
    assert result == expected

def test_missing_date_key():
    """Тест: словарь без ключа 'date' должен вызвать KeyError."""
    data = [{'id': 1, 'name': 'test'}]
    with pytest.raises(KeyError):
        processing.sort_by_date(data)

