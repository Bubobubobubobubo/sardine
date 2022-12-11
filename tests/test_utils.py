import functools
from typing import Sequence, Union

import pytest

from sardine import utils

Number = Union[float, int]


@pytest.mark.parametrize(
    "x,in_min,in_max,out_min,out_max,expected",
    [
        (1, 0, 2, 0, 100, 50),
        (1 / 3, 0, 1, 0, 4, 4 / 3),
        (1, 0, 3, 0, 4, 4 / 3),
        (3, 1, 3, 0, 1 / 64, 1 / 64),
    ],
)
def test_lerp_individual(
    x: Number,
    in_min: Number,
    in_max: Number,
    out_min: Number,
    out_max: Number,
    expected: Number,
):
    result = utils.lerp(x, in_min, in_max, out_min, out_max)
    assert isinstance(result, float)
    assert result == expected


@pytest.mark.parametrize(
    "values,span",
    [
        ([1, 3], 1),
        ([2, 2], 4),
        ([1/3, 2/3], 2),
        ([1/2, 7/2], 4),
        (range(2154), 1),
    ],
)
def test_lerp_multiple(values: Sequence[Number], span: Number):
    # Written similarly to Player.fit_period_to_timespan()
    lerper = functools.partial(
        utils.lerp, in_min=0, in_max=sum(values), out_min=0, out_max=span
    )
    results = list(map(lerper, values))
    assert sum(results) == span
