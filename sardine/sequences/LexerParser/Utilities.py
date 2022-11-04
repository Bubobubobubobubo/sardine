from itertools import islice, count, cycle


def floating_point_range(start, end, step):
    """Analog to range for floating point numbers

    Args:
        start (float): A minimum float
        end (float): A maximum float
        step (float): Step for increment

    Returns:
        list: A list of floats from 'start' to 'end', layed out
        every 'step'.
    """
    assert step != 0
    sample_count = int(abs(end - start) / step)
    return islice(count(start, step), sample_count)


def allow_silence_1(func):
    """Wrap a unary function to return None when called with None"""

    def result_func(x):
        if x is not None:
            return func(x)
        else:
            return None

    return result_func


def allow_silence_2(func):
    """Wrap a binary function to return None when called with None"""

    def result_func(x, y):
        if x is not None and y is not None:
            return func(x, y)
        else:
            return None

    return result_func


def map_unary_function(func, value):
    """Apply an unary function to a value or a list of values

    Args:
        func: The function to apply
        value: The value or the list of values
    """
    return [allow_silence_1(func)(x) for x in value]


def zip_cycle(left, right):
    """Zip two lists, cycling the shortest one"""
    if len(left) < len(right):
        return zip(cycle(left), right)
    else:
        return zip(left, cycle(right))


def map_binary_function(func, left, right):
    """Apply an binary function to a value or a list of values

    Args:
        func: The function to apply
        left: The left value or list of values
        right: The right value or list of values
    """
    return [allow_silence_2(func)(x, y) for x, y in zip_cycle(left, right)]
