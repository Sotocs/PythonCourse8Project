from typing import Union


def get_mask_card_number(number: Union[str, int]) -> str:
    """
    Маскирует номер карты: первые 6 цифр видны, с 7‑й по 12‑ю — звёздочки, последние 4 — видны.
    Формат: 1234 56** **** 3456
    """
    number = str(number)
    return str(number)[-16:-12] + " " + str(number)[-12:-14] + "** **** " + str(number)[-4:]


def get_mask_account(number: Union[str, int]) -> str:
    """
    Маскирует номер счёта: все цифры, кроме последних 4, заменяются на звёздочки.
    Формат: (**** 1234).
    """
    return "**** " + str(number)[-4:]
