# PythonCourse10Project

Учебный Python-проект для обработки финансовых данных: маскирования номеров карт и счетов, фильтрации, сортировки и
эффективной работы с транзакциями.

---

## Структура проекта

```
PythonCourse8Project/
├── data/
│   └── operations.json        # JSON-файл с финансовыми транзакциями
│
├── scr/                       # Основной код проекта
│   ├── __init__.py
│   ├── decorators.py          # Декоратор log для логирования функций
│   ├── external_api.py        # Работа с внешним API (конвертация валют)
│   ├── generators.py          # Генераторы для обработки данных
│   ├── main.py                # Точка входа / запуск программы
│   ├── masks.py               # Маскирование карт и счетов
│   ├── processing.py          # Фильтрация и сортировка операций
│   ├── utils.py               # Загрузка данных из JSON
│   └── widget.py              # Форматирование и вывод данных
│
├── tests/                     # Тесты (pytest)
│   ├── __init__.py
│   ├── test.py
│   ├── test_decorators.py
│   ├── test_external_api.py
│   ├── test_generators.py
│   ├── test_masks.py
│   ├── test_processing.py
│   ├── test_utils.py
│   └── test_widget.py
│
├── htmlcov/                   # Отчёт покрытия (coverage)
├── .env.example               # Шаблон переменных окружения
├── README.md
└── requirements.txt
```

---

## Описание функций проекта

Проект содержит набор функций для обработки финансовых операций, включая фильтрацию, сортировку, форматирование и защиту
чувствительных данных.

### Маскирование данных (`masks.py`)

Функции этого модуля предназначены для защиты конфиденциальной информации:

* маскирование номеров банковских карт (скрывает часть цифр);
* маскирование номеров счетов (отображает только последние цифры).

Это позволяет безопасно отображать данные пользователю без риска утечки.

---

### Обработка операций (`processing.py`)

Модуль отвечает за работу со списками транзакций:

* фильтрация операций по заданным параметрам (например, по статусу выполнения);
* сортировка операций по дате (по возрастанию или убыванию).

Функции помогают структурировать данные перед выводом или дальнейшей обработкой.

---

### Форматирование и вывод (`widget.py`)

Модуль объединяет функциональность проекта и подготавливает данные для отображения:

* форматирует даты операций;
* применяет маскирование к картам и счетам;
* формирует удобный для пользователя вид информации.

---

### Генераторы (`generators.py`)

Модуль реализует функции-генераторы для поэтапной обработки данных:

* фильтрация транзакций с использованием итераторов;
* последовательное получение данных без загрузки всего списка в память;
* генерация значений (например, номеров карт) по заданным параметрам.

Использование генераторов делает обработку более эффективной и гибкой.

---

## Декоратор `log`

Декоратор `log` автоматически логирует выполнение функций.

- **Успешное выполнение:**  
  "Function {func.__name__} executed successfully with result {result}"

- **При ошибке:**  
  "Function {func.__name__} raised exception {e} with arguments args {args}, kwargs {kwargs}"

**Параметры:**

- `filename` (необязательный) — путь к файлу для логов.
- Если указан, запись идёт в файл.
- Если не указан, вывод идёт в консоль.

## Пример использования

```python
from scr.processing import filter_by_state, sort_by_date
from scr.widget import get_date, mask_account_card
from scr.generators import filter_by_currency

operations = [
    {
        "state": "EXECUTED",
        "date": "2019-08-26T10:50:58.294041",
        "amount": {"currency": "USD"},
    },
    {
        "state": "CANCELED",
        "date": "2018-12-23T11:47:52.403285",
        "amount": {"currency": "EUR"},
    },
]

# фильтрация по статусу
executed = filter_by_state(operations)

# сортировка по дате
sorted_ops = sort_by_date(executed)

# фильтрация по валюте (генератор)
usd_ops = filter_by_currency(sorted_ops, "USD")

for op in usd_ops:
    print(op)
```

---

## Примеры генераторов

### Фильтрация по валюте

```python
from scr.generators import filter_by_currency

for transaction in filter_by_currency(transactions, "USD"):
    print(transaction)
```

---

### Описания транзакций

```python
from scr.generators import transaction_descriptions

for desc in transaction_descriptions(transactions):
    print(desc)
```

---

### Генерация номеров карт

```python
from scr.generators import card_number_generator

for card in card_number_generator(1, 3):
    print(card)
```

### Пример для Log:

```python
@log(filename="log.txt")
def add(a, b):
    return a + b
```

---

## Технологии

* Python 3.x;
* стандартная библиотека Python;
* модульная архитектура;
* генераторы и итераторы.

---

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

3. Запускайте и тестируйте функции через Python-интерпретатор или IDE.

---

## Тестирование

### Запуск тестов

```bash
pytest tests/        # все тесты
pytest -v tests/     # подробный вывод
pytest -x tests/     # остановка на первой ошибке
```

### Проверка покрытия кода

```bash
coverage run -m pytest tests/
coverage report
coverage html
```

---

## Требования к качеству

* покрытие кода ≥ 80–85%;
* все тесты проходят без ошибок;
* соответствие стандарту PEP 8 (`flake8`).

---

## Требования к зависимостям

```
pytest>=7.0
pytest-cov>=4.0
coverage>=6.0
flake8>=6.0
```

---

## Назначение проекта

Проект создан в учебных целях и демонстрирует:

* работу с финансовыми данными;
* разделение логики по модулям;
* чистый и читаемый код;
* использование генераторов для оптимизации;
* базовые принципы архитектуры Python-приложений.

---

## Лицензия

Проект распространяется свободно и может использоваться в учебных целях.
