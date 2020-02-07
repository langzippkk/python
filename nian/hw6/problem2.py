"""
>>> a = Array(['1', '2', '3'], int)
>>> a
[1, 2, 3]
>>> a.dtype
<class 'int'>
>>> a.dtype = str
>>> a
['1', '2', '3']
>>> a.dtype
<class 'str'>
>>> a.data = [4, 5, 6] # doctest: +IGNORE_EXCEPTION_DETAIL
Traceback (most recent call last):
AttributeError:
>>> b = Array(['foo', 'bar'], int)  # doctest: +IGNORE_EXCEPTION_DETAIL
Traceback (most recent call last):
ValueError:
>>> b = Array(['1', '2', '3'], int())  # doctest: +IGNORE_EXCEPTION_DETAIL
Traceback (most recent call last):
TypeError:

"""

from collections import Callable


class Array:

    def __init__(self,data,dtype):
        self._data = data
        self.dtype = dtype

    def __repr__(self):
       return repr(self._data)

    @property
    def data(self):
        result = self._data.copy()
        return result

    @property
    def dtype(self):
        return self._dtype

    @dtype.setter 
    def dtype(self,dtype):
        if not isinstance(dtype,Callable):
            raise TypeError("Not Callable")
        else:
            self._dtype = dtype
            self._data = [self.dtype(x) for x in self._data]

        ## setter method.

