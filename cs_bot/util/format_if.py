

def format_if(string, *args, condition=lambda args: None not in args, default=''):
    if not condition(args):
        return default
    return string.format(*args)
