from numbers import Real
import reprlib

class Vector:

    def __init__(self, vals):
        self.vals = tuple(vals)

    def __repr__(self):
        return "Vector{}".format(reprlib.repr(self.vals))

    def __iter__(self):
        return (x for x in self.vals)

    def __len__(self):
        return len(self.vals)

    def __getitem__(self, item):
        return self.vals[item]

    def __neg__(self):
        return Vector(-x for x in self)

    def __add__(self, other):
        if isinstance(other, Real):
            return Vector(x + other for x in self)
        elif isinstance(other, Vector):
            return Vector(x + y for x, y in zip(self, other))
        else:
            return NotImplemented

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return other + (-self)

    def __mul__(self, other):
        if isinstance(other, Real):
            return Vector(x * other for x in self)
        elif isinstance(other, Vector):
            return sum(x * y for x, y in zip(self, other))
        else:
            return NotImplemented

    def __rmul__(self, other):
        return self * other

if __name__ == '__main__':
    v1 = Vector([-5, 6, -7, 8])
    v2 = Vector([1, 2, 3, 4])

    print("v1:      ", v1)

    print("-v1:     ", -v1)

    print("10 + v1: ", 10 + v1)
    print("v1 + 10: ", v1 + 10)

    print("10 - v1: ", 10 - v1)
    print("v1 - 10: ", v1 - 10)

    print("v1 * 10: ", v1 * 10)
    print("10 * v1: ", 10 * v1)

    print("v1 * v2: ", v1 * v2)
    print("v2 * v1: ", v2 * v1)
