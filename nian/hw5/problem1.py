"""
Test ZeroDivisionError
>>> Fraction(1, 0)
Traceback (most recent call last):
ZeroDivisionError

Test negation
>>> -Fraction(1, 5)
Fraction(-1, 5)
>>> -Fraction(-1, 5)
Fraction(1, 5)

Test Addition
>>> Fraction(37, 150) + Fraction(13, 150)
Fraction(1, 3)
>>> Fraction(13, 150) + Fraction(37, 150)
Fraction(1, 3)
>>> Fraction(1, 3) + 2
Fraction(7, 3)
>>> 2 + Fraction(1, 3)
Fraction(7, 3)

# Test subtraction
>>> Fraction(3, 8) - Fraction(1, 4)
Fraction(1, 8)
>>> Fraction(1, 4) - Fraction(3, 8)
Fraction(-1, 8)
>>> Fraction(3,8) - 2
Fraction(-13, 8)
>>> 2 - Fraction(3,8)
Fraction(13, 8)

# Test multiplication
>>> Fraction(2, 3) * Fraction(3, 4)
Fraction(1, 2)
>>> Fraction(3, 4) * Fraction(2, 3)
Fraction(1, 2)
>>> Fraction(3, 8) * 2
Fraction(3, 4)
>>> 2 * Fraction(3, 8)
Fraction(3, 4)

# Test division
>>> Fraction(3, 4) / Fraction(3, 2)
Fraction(1, 2)
>>> Fraction(3, 2) / Fraction(3, 4)
Fraction(2, 1)
>>> 3 / Fraction(4, 6)
Fraction(9, 2)
>>> Fraction(4, 6) / 3
Fraction(2, 9)
"""

import math

class Fraction:
    def __init__(self, numerator, denominator):
        ## numerator and denominator should all divide by a gcd
        self.numerator = numerator // math.gcd(numerator, denominator)
        self.denominator = denominator // math.gcd(numerator, denominator)
        if denominator == 0:
            raise ZeroDivisionError


    def __neg__(self):
        return Fraction((-1)*self.numerator, self.denominator)

    def __add__(self, other):
        ## if add a int, convert to instance
        if isinstance(other, int):
            other = Fraction(other, 1)
        elif not isinstance(other, Fraction):
            return NotImplemented
        ## adding to fraction: using the formula
        return Fraction(self.numerator*other.denominator+other.numerator*self.denominator, self.denominator*other.denominator)


    def __radd__(self, other):
    ## self =y, return y+x
        return self+other


    def __sub__(self, other):
        if isinstance(other, int):
            other = Fraction(other, 1)
        elif not isinstance(other, Fraction):
            return NotImplemented
        return Fraction(self.numerator*other.denominator-other.numerator*self.denominator, self.denominator*other.denominator)

    def __rsub__(self, other):
        return -(self - other)

    def __mul__(self, other):
        if isinstance(other, int):
            other = Fraction(other, 1)
        elif not isinstance(other, Fraction):
            return NotImplemented
        return Fraction(other.numerator*self.numerator, other.denominator*self.denominator)

    def __rmul__(self, other):
        return self*other


    def __truediv__(self, other):
        if isinstance(other, int):
            other = Fraction(other, 1)
        elif not isinstance(other, Fraction):
            return NotImplemented
        return Fraction(self.numerator*other.denominator, self.denominator*other.numerator)


    def __rtruediv__(self, other):
        ## other is int, then transform to int/1 * deno/numerator
        return Fraction(other,1)*Fraction(self.denominator,self.numerator)

    def __repr__(self):
        return f'Fraction({self.numerator}, {self.denominator})'
