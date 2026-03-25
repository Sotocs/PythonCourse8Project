import dotenv
import os
import requests

dotenv.load_dotenv()


def convertation(transaction: dict) -> float:
    """
    Функция, которая принимает на вход транзакцию
     и возвращает сумму транзакции (amount) в рублях,
      тип данных — float. Если транзакция была в USD или EUR,
       происходит обращение к внешнему API для получения
        текущего курса валют и конвертации суммы операции в рубли
    """
    currency = transaction["operationAmount"]["currency"]["code"]
    if currency == "RUB":
        amount = float(transaction["operationAmount"]["amount"])
        return amount
    elif currency == "USD" or currency == "EUR":
        API_KEY = os.getenv("EXCHANGE_API_KEY")

        amount = float(transaction["operationAmount"]["amount"])
        BASE_URL = os.getenv("EXCHANGE_API_URL")
        url = f"{BASE_URL}?to=RUB&from={currency}&amount={amount}"
        if not API_KEY:
            raise ValueError("Не указан ключ API в .env")
        headers = {"apikey": API_KEY}
        response = requests.get(url, headers=headers)
        data = response.json()
        return float(data.get("result", 0))

    raise ValueError(f"Неизвестная валюта: {currency}")

