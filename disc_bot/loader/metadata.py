import importlib.metadata 
import inspect


def candidates(arg):
    return importlib.metadata.entry_points()[arg]

def load(func_meta_data):
    return func_meta_data.load()

def run(func, **potential_args):
    args = inspect.getargs(func.__code__).args
    return func(**{
        x: potential_args[x] for x in potential_args.keys()
        if x in args
        })


