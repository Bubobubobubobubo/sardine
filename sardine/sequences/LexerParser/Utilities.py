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


def map_unary_function(func, value):
    """Apply an unary function to a value or a list of values

    Args:
        func: The function to apply
        value: The value or the list of values
    """
    if isinstance(value, (float, int)):
        return func(value)
    if isinstance(value, list):
        return [func(x) for x in value]
    return None


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
    if all(map(lambda x: isinstance(x, (float, int)), [left, right])):
        return func(left, right)
    if all(map(lambda x: isinstance(x, list), [left, right])):
        return [func(x, y) for x, y in zip_cycle(left, right)]
    if isinstance(left, (int, float)) and isinstance(right, list):
        return [func(left, x) for x in right]
    if isinstance(left, list) and isinstance(right, (float, int)):
        return [func(x, right) for x in left]
    return None
