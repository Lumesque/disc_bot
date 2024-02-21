from contextlib import contextmanager

@contextmanager
def print_traceback(msg):
    try:
        yield
    except Exception:
        print(msg)
        traceback.print_exc()
