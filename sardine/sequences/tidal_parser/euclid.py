from typing import List

from utils import flatten


def bjorklund(k: int, n: int, safe=True) -> List[int]:
    """Applies Bjorklund's algorithm for generating an euclidean rhythm sequence"""

    if not safe:
        if k > n:
            raise ValueError("k should be <= n")
        if k < 0 or n < 0:
            raise ValueError("k and n should be non-negative integers")

    # Instead of throwing exception, make sure `n` and `k are valid by taking
    # the absolute value of `n`` and `k % n` respectively.
    n = abs(n)
    k = abs(k % n)

    if n == 0 or k == 0:
        return []

    bins = [[1] for _ in range(k)]
    if n == k:
        return flatten(bins)
    remainders = [[0] for _ in range(n - k)]

    while len(remainders) > 1:
        new_remainders = []
        for i, bin in enumerate(bins):
            if not remainders:
                new_remainders.append(bin)
            else:
                bin += remainders.pop(0)
                bins[i] = bin

        if new_remainders:
            bins = bins[: -len(new_remainders)]
            remainders = new_remainders

    return flatten(bins + remainders)
