import functools
from typing import Callable, Any, Optional


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования начала и конца выполнения функции, а также её результатов
    или возникших ошибок.

    Декоратор автоматически записывает в лог:
    - имя функции и результат выполнения при успешной операции;
    - имя функции, тип возникшей ошибки и входные параметры, если выполнение
      функции привело к ошибке.
    """

    def dec(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                result = func(*args, **kwargs)
                log_message = f"Function {func.__name__} executed successfully with result {result}"
                if filename is None or filename == "console":
                    print(log_message)
                else:
                    with open(filename, "a") as f:
                        f.write(log_message)
                return result
            except Exception as e:
                log_message = (
                    f"Function {func.__name__} raised exception {e} with arguments args {args}, kwargs {kwargs}"
                )
                if filename is None or filename == "console":
                    print(log_message)
                else:
                    with open(filename, "a") as f:
                        f.write(log_message)
                raise  #

        return wrapper

    return dec
