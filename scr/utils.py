import csv
import json
import logging

import pandas as pd

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("../logs/utils.log", encoding="utf-8", mode="w")
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def load_transactions(path: str) -> list:
    """
    Функция, которая принимает на вход путь до JSON-файла
     и возвращает список словарей с данными о финансовых
      транзакциях. Если файл пустой, содержит не список
       или не найден, функция возвращает пустой список.
    """

    logger.debug("Программа запущена")
    try:
        # Открываем файл с правильной кодировкой
        if path.endswith(".json"):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)  # Загружаем JSON
            logger.debug("Файл открыт с необходимой кодировкой в формате json")
            # Проверяем, что в файле действительно список
            if isinstance(data, list):
                logger.debug("Проверка на список в исходном файле пройдена")
                return data
            else:
                return []

        elif path.endswith(".csv"):
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                data = list(reader)
            logger.debug("Файл открыт с необходимой кодировкой в формате csv")
            # Проверяем, что в файле действительно список
            if isinstance(data, list):
                logger.debug("Проверка на список в исходном файле пройдена")
                return data
            else:
                return []

        elif path.endswith(".xlsx"):
            data = pd.read_excel(path)
            data_list = data.to_dict("records")
            logger.debug("Файл открыт с необходимой кодировкой в формате xlsx")
            # Проверяем, что в файле действительно список
            if isinstance(data_list, list):
                logger.debug("Проверка на список в исходном файле пройдена")
                return data_list
            else:
                return []

        else:
            logger.error("Проверка на список в исходном файле не пройдена," " возвращается пустой список")
            return []  # Если не список, возвращаем пустой

    except FileNotFoundError:
        logger.error(f"Файл не найден: {path}")
        return []
    except (json.JSONDecodeError, UnicodeDecodeError, IOError):
        # Если файл поврежден, пустой или кодировка неправильная
        logger.error(f"Файл {path} поврежден, пустой или кодировка неправильная, возвращается пустой список")
        return []
    except Exception as e:
        logger.error(f"Неожиданная ошибка при чтении файла {path}: {e}")
        return []
