import pytest
from scr import widget


def test_mask_account_card():
    assert widget.mask_account_card("Счет 1234564323133456") == "**** 3456"
    assert widget.mask_account_card("Maestro 1596837868705199") == "1596 83** **** 5199"
    with pytest.raises(ValueError) as exc_info:
        assert widget.mask_account_card("Счет 64686473678894779589")
        print(exc_info)
    with pytest.raises(ValueError) as exc_info:
        widget.mask_account_card("MasterCard 7158 3007 3472 6758")
        print(exc_info)
    with pytest.raises(ValueError) as exc_info:
        widget.mask_account_card("Счет 353830334744478955")
        print(exc_info)
    #           'Visa Classic 6831982476737658',
    #           'Visa Platinum 8990922113665229',
    #           'Visa Gold 5999414228426353',
    #           'Счет 73654108430135874305']:
    #     print(mask_account_card(e))


def test_get_date():
    assert widget.get_date("2024-03-11T02:26:18.671407") == "11.03.2024"
    assert widget.get_date("2025-04-20T02:26:18.671407") == "20.04.2025"
    with pytest.raises(ValueError) as exc_info:
        widget.get_date("2025-04-T02:26:18.671407")
        print(exc_info)
    with pytest.raises(ValueError) as exc_info:
        widget.get_date("2025-04-T02:26:18.6")
        print(exc_info)
