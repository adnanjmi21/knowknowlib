"""
Functions that don't need state of knowknow engine.
Mostly are meant to generate empty/autofilled data structures or for type transformation.
"""
from collections import namedtuple


def comb(x, y):
    """
    TODO: figure out
    :param x: . separated values
    :param y: . separated values
    :return: union of unique values from x and y. . separated
    'q.w.e', 'e.r.t' -> 'e.q.r.t.w'
    """
    a = set(x.split("."))
    b = set(y.split("."))

    return ".".join(sorted(a.union(b)))


def make_cross_kwargs(*args, **kwargs):
    """
    Looks like it turns a dictionary into a named tuple.
    TODO: get rid of kwargs logic. Why generating a named tuple is named cross?
    :param args:
    :param kwargs:
    :return:
    """
    # removed caching
    if len(args):
        assert (type(args[0]) == dict)
        return make_cross_kwargs(**args[0])

    keys = tuple(sorted(kwargs))

    my_named_tuple = namedtuple("_".join(keys), keys)

    return my_named_tuple(**kwargs)


def gen_tuple_template(keys: tuple):
    """
    :param keys: a tuple of strings
    :return: a named tuple template
    ('e', 'q', 'w') -> <class '__main__.e_q_w'>
    """
    # TODO: add caching
    return namedtuple('_'.join(keys), keys)


def make_cross(key___value: dict):
    """
    :param key___value:
    :return:
    {'1': 'q', '2': 'w', '3': 'e'} -> e_q_w(e='3', q='1', w='2')
    """
    return gen_tuple_template(tuple(sorted(key___value.keys())))(**key___value)


def named_tupelize(d: dict, ctype: str):
    """
    For each key in d, try making it a named tuple. Return {namedtuple(k, ctypes): v for k, v in dict)
    :param d:
    :param ctype: category types?
    :return:
    """
    keys = sorted(ctype.split("."))

    def doit(k):
        if type(k) in [tuple, list]:
            return make_cross(dict(zip(keys, k)))
        elif len(keys) == 1:
            return make_cross({keys[0]: k})
        else:
            raise Exception(f"Cannot transform {k} into a named tuple with keys {keys}")

    return {doit(k): v for k, v in d.items()}
