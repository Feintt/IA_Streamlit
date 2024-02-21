import time


def execution_time(func):
    """
    Decorator that prints the time it takes for a function to execute.
    """

    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"The function {func.__name__} took {end - start} seconds to execute.")
        return result

    return wrapper
