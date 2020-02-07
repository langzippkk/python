matvec
======

The intent of this problem is to implement linear algebra operations using functional programming with iterators.  
You don't need to do any error-checking with vector or matrix sizes, since that's not the point of this exercise.  


`Vector` class
--------------

Implement a vector with the following methods.  Do **not** use any direct indexing (such as `self.vals[i]`) for any 
method

* `__iter__`: Returns a generator that yields each element
* `__add__`: 
  * If `other` is a scalar, add it to each element.  
  * If `other` is a vector, add the vectors elementwise
  * In both cases, return a new instance of `Vector`
* `__radd__`: 
  * Do the same thing as `__add__`
* `__mul__`: 
  * If `other` is a scalar, add it to each element and return a new `Vector`.  
  * If `other` is a vector, compute a dot product and return a scalar
* `__rmul__`: 
  * Do the same thing as `__mul__`
  
  
`RowMatrix` class
-----------------

Implement a matrix with the following methods.  For `iterrows` and `itercols`,  you may use direct indexing 
(such as `self.vals[i][j]`).  For all other methods, **try to use only `iterrow` and `itercols`, as well as the math 
operations you implemented for `Vector`; avoid direct indexing.**

* `__init__`:  Instantiates a matrix such that each row is an instance of `Vector`
* `__iterrows__`: Returns a generator which yields each row as a new instance of `Vector`
* `__itercols__`: Returns a generator which yields each column as a new instance of `Vector`
* `__iter__`: Does the same thing as `__iterrows__`
* `__add__`: 
  * If `other` is a scalar, add it to each element.  
  * If `other` is vector, treat it as a column vector (`n` rows, 1 col) and add it elementwise to each column of the matrix.
  * If `other` is a matrix, add it elementwise.  
  * In all cases, return a new instance of `RowMatrix`
* `__radd__`:
  * If `other` is a vector, treat it as a row vector (1 row, `n` cols) and add it elementwise.  Return a new `RowMatrix`.
  * If `other` is a scalar or matrix, do the same thing as `__add__`
* `__mul__`:
  * If `other` is a scalar, multiply it by each element and return a new `RowMatrix`
  * If `other` is a vector, treat it as a column vector and do matrix-vector multiplication.  Return a new `Vector`.  
  * If `other` is a matrix, do matrix-matrix multiplication and return a new `RowMatrix`.
* `__rmul__`:
  * If `other` is a vector, treat it as a row vector and do matrix-vector multiplication.  Return a new `Vector`.  
  * If `other` is a scalar or matrix, do the same thing as `__rmul__`
