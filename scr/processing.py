from typing import Any


def filter_by_state(list_of_dicts: list[dict], argument: str = "EXECUTED") -> list[dict]:
    """Функция сортирует список словарей по ключевому слову.
    По умолчанию EXECUTED. Выводит список подходящих словарей"""
    filtered_list = []
    for d in list_of_dicts:
        if d["state"] == argument:
            filtered_list.append(d)
    return filtered_list


def sort_by_date(list_of_dicts: list[dict], sort_type_forward: bool = True) -> list[Any]:
    """Функция принимает список словарей и необязательный параметр,
     задающий порядок сортировки (по умолчанию — убывание).
    Функция возвращает новый список, отсортированный по дате"""
    sorted_list = sorted(list_of_dicts, key=lambda d: d["date"], reverse=sort_type_forward)
    return sorted_list
