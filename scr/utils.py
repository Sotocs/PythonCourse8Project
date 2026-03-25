import json


def load_transactions(path: str) -> list:
    """
    Функция, которая принимает на вход путь до JSON-файла
     и возвращает список словарей с данными о финансовых
      транзакциях. Если файл пустой, содержит не список
       или не найден, функция возвращает пустой список.
    """
    try:
        # Открываем файл с правильной кодировкой
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)  # Загружаем JSON

        # Проверяем, что в файле действительно список
        if isinstance(data, list):
            return data
        else:
            return []  # Если не список, возвращаем пустой

    except (json.JSONDecodeError, UnicodeDecodeError, IOError):
        # Если файл поврежден, пустой или кодировка неправильная
        return []


# print(load_transactions("../data/operations.json"))
