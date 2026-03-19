import pytest
from scr import masks


@pytest.fixture()
def card_name_base():
    return 1234564323133456


@pytest.mark.parametrize(
    "card, expected",
    [
        ("1234 5643 2313 3456", "1234 56** **** 3456"),
        ("1234 5643 0000 3456", "1234 56** **** 3456"),
        ("1234 3443 0000 3776", "1234 34** **** 3776"),
    ],
)
def test_add(card, expected):
    assert masks.get_mask_card_number(card) == expected


def test_get_mask_card_number(card_name_base):
    assert masks.get_mask_card_number(card_name_base) == "1234 56** **** 3456"
    assert masks.get_mask_card_number("1234 5643 2313 3456") == "1234 56** **** 3456"
    with pytest.raises(ValueError) as exc_info:
        masks.get_mask_card_number("1234 5643 2313 34564")
        print(exc_info)
    with pytest.raises(ValueError) as exc_info:
        masks.get_mask_card_number("1234 5643 2313 3")
        print(exc_info)
    with pytest.raises(ValueError) as exc_info:
        masks.get_mask_card_number(123456432313345677)
        print(exc_info)
    with pytest.raises(ValueError) as exc_info:
        masks.get_mask_card_number(123231677)
        print(exc_info)


def test_get_mask_account(card_name_base):
    assert masks.get_mask_account(card_name_base) == "**** 3456"
    assert masks.get_mask_account("1234 43443333 3456") == "**** 3456"
    with pytest.raises(ValueError) as exc_info:
        masks.get_mask_account("1234222243443333 3456")
        print(exc_info)
    with pytest.raises(ValueError) as exc_info:
        masks.get_mask_account("123456")
        print(exc_info)
