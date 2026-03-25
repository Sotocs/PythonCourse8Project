from typing import Union
import logging

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("../logs", mode="w")
file_formatter = logging.Formatter("%(asctime)s %(funcName)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logging.basicConfig(level=logging.DEBUG)


def get_mask_card_number(number: Union[str, int]) -> str:
    """
    Маскирует номер карты: первые 6 цифр видны, с 7‑й по 12‑ю — звёздочки, последние 4 — видны.
    Формат: 1234 56** **** 3456
    """
    logger.addHandler(file_handler)
    logger.debug("Программа запущена")
    number = "".join(str(number).split(" "))
    if len(number) != 16:
        logger.warning(f"Ошибка: Неправильный формат ввода, входные данные: {number}")
        raise ValueError(f"Неправильный формат, входные данные: {number}")
    else:
        logger.debug(f"Программа успешно выполнена с входными данными:{number}")
        return str(number)[-16:-12] + " " + str(number)[-12:-10] + "** **** " + str(number)[-4:]


def get_mask_account(number: Union[str, int]) -> str:
    """
    Маскирует номер счёта: все цифры, кроме последних 4, заменяются на звёздочки.
    Формат: (**** 1234).
    """
    logger.addHandler(file_handler)
    logger.debug("Программа запущена")
    number = "".join(str(number).split(" "))
    if len(number) != 16:
        logger.warning(f"Ошибка: Неправильный формат ввода, входные данные: {number}")
        raise ValueError("Неправильный формат, входные данные: {number}")
    else:
        logger.debug(f"Программа успешно выполнена с входными данными:{number}")
        return "**** " + number[-4:]
