from itertools import islice, count


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
