from practice.matvec.vector import Vector
from numbers import Real
import numpy as np

class RowMatrix:

    def __init__(self, vals):
        self.vals = tuple(Vector(row) for row in vals)

    def iterrows(self):
        return (row for row in self.vals)

    def itercols(self):
        return (Vector(row[i] for row in self) for i in range(len(self.vals[0])))

    def __iter__(self):
        return self.iterrows()

    def __repr__(self):
        res = "Matrix(\n"
        for row in self:
            res += "  {},\n".format(row)
        res = res.rstrip()
        res = res.rstrip(',')
        res += ')'
        return res

    def __add__(self, other):
        if isinstance(other, Real):
            return RowMatrix(row + other for row in self)
        elif isinstance(other, RowMatrix) or isinstance(other, Vector):
            return RowMatrix(r1 + r2 for r1, r2 in zip(self, other))
        else:
            return NotImplemented

    def __radd__(self, other):
        if isinstance(other, Real) or isinstance(other, Vector):
            return RowMatrix(row + other for row in self)
        # elif isinstance(other, RowMatrix):
            # This is redundant.  If the other is a RowMatrix, then other.__add__ will dispatched before attempting this
        else:
            return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Real):
            return RowMatrix(row * other for row in self)
        elif isinstance(other, Vector):
            return Vector(row * other for row in self)
        elif isinstance(other, RowMatrix):
            return RowMatrix([row * col for col in other.itercols()] for row in self)
        else:
            return NotImplemented

    def __rmul__(self, other):
        if isinstance(other, Real):
            return self * other
        elif isinstance(other, Vector):
            return Vector(col * other for col in self.itercols())
        # elif isinstance(other, RowMatrix):
            # This is redundant.  If the other is a RowMatrix, then other.__mul__ will dispatched before attempting this
        else:
            return NotImplemented



if __name__ == '__main__':
    m1 = RowMatrix([[1, 2, 3],
                    [4, 5, 6],
                    [7, 8, 9]])
    n1 = np.array([[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9]])

    m2 = RowMatrix([[10, 11, 12],
                    [13, 14, 15],
                    [16, 17, 18]])
    n2 = np.array(([10, 11, 12],
                   [13, 14, 15],
                   [16, 17, 18]))

    v1 = Vector([-10, 11, -12])
    w1 = np.array([-10, 11, -12])

    print("\nTest matrix-vector mul")
    print("======================")
    print(m1 * v1)
    print(n1 @ w1.reshape((-1,1)))
    print(v1 * m1)
    print(w1 @ n1)


    print("\nTest matrix-matrix mul")
    print("======================")
    print(m1 * m2)
    print(n1 @ n2)

    print(m2 * m1)
    print(n2 @ n1)




