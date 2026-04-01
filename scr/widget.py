from typing import Any

from scr.masks import get_mask_account, get_mask_card_number
from datetime import datetime


def mask_account_card(name_number: list[str] | str) -> str:
    """Принимает строку с содержанием имени: карта или счет
    Maestro 1596837868705199
    Счет 64686473678894779589
    Выводит замаскированную строку с маской в зависимости от выбора Счет или Карта"""
    name_number = str(name_number).split(" ")
    if name_number[0] == "Счет" or name_number[0] == "Счёт":
        return str(get_mask_account(name_number[-1]))
    else:
        return str(get_mask_card_number(name_number[-1]))


# #for e in ['Maestro 1596837868705199',
#           'Счет 64686473678894779589',
#           'MasterCard 7158300734726758',
#           'Счет 35383033474447895560',
#           'Visa Classic 6831982476737658',
#           'Visa Platinum 8990922113665229',
#           'Visa Gold 5999414228426353',
#           'Счет 73654108430135874305']:
#     print(mask_account_card(e))


def get_date(date: str) -> Any:
    """Принимает строку формата: 2024-03-11T02:26:18.671407
    И возвращает строку формата:  "ДД.ММ.ГГГГ"("11.03.2024")."""
    try:
        parsed_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f")
        return parsed_date.strftime("%d.%m.%Y")
    except ValueError as e:
        raise ValueError(f"Неправильный формат даты: {e}")

# print(get_date('2024-03-11T02:26:18.671407'))
