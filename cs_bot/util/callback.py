from functools import wraps


_DEFAULT_DELIM = ';'


class CallChecker:
    def __init__(self, call, delim=_DEFAULT_DELIM):
        self._state = True
        self._call = call.data.split(delim)

    def __bool__(self):
        return self._state

    def __lazy_evaluation(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if self._state is False:
                return self
            return func(self, *args, **kwargs)
        return wrapper

    @__lazy_evaluation
    def like(self, *pattern):
        self.length(len(pattern))
        for ind, item in enumerate(pattern):
            if self._state is False:
                return self
            if isinstance(item, str):
                self._has(item, ind)
            elif isinstance(item, list):
                self._has_from(item, ind)
            else:
                self._state = False
        return self

    @__lazy_evaluation
    def length(self, value):
        self._check(len(self._call) == value)
        return self

    @__lazy_evaluation
    def has(self, value, ind=None):
        if ind is None:
            self._check(value in self._call)
        else:
            self._check(len(self._call) > ind)
            self._has(value, ind)
        return self

    @__lazy_evaluation
    def has_from(self, values, ind=None):
        if ind is None:
            self._check(any(map(lambda value: value in self._call, values)))
        else:
            self._check(len(self._call) > ind)
            self._has_from(values, ind)
        return self

    @__lazy_evaluation
    def _has(self, value, ind):
        self._check(self._call[ind] == value)

    @__lazy_evaluation
    def _has_from(self, values, ind):
        self._check(self._call[ind] in values)

    @__lazy_evaluation
    def _check(self, expression):
        self._state = self._state and expression


class CallBuilder:
    def __init__(self, delim=_DEFAULT_DELIM):
        self.delim = delim

    def make(self, *args):
        return self.delim.join(args)


class CallParser:
    def __init__(self, call, delim=_DEFAULT_DELIM):
        self._call = call.data.split(delim)

    def get(self, ind):
        return self._call[ind]
