import traceback
from contextlib import contextmanager


@contextmanager
def print_traceback(msg):
    try:
        yield
    except Exception:  # noqa: BLE001
        print(msg)
        traceback.print_exc()
