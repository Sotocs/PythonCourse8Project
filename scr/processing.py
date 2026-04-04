import re
from collections import Counter
from pprint import pprint
from typing import Any

from scr.generators import transaction_descriptions


def filter_by_state(list_of_dicts: list[dict], argument: str = "EXECUTED") -> list[dict]:
    """Функция сортирует список словарей по ключевому слову.
    По умолчанию EXECUTED. Выводит список подходящих словарей"""
    filtered_list = []
    for d in list_of_dicts:
        if "state" in d:
            if d["state"] == argument:
                filtered_list.append(d)
        else:
            filtered_list.append(d)
    return filtered_list


def sort_by_date(list_of_dicts: list[dict], sort_type_forward: bool = True) -> list[Any]:
    """Функция принимает список словарей и необязательный параметр,
     задающий порядок сортировки (по умолчанию — убывание).
    Функция возвращает новый список, отсортированный по дате"""
    filtered_list = [d for d in list_of_dicts if "date" in d]
    sorted_list = sorted(filtered_list, key=lambda d: d["date"], reverse=sort_type_forward)
    return sorted_list


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """Функцию, которая принимает список словарей с данными о банковских
     операциях и строку поиска, а возвращать список словарей, у которых в
    описании есть данная строка.
    """
    result = []
    pattern = re.compile(search, re.IGNORECASE)
    for e in data:
        if "description" in e:
            if pattern.findall(e["description"]):
                result.append(e)
    return result


def process_bank_operations(data: list[dict], categories: list) -> dict:
    """Функция, которая принимает список словарей с данными о банковских операциях
     и список категорий операций, а возвращать словарь, в котором ключи — это названия категорий,
    а значения — это количество операций в каждой категории.
    """
    result = dict()
    descriptions = []
    for e in transaction_descriptions(data):
        descriptions.append(e)
    counter = Counter(descriptions)
    for category in categories:
        if category in counter:
            result[category] = counter[category]
    return result
