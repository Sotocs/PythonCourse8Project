import logging
import os
from typing import Union

log_dir = "../logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "masks.log")

logger = logging.getLogger(__name__)
handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
handler.setFormatter(logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
logger.addHandler(handler)


def get_mask_card_number(number: Union[str, int]) -> str:
    """
    Маскирует номер карты: первые 6 цифр видны, с 7‑й по 12‑ю — звёздочки, последние 4 — видны.
    Формат: 1234 56** **** 3456
    """
    logger.debug("Программа запущена")
    number = "".join(str(number).split(" "))
    if len(number) != 16:
        logger.error(f"Ошибка: Неправильный формат ввода, входные данные: {number}")
        raise ValueError(f"Неправильный формат, входные данные: {number}")
    else:
        logger.debug(f"Программа успешно выполнена с входными данными:{number}")
        return str(number)[-16:-12] + " " + str(number)[-12:-10] + "** **** " + str(number)[-4:]


def get_mask_account(number: Union[str, int]) -> str:
    """
    Маскирует номер счёта: все цифры, кроме последних 4, заменяются на звёздочки.
    Формат: (**** 1234).
    """
    logger.debug("Программа запущена")
    number = "".join(str(number).split(" "))
    if len(number) != 16:
        logger.error(f"Ошибка: Неправильный формат ввода, входные данные: {number}")
        raise ValueError("Неправильный формат, входные данные: {number}")
    else:
        logger.debug(f"Программа успешно выполнена с входными данными:{number}")
        return "**** " + number[-4:]
