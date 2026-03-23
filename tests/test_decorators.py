import pytest
from scr import decorators


# Тест: функция успешно выполняется и пишет в консоль
def test_log_success(capsys):
    @decorators.log()
    def add(a, b):
        return a + b

    result = add(1, 2)

    # Перехватываем вывод в консоль
    captured = capsys.readouterr()

    # Проверяем результат функции
    assert result == 3

    # Проверяем, что в консоль вывелось сообщение
    assert "Function add executed successfully with result 3" in captured.out


# Тест: функция падает с ошибкой и логирует её
def test_log_error(capsys):
    @decorators.log()
    def divide(a, b):
        return a / b

    # Проверяем, что ошибка действительно возникает
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)

    captured = capsys.readouterr()

    # Проверяем текст ошибки в логе
    assert "Function divide raised exception division by zero with arguments args (1, 0), kwargs {}" in captured.out


# Тест: проверяем, что имя функции не теряется
def test_log_name():
    @decorators.log()
    def my_func():
        return "ok"

    assert my_func.__name__ == "my_func"
