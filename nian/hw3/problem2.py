"""
>>> from math import sqrt
>>> multi_sqrt = vectorize(sqrt)
>>> multi_sqrt(4.0, 25.0, 1.0)
[2.0, 5.0, 1.0]

>>> multi_upper = vectorize(str.upper)
>>> multi_upper('foo', 'BAR', 'Baz')
['FOO', 'BAR', 'BAZ']
"""


def vectorize(func):
    series = []
    def vec(*list1):
        for ele in list1:
            series.append(func(ele))
        return series
    return vec
