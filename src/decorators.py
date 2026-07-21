import time
from typing import Any, Callable, Optional
from functools import wraps



def log(filename=None):
    """
       Декоратор, который  логирует  начало, конец и продолжительность выполнения функции,
       ее результаты или возникшие ошибки.
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
              log_message = f'{func.__name__} started\nGetting started: {time_start}\n{func.__name__} finished\nEnd of work: {time_end}\nTime for work: {time_end - time_start}\nResult: {result},\nПереданные аргументы {args}, {kwargs}\n\n'
              if filename:
                with open(filename, "a", encoding="utf-8") as file:
                   file.write(log_message)
              else:
                print(log_message)
              return result
          except Exception as e:
             log_message_error = f'{func.__name__} error: {type(e).__name__}. Inputs: {args},{kwargs}\n'

             if filename:
                with open(filename, "a", encoding="utf-8") as file:
                   file.write('\n'+log_message_error)
             else:
                print(log_message_error)
          raise Exception("Type error")
       return inner
    return wrapper




@log()
def my_function(x, y):
    """Выполняет суммирование двух чисел."""
    for i in range(100000000):
        continue
    return x + y

