"""
>>> def tester(test_gen):
...     prev = 0
...     for i, n in enumerate(test_gen()):
...         if abs(n - prev) < 1e-8:
...             return n
...         if i > 100:
...             return 0
...         prev = n
...
>>> res = tester(golden)
>>> abs(res - 1.618033988738303) < 1e-8
True
"""


def golden():
    a, b = 1, 1
    for _ in range(200):
        yield b/a
        a, b = b, a+b


