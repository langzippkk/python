import math
import random
import numpy as np
import timeit


def mc_vanilla(tot):
    tin = 0
#  use only built-ins and the standard library random and math modules.
    for i in range(0,tot):

        x = random.random()**2
        y = random.random()**2

        if (x+y)<1.0:
            tin = tin +1
    return 4*(float(tin)/tot)

def mc_numpy(tot):
#  use NumPy vector operation
    x = np.random.rand(1,tot)**2
    y = np.random.rand(1,tot)**2
    sum1 = x+y
    result = 4*np.sum(sum1<1)/tot
    return result


if __name__ == '__main__':
    print(mc_vanilla(10000000))
    print(min(timeit.repeat(stmt='mc_vanilla(10000000)', number=1, repeat=3, globals=globals())))
    print(mc_numpy(10000000))
    print(min(timeit.repeat(stmt='mc_numpy(10000000)', number=1, repeat=3, globals=globals())))
