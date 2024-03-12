from functools import wraps
from sys import stderr
from time import perf_counter

from loguru import logger


def time_measure_decorator(func):
    """Decorator para medição de tempo de execução."""
    logger.add(
        sink=stderr,
        format="{time} - {level} - {message} - {file}",
        level="INFO",
    )

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = perf_counter()
        result = func(*args, **kwargs)
        end_time = perf_counter()
        logger.info(f"Name: {func.__name__} - Time: {end_time - start_time:.2f}s")
        return result

    return wrapper


def log_decorator(func):
    """Decorator para logar exception."""
    logger.add(
        sink="logs/logs_exception.log",
        format="{time} - {level} - {message} - {file}",
        level="ERROR",
    )

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            logger.exception(f"Exception gerada em {func.__name__}. Exception: {e}")
            raise e

    return wrapper
