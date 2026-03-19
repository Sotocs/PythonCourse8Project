from typing import Generator


def filter_by_currency(list_of_dicts: list[dict], currency: str) -> Generator:
    """
    Функция filter_by_currency обрабатывает список словарей
    с транзакциями и возвращает итератор, содержащий только
    транзакции с указанной валютой (например, USD).
    """
    for e in list_of_dicts:
        if e["operationAmount"]["currency"]["code"] == currency:
            yield e


def transaction_descriptions(list_of_dicts: list[dict]) -> Generator:
    """
    Генератор, который принимает на вход перечень словарей,
    содержащих информацию о транзакциях, и последовательно
    генерирует описание каждой из операций.
    """
    for e in list_of_dicts:
        yield e["description"]


def card_number_generator(a: int, b: int) -> Generator:
    """
    Генератор выдает номера банковских карт в формате
    'XXXX XXXX XXXX XXXX', где 'X' представляет
    собой цифру номера карты. Программа способна
    генерировать номера карт в пределах заданного
    диапазона от 0000 0000 0000 0001 до 9999 9999 9999 9999.
    """
    for num in range(a, b + 1):
        # Форматируем число в строку длиной 16 символов с ведущими нулями
        card_str = f"{num:016d}"
        # Разбиваем на группы по 4 цифры и соединяем пробелами
        formatted_card = f"{card_str[:4]} {card_str[4:8]} {card_str[8:12]} {card_str[12:]}"
        yield formatted_card
