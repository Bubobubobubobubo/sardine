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
    if isinstance(value, list):
        return [func(x) for x in value]
    else:
        return func(value)


def force_value_to_list(value):
    """Convert a value to a singleton list, if it is not already a list"""
    if isinstance(value, list):
        # Already a list
        return value
    else:
        # Make a singleton
        return [value]


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
    return [
        func(x, y)
        for x, y in zip_cycle(force_value_to_list(left), force_value_to_list(right))
    ]
