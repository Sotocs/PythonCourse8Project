import json
import logging

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("../logs", mode="w")
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)

logging.basicConfig(level=logging.DEBUG)

def load_transactions(path: str) -> list:
    """
    Функция, которая принимает на вход путь до JSON-файла
     и возвращает список словарей с данными о финансовых
      транзакциях. Если файл пустой, содержит не список
       или не найден, функция возвращает пустой список.
    """
    logger.addHandler(file_handler)
    logger.debug("Программа запущена")
    try:
        # Открываем файл с правильной кодировкой
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)  # Загружаем JSON
        logger.debug("Файл открыт с необходимой кодировкой")
        # Проверяем, что в файле действительно список
        if isinstance(data, list):
            logger.debug("Проверка на список в исходном файле пройдена")
            return data
        else:
            logger.warning("Проверка на список в исходном файле не пройдена," " возвращается пустой список")
            return []  # Если не список, возвращаем пустой

    except (json.JSONDecodeError, UnicodeDecodeError, IOError):
        # Если файл поврежден, пустой или кодировка неправильная
        logger.warning("Файл поврежден, пустой или кодировка неправильная, возвращается пустой список")
        return []
