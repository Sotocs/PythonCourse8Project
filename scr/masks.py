from typing import Union


def get_mask_card_number(number: Union[str, int]) -> str:
    """
    Маскирует номер карты: первые 6 цифр видны, с 7‑й по 12‑ю — звёздочки, последние 4 — видны.
    Формат: 1234 56** **** 3456
    """
    number = ''.join(str(number).split(' '))
    if len(number) != 16:
        raise ValueError("Неправильный формат")
    else:
        return str(number)[-16:-12] + " " + str(number)[-12:-10] + "** **** " + str(number)[-4:]



def get_mask_account(number: Union[str, int]) -> str:
    """
    Маскирует номер счёта: все цифры, кроме последних 4, заменяются на звёздочки.
    Формат: (**** 1234).
    """
    number = ''.join(str(number).split(' '))
    if len(number) != 16:
        raise ValueError("Неправильный формат")
    else:
        return "**** " + str(number)[-4:]

print(get_mask_card_number('1234 4344 3333 3456'))