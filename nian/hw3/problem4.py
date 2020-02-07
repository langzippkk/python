"""

Tests if a function with 1 arg works

>>> cached_upper = lru_cache(str.upper, maxsize=32)
>>> inputs = ['a', 'b', 'c', 'd', 'a', 'e', 'd', 'f', 'g', 'd', 'h']
>>> [cached_upper(x) for x in inputs]
['A', 'B', 'C', 'D', 'A', 'E', 'D', 'F', 'G', 'D', 'H']
>>> cached_upper.cache_info()
CacheInfo(hits=3, misses=8, maxsize=32, currsize=8)

Tests if a function with 2 args works

>>> import operator
>>> cached_add = lru_cache(operator.add, maxsize=32)
>>> inputs = [1, 2, 3, 4, 2, 2, 5, 6, 4, 1]
>>> [cached_add(x, 1) for x in inputs]
[2, 3, 4, 5, 3, 3, 6, 7, 5, 2]
>>> cached_add.cache_info()
CacheInfo(hits=4, misses=6, maxsize=32, currsize=6)

Tests if LRU behavior works

>>> cached_mul = lru_cache(operator.mul, maxsize=4)
>>> inputs = [1, 2, 3, 4, 2, 2, 5, 6, 4, 1, 2, 1, 5]
>>> [cached_mul(x, 2) for x in inputs]
[2, 4, 6, 8, 4, 4, 10, 12, 8, 2, 4, 2, 10]
>>> cached_mul.cache_info()
CacheInfo(hits=4, misses=9, maxsize=4, currsize=4)
"""


from collections import namedtuple
from collections import OrderedDict


cache_info = namedtuple('CacheInfo', ['hits', 'misses', 'maxsize', 'currsize'])
def lru_cache(func, maxsize=128):
    hit_counts = cache_info(0, 0, maxsize, 0)
    cache = OrderedDict()
    
    def LRU(*args):
    ## if the argument has occured, increase hit by 1, put/update this information to the end of 
    ## orderedDict
        nonlocal hit_counts
        nonlocal cache
        
    # Problem without nonlocal: This is because, even though Var1 exists, you're also using an assignment statement 
    # on the name Var1 inside of the function Naturally, this creates a variable inside the function's scope called Var1
    # The Python interpreter sees this at module load time and decides (correctly so) 
    # that the global scope's Var1 should not be used inside the local scope, which leads to a problem when you try to reference the variable before it is locally assigned.
        if args in cache:
            hit_counts = cache_info(hit_counts.hits+1, hit_counts.misses, hit_counts.maxsize, hit_counts.currsize)
            cache.move_to_end(args)
            return (cache[args])     ## use existed cache instead of call the function again
    ## otherwise, we missed this information and we need to add this into cache.
        else:
            hit_counts = cache_info(hit_counts.hits, hit_counts.misses+1, hit_counts.maxsize, hit_counts.currsize)
            ## if currsize is bigger than maxsize, we need to remove the oldest one,and 
            ## add newest one to the end.
            if hit_counts.currsize >= hit_counts.maxsize:
                cache.popitem(last = False)
                cache[args] = func(*args)   ## automatically insert on the last position
                return (func(*args))
            else:
            ## currsize is less than maxsize,add it directly.
                cache[args] = func(*args)
                hit_counts = cache_info(hit_counts.hits, hit_counts.misses, hit_counts.maxsize, hit_counts.currsize+1)
                return (func(*args))
    def accessor():
        return hit_counts
    LRU.cache_info = accessor

    return LRU


if __name__ == '__main__':

    # Example usage.  Feel free to change this.  It won't be graded.

    import urllib.request, urllib.error


    def get_pep(num):
        resource = 'http://www.python.org/dev/peps/pep-%04d/' % num
        try:
            with urllib.request.urlopen(resource) as s:
                return s.read()
        except urllib.error.HTTPError:
            return 'Not Found'

    get_pep = lru_cache(get_pep, maxsize=32)

    for n in 8, 290, 308, 320, 8, 218, 320, 279, 289, 320, 9991:
        pep = get_pep(n)
        print(n, len(pep))
    print(get_pep.cache_info())
