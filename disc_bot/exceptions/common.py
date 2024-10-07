import traceback
from contextlib import contextmanager


@contextmanager
def e_print(message, print_stack=True, expected_exception=Exception):
    try:
        yield
    except expected_exception:
        print(message)
        if print_stack:
            traceback.print_exc()
