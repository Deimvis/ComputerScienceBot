import inspect


def get_class_attributes(cls):
    attrs = inspect.getmembers(cls, lambda member: not(inspect.isroutine(member)))
    is_class_attriute = lambda attribute: not attribute[0].startswith('__')
    class_attrs = filter(is_class_attriute, attrs)
    return list(map(lambda attr: attr[1], class_attrs))
