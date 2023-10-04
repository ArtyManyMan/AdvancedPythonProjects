"""This module provides a decorator function for
measuring and reporting the average execution time
of a decorated function over multiple calls."""

import time


def average_time_deco(k):
    def decorator(func):
        lst_times = []

        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            lst_times.append(execution_time)

            if len(lst_times) > k:
                lst_times.pop(0)

            if len(lst_times) < k:
                print('Количество вызовов меньше необходимого числа')
            else:
                avg_time = sum(lst_times) / len(lst_times)
                print(f'Среднее время выполнения последних {k} вызовов: {avg_time} секунд')

            return result
        return wrapper
    return decorator


@average_time_deco(5)
def my_function(arg):
    res = arg + " White! You're goddamn right"
    time.sleep(1)
    return res
