"""
A light vector class to make life easier.
"""

from typing import List, Union
from math import atan2, ceil, sqrt


Number = Union[int, float]


# noinspection PyAttributeOutsideInit
class Vector(list, List[Number]):
    def __init__(self, x, y):
        super().__init__((x, y))

    def angle(self, other: "Vector"):
        return atan2(other.y - self.y, other.x - self.x)

    def dot(self, other):
        return self @ other

    def to_int(self):
        return Vector(*tuple(map(ceil, self)))

    @property
    def magnitude(self):
        return sqrt(pow(self.y, 2) + pow(self.x, 2))

    @magnitude.setter
    def magnitude(self, value):
        new = value * self / self.magnitude
        self.x, self.y = new

    @property
    def x(self):
        return super().__getitem__(0)

    @x.setter
    def x(self, value):
        super().__setitem__(0, value)

    @property
    def y(self):
        return super().__getitem__(1)

    @y.setter
    def y(self, value):
        super().__setitem__(1, value)

    def __str__(self):
        return "<" + ", ".join(map(str, self)) + ">"

    def __repr__(self):
        return f"Vector<" + ", ".join(map(str, self)) + ">"

    def __mul__(self, other) -> "Vector":
        x, y = self
        try:
            j, k = other
            return Vector(x * j, y * k)
        except TypeError:
            return Vector(x * other, y * other)

    def __imul__(self, other):
        try:
            j, k = other
            self.x *= j
            self.y *= k
        except TypeError:
            self.x *= other
            self.y *= other
        return self

    def __rmul__(self, other):
        return self.__mul__(other)

    def __add__(self, other) -> "Vector":
        x, y = self
        try:
            j, k = other
            return Vector(x + j, y + k)
        except TypeError:
            return Vector(x + other, y + other)

    def __iadd__(self, other):
        try:
            j, k = other
            self.x += j
            self.y += k
        except TypeError:
            self.x += other
            self.y += other
        return self

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other) -> "Vector":
        x, y = self
        try:
            j, k = other
            return Vector(x - j, y - k)
        except TypeError:
            return Vector(x - other, y - other)

    def __isub__(self, other):
        try:
            j, k = other
            self.x -= j
            self.y -= k
        except TypeError:
            self.x -= other
            self.y -= other
        return self

    def __rsub__(self, other):
        x, y = self
        try:
            j, k = other
            return Vector(j - x, k - y)
        except TypeError:
            return Vector(other - x, other - y)

    def __truediv__(self, other):
        x, y = self
        try:
            j, k = other
            return Vector(x / j, y / k)
        except TypeError:
            return Vector(x / other, y / other)

    def __itruediv__(self, other):
        try:
            j, k = other
            self.x /= j
            self.y /= k
        except TypeError:
            self.x /= other
            self.y /= other
        return self

    def __rtruediv__(self, other):
        x, y = self
        try:
            j, k = other
            return Vector(j / x, k / y)
        except TypeError:
            return Vector(other / x, other / y)

    def __floordiv__(self, other):
        x, y = self
        try:
            j, k = other
            return Vector(x // j, y // k)
        except TypeError:
            return Vector(x // other, y // other)

    def __ifloordiv__(self, other):
        try:
            j, k = other
            self.x //= j
            self.y //= k
        except TypeError:
            self.x //= other
            self.y //= other
        return self

    def __rfloordiv__(self, other):
        x, y = self
        try:
            j, k = other
            return Vector(j // x, k // y)
        except TypeError:
            return Vector(other // x, other // y)

    def __matmul__(self, other):
        if isinstance(other, Vector):
            return self.x * other.x + self.y * other.y
        else:
            raise TypeError("Cannot take the dot product of a non-vector.")

    def __complex__(self):
        return complex(self.x, self.y)

    def __int__(self):
        """Return the real portion of the vector as an integer."""
        return int(self.x)

    def __float__(self):
        """Return the real portion of the vector as a floating-point number."""
        return float(self.x)
