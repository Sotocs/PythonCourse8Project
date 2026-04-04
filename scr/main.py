from pprint import pprint

from scr.generators import filter_by_currency
from scr.processing import filter_by_state, process_bank_search, sort_by_date
from scr.utils import load_transactions


def main() -> None:
    while True:
        print(
            "Привет! Добро пожаловать в программу работы с банковскими транзакциями.\n"
            " Выберите необходимый пункт меню:\n"
            " 1. Получить информацию о транзакциях из JSON-файла\n"
            " 2. Получить информацию о транзакциях из CSV-файла\n"
            " 3. Получить информацию о транзакциях из XLSX-файла"
        )
        programm_choose = int(input())
        if programm_choose == 1:
            print("Для обработки выбран JSON-файл.")
            file = load_transactions("../data/operations.json")
            break
        if programm_choose == 2:
            print("Для обработки выбран CSV-файл.")
            file = load_transactions("../data/transactions.csv")
            break
        if programm_choose == 3:
            print("Для обработки выбран XLSX-файл.")
            file = load_transactions("../data/transactions_excel.xlsx")
            break
        else:
            print("Некорректный ввод, попробуйте ещё")
    while True:
        print(
            "Введите статус, по которому необходимо выполнить фильтрацию.\n"
            " Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING"
        )
        filter_status = input().upper()
        if filter_status in ["EXECUTED", "CANCELED", "PENDING"]:
            file = filter_by_state(file, filter_status)
            print(f'Операции отфильтрованы по статусу "{filter_status}"')
            break
        else:
            print("Некорректный ввод, попробуйте ещё")
    while True:
        print("Отсортировать операции по дате? Да / Нет")
        answer = input().upper()
        if answer == "ДА":
            print("Отсортировать по возрастанию или по убыванию?")
            answer2 = input().lower()
            if answer2 == "по возрастанию":
                file = sort_by_date(file, sort_type_forward=False)
                break
            if answer2 == "по убыванию":
                file = sort_by_date(file, sort_type_forward=True)
                break
        elif answer == "НЕТ":
            break
        else:
            print("Некорректный ввод, попробуйте ещё")
    while True:
        print("Выводить только рублевые транзакции? Да/Нет")
        answer = input().upper()
        if answer == "ДА":
            file = list(filter_by_currency(file, "RUB"))
            break
        elif answer == "НЕТ":
            break
        else:
            print("Некорректный ввод, попробуйте ещё")
    while True:
        print("Отфильтровать список транзакций по определенному слову в описании? Да/Нет")
        answer = input().upper()
        if answer == "ДА":
            print("Введите слово:")
            filter_word = input()
            file = process_bank_search(file, filter_word)
            break
        elif answer == "НЕТ":
            break
        else:
            print("Некорректный ввод, попробуйте ещё")
    print("Распечатываю итоговый список транзакций...")

    print(f"Всего банковских операций в выборке: {len(file)}")
    pprint(file)


if __name__ == "__main__":
    main()
