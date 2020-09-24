from math import *
from typing import Iterable, Tuple


__all__ = ("from_polar", "crumble", "nearby_cells", "next_cell")


# ****** Globals ******
# **** Types ****
Cell = Tuple[int, int]

# **** Constants ****
eighth = tau / 8


def from_polar(radius, angle, rotation=0):
    x = radius * cos(angle + rotation)
    y = radius * sin(angle + rotation)
    return x, y


def crumble(lower: int, upper: int, start: int = None) -> Iterable[int]:
    """Return number n above and n below the start index
    where n is incremented until both bounds are exceeded.

    If start is omitted, acts like range.
    """
    if start is None:
        start = lower

    if not lower <= start < upper:
        yield start
        return

    finished_upper = False
    finished_lower = False
    count = 1
    yield start
    while not (finished_upper and finished_lower):
        if not start + count >= upper:
            yield start + count
        else:
            finished_upper = True

        if not start - count < lower:
            yield start - count
        else:
            finished_lower = True

        count += 1


def nearby_cells(i, j, power, *, angle=None) -> Iterable[Cell]:
    """
    12 14 16 18 23
    11 02 04 07 22
    10 01 !! 06 21
    09 00 03 05 20
    08 13 15 17 19
    """

    if angle is None:
        # start in the SW corner
        p2 = pow(power, 2) - 1
        angle = (5 * p2 / 8) * (tau / p2)

    for p in range(2, power + 1, 2):
        half = p // 2
        xh, yh = map(round, from_polar(half, angle))

        for k in crumble(-half, +half + 1, xh):
            for m in crumble(-half, +half + 1, yh):
                # if on the outer edge
                if not (abs(k) < half and abs(m) < half):
                    yield (i + k, j + m)


def next_cell(i: int, j: int, angle: float, *, power: int = 3) -> Cell:
    k, m = tuple(map(round, from_polar(power // 2, angle)))
    return i + k, j + m
