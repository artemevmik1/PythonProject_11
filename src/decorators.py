import time
from functools import wraps


def log(filename=None):
    """
    Декоратор, который  логирует  начало, конец и
    продолжительность выполнения функции, ее результаты или возникшие ошибки.
    Может принимать необязательный аргумент 'filename', который определяет,
    куда будут записываться логи (в файл или в консоль)
    """

    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            try:
                time_start = time.time()
                result = func(*args, **kwargs)
                time_end = time.time()
                log_message = (
                    f"{func.__name__} started\nGetting started: "
                    f"{time_start}\n{func.__name__} finished\n"
                    f"End of work: {time_end}\n"
                    f"Time for work: {time_end - time_start}\n"
                    f"Result: {result},\n"
                    f"Переданные аргументы {args}, {kwargs}\n\n"
                )
                if filename:
                    with open(filename, "a", encoding="utf-8") as file:
                        file.write(log_message)
                else:
                    print(log_message)
                return result
            except Exception as e:
                log_message_error = f"{func.__name__} error:" f" {type(e).__name__}. Inputs:" f" {args},{kwargs}\n"

                if filename:
                    with open(filename, "a", encoding="utf-8") as file:
                        file.write("\n" + log_message_error)
                else:
                    print(log_message_error)
            raise Exception("Type error")

        return inner

    return wrapper
