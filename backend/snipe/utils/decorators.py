import time


def exetime(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        duration = round((end - start) * 1000)
        print(f"Function {func.__name__}() took {duration}ms.\n")
        return result

    return wrapper
