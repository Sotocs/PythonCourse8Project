
# PythonCourse10Project


Учебный Python‑проект для обработки финансовых данных: маскирования номеров карт и счетов, фильтрации и сортировки операций.

## Структура проекта


```
PythonCourse8Project/
├── scr/
│   ├── masks.py        # Маскирование номеров карт и счетов
│   ├── processing.py  # Фильтрация и сортировка операций
│   ├── widget.py      # Высокоуровневые функции для вывода данных
│   └── __init__.py
├── tests/             # Тесты для всех модулей
├── README.md
└── requirements.txt
```
```

## Описание модулей

### masks.py

Функции для маскирования конфиденциальных данных:
* маскирование номера банковской карты (например, `Visa Classic 6831 98** **** 7654`);
* маскирование номера счёта (например, `Счёт **4305`).

### processing.py

Обработка операций:
* `filter_by_state` — фильтрация по статусу (`EXECUTED`, `CANCELED`);
* `sort_by_date` — сортировка по дате (по возрастанию/убыванию).

### widget.py

Объединяет функциональность проекта:
* форматирует данные операций;
* использует функции из `masks.py` и `processing.py`;
* подготавливает информацию для вывода пользователю.

## Пример использования

```python
from scr.processing import filter_by_state, sort_by_date
from scr.widget import get_date, mask_account_card

operations = [
    {"state": "EXECUTED", "date": "2019-08-26T10:50:58.294041"},
    {"state": "CANCELED", "date": "2018-12-23T11:47:52.403285"},
]

executed = filter_by_state(operations)
sorted_ops = sort_by_date(executed)
print(sorted_ops)
```

## Технологии

* Python 3.x;
* стандартная библиотека Python;
* модульная архитектура.

## Запуск проекта

1. Клонируйте репозиторий:
```bash
git clone https://github.com/Sotocs/PythonCourse8Project.git
cd PythonCourse8Project
```
2. Установите зависимости:
```bash
pip install -r requirements.txt
```
3. Запускайте и тестируйте функции через Python‑интерпретатор или IDE.

## Тестирование

**Запуск тестов:**
```bash
pytest tests/          # все тесты
pytest -v tests/       # подробный вывод
pytest -x tests/      # остановка на первой ошибке
```

**Проверка покрытия кода:**
```bash
coverage run -m pytest tests/
coverage report        # текстовый отчёт
coverage html          # HTML‑отчёт (папка htmlcov/)
```

**Ожидаемые стандарты:**
* покрытие кода ≥ 85 %;
* все тесты проходят без ошибок;
* соответствие PEP 8 (`flake8`).

## Требования к зависимостям

В `requirements.txt`:
```
pytest>=7.0
pytest-cov>=4.0
coverage>=6.0
flake8>=6.0
```

## Назначение проекта

Проект создан в учебных целях и демонстрирует:
* работу с данными;
* разделение логики по модулям;
* чистый и читаемый код;
* базовые принципы Python‑архитектуры.

## Лицензия

Проект распространяется свободно и может использоваться в учебных целях.

