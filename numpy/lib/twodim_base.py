""" Basic functions for manipulating 2d arrays

"""
from __future__ import division

__all__ = ['diag','diagflat','eye','fliplr','flipud','rot90','tri','triu',
           'tril','vander','histogram2d','mask_indices',
           'tril_indices','tril_indices_from','triu_indices','triu_indices_from',
           ]

from numpy.core.numeric import asanyarray, equal, subtract, arange, \
     zeros, greater_equal, multiply, ones, asarray, alltrue, where, \
     empty, diagonal

def fliplr(m):
    """
    Flip array in the left/right direction.

    Flip the entries in each row in the left/right direction.
    Columns are preserved, but appear in a different order than before.

    Parameters
    ----------
    m : array_like
        Input array.

    Returns
    -------
    f : ndarray
        A view of `m` with the columns reversed.  Since a view
        is returned, this operation is :math:`\\mathcal O(1)`.

    See Also
    --------
    flipud : Flip array in the up/down direction.
    rot90 : Rotate array counterclockwise.

    Notes
    -----
    Equivalent to A[:,::-1]. Does not require the array to be
    two-dimensional.

    Examples
    --------
    >>> A = np.diag([1.,2.,3.])
    >>> A
    array([[ 1.,  0.,  0.],
           [ 0.,  2.,  0.],
           [ 0.,  0.,  3.]])
    >>> np.fliplr(A)
    array([[ 0.,  0.,  1.],
           [ 0.,  2.,  0.],
           [ 3.,  0.,  0.]])

    >>> A = np.random.randn(2,3,5)
    >>> np.all(np.fliplr(A)==A[:,::-1,...])
    True

    """
    m = asanyarray(m)
    if m.ndim < 2:
        raise ValueError("Input must be >= 2-d.")
    return m[:, ::-1]

def flipud(m):
    """
    Flip array in the up/down direction.

    Flip the entries in each column in the up/down direction.
    Rows are preserved, but appear in a different order than before.

    Parameters
    ----------
    m : array_like
        Input array.

    Returns
    -------
    out : array_like
        A view of `m` with the rows reversed.  Since a view is
        returned, this operation is :math:`\\mathcal O(1)`.

    See Also
    --------
    fliplr : Flip array in the left/right direction.
    rot90 : Rotate array counterclockwise.

    Notes
    -----
    Equivalent to ``A[::-1,...]``.
    Does not require the array to be two-dimensional.

    Examples
    --------
    >>> A = np.diag([1.0, 2, 3])
    >>> A
    array([[ 1.,  0.,  0.],
           [ 0.,  2.,  0.],
           [ 0.,  0.,  3.]])
    >>> np.flipud(A)
    array([[ 0.,  0.,  3.],
           [ 0.,  2.,  0.],
           [ 1.,  0.,  0.]])

    >>> A = np.random.randn(2,3,5)
    >>> np.all(np.flipud(A)==A[::-1,...])
    True

    >>> np.flipud([1,2])
    array([2, 1])

    """
    m = asanyarray(m)
    if m.ndim < 1:
        raise ValueError("Input must be >= 1-d.")
    return m[::-1,...]

def rot90(m, k=1):
    """
    Rotate an array by 90 degrees in the counter-clockwise direction.

    The first two dimensions are rotated; therefore, the array must be at
    least 2-D.

    Parameters
    ----------
    m : array_like
        Array of two or more dimensions.
    k : integer
        Number of times the array is rotated by 90 degrees.

    Returns
    -------
    y : ndarray
        Rotated array.

    See Also
    --------
    fliplr : Flip an array horizontally.
    flipud : Flip an array vertically.

    Examples
    --------
    >>> m = np.array([[1,2],[3,4]], int)
    >>> m
    array([[1, 2],
           [3, 4]])
    >>> np.rot90(m)
    array([[2, 4],
           [1, 3]])
    >>> np.rot90(m, 2)
    array([[4, 3],
           [2, 1]])

    """
    m = asanyarray(m)
    if m.ndim < 2:
        raise ValueError("Input must >= 2-d.")
    k = k % 4
    if k == 0:
        return m
    elif k == 1:
        return fliplr(m).swapaxes(0,1)
    elif k == 2:
        return fliplr(flipud(m))
    else:
        # k == 3
        return fliplr(m.swapaxes(0,1))

def eye(N, M=None, k=0, dtype=float):
    """
    Return a 2-D array with ones on the diagonal and zeros elsewhere.

    Parameters
    ----------
    N : int
      Number of rows in the output.
    M : int, optional
      Number of columns in the output. If None, defaults to `N`.
    k : int, optional
      Index of the diagonal: 0 (the default) refers to the main diagonal,
      a positive value refers to an upper diagonal, and a negative value
      to a lower diagonal.
    dtype : data-type, optional
      Data-type of the returned array.

    Returns
    -------
    I : ndarray of shape (N,M)
      An array where all elements are equal to zero, except for the `k`-th
      diagonal, whose values are equal to one.

    See Also
    --------
    identity : (almost) equivalent function
    diag : diagonal 2-D array from a 1-D array specified by the user.

    Examples
    --------
    >>> np.eye(2, dtype=int)
    array([[1, 0],
           [0, 1]])
    >>> np.eye(3, k=1)
    array([[ 0.,  1.,  0.],
           [ 0.,  0.,  1.],
           [ 0.,  0.,  0.]])

    """
    if M is None:
        M = N
    m = zeros((N, M), dtype=dtype)
    if k >= M:
        return m
    if k >= 0:
        i = k
    else:
        i = (-k) * M
    m[:M-k].flat[i::M+1] = 1
    return m

def diag(v, k=0):
    """
    Extract a diagonal or construct a diagonal array.

    See the more detailed documentation for ``numpy.diagonal`` if you use this
    function to extract a diagonal and wish to write to the resulting array;
    whether it returns a copy or a view depends on what version of numpy you
    are using.

    Parameters
    ----------
    v : array_like
        If `v` is a 2-D array, return a copy of its `k`-th diagonal.
        If `v` is a 1-D array, return a 2-D array with `v` on the `k`-th
        diagonal.
    k : int, optional
        Diagonal in question. The default is 0. Use `k>0` for diagonals
        above the main diagonal, and `k<0` for diagonals below the main
        diagonal.

    Returns
    -------
    out : ndarray
        The extracted diagonal or constructed diagonal array.

    See Also
    --------
    diagonal : Return specified diagonals.
    diagflat : Create a 2-D array with the flattened input as a diagonal.
    trace : Sum along diagonals.
    triu : Upper triangle of an array.
    tril : Lower triange of an array.

    Examples
    --------
    >>> x = np.arange(9).reshape((3,3))
    >>> x
    array([[0, 1, 2],
           [3, 4, 5],
           [6, 7, 8]])

    >>> np.diag(x)
    array([0, 4, 8])
    >>> np.diag(x, k=1)
    array([1, 5])
    >>> np.diag(x, k=-1)
    array([3, 7])

    >>> np.diag(np.diag(x))
    array([[0, 0, 0],
           [0, 4, 0],
           [0, 0, 8]])

    """
    v = asarray(v)
    s = v.shape
    if len(s) == 1:
        n = s[0]+abs(k)
        res = zeros((n,n), v.dtype)
        if k >= 0:
            i = k
        else:
            i = (-k) * n
        res[:n-k].flat[i::n+1] = v
        return res
    elif len(s) == 2:
        return v.diagonal(k)
    else:
        raise ValueError("Input must be 1- or 2-d.")

def diagflat(v, k=0):
    """
    Create a two-dimensional array with the flattened input as a diagonal.

    Parameters
    ----------
    v : array_like
        Input data, which is flattened and set as the `k`-th
        diagonal of the output.
    k : int, optional
        Diagonal to set; 0, the default, corresponds to the "main" diagonal,
        a positive (negative) `k` giving the number of the diagonal above
        (below) the main.

    Returns
    -------
    out : ndarray
        The 2-D output array.

    See Also
    --------
    diag : MATLAB work-alike for 1-D and 2-D arrays.
    diagonal : Return specified diagonals.
    trace : Sum along diagonals.

    Examples
    --------
    >>> np.diagflat([[1,2], [3,4]])
    array([[1, 0, 0, 0],
           [0, 2, 0, 0],
           [0, 0, 3, 0],
           [0, 0, 0, 4]])

    >>> np.diagflat([1,2], 1)
    array([[0, 1, 0],
           [0, 0, 2],
           [0, 0, 0]])

    """
    try:
        wrap = v.__array_wrap__
    except AttributeError:
        wrap = None
    v = asarray(v).ravel()
    s = len(v)
    n = s + abs(k)
    res = zeros((n,n), v.dtype)
    if (k >= 0):
        i = arange(0,n-k)
        fi = i+k+i*n
    else:
        i = arange(0,n+k)
        fi = i+(i-k)*n
    res.flat[fi] = v
    if not wrap:
        return res
    return wrap(res)

def tri(N, M=None, k=0, dtype=float):
    """
    An array with ones at and below the given diagonal and zeros elsewhere.

    Parameters
    ----------
    N : int
        Number of rows in the array.
    M : int, optional
        Number of columns in the array.
        By default, `M` is taken equal to `N`.
    k : int, optional
        The sub-diagonal at and below which the array is filled.
        `k` = 0 is the main diagonal, while `k` < 0 is below it,
        and `k` > 0 is above.  The default is 0.
    dtype : dtype, optional
        Data type of the returned array.  The default is float.

    Returns
    -------
    tri : ndarray of shape (N, M)
        Array with its lower triangle filled with ones and zero elsewhere;
        in other words ``T[i,j] == 1`` for ``i <= j + k``, 0 otherwise.

    Examples
    --------
    >>> np.tri(3, 5, 2, dtype=int)
    array([[1, 1, 1, 0, 0],
           [1, 1, 1, 1, 0],
           [1, 1, 1, 1, 1]])

    >>> np.tri(3, 5, -1)
    array([[ 0.,  0.,  0.,  0.,  0.],
           [ 1.,  0.,  0.,  0.,  0.],
           [ 1.,  1.,  0.,  0.,  0.]])

    """
    if M is None:
        M = N
    m = greater_equal(subtract.outer(arange(N), arange(M)),-k)
    return m.astype(dtype)

def tril(m, k=0):
    """
    Lower triangle of an array.

    Return a copy of an array with elements above the `k`-th diagonal zeroed.

    Parameters
    ----------
    m : array_like, shape (M, N)
        Input array.
    k : int, optional
        Diagonal above which to zero elements.  `k = 0` (the default) is the
        main diagonal, `k < 0` is below it and `k > 0` is above.

    Returns
    -------
    tril : ndarray, shape (M, N)
        Lower triangle of `m`, of same shape and data-type as `m`.

    See Also
    --------
    triu : same thing, only for the upper triangle

    Examples
    --------
    >>> np.tril([[1,2,3],[4,5,6],[7,8,9],[10,11,12]], -1)
    array([[ 0,  0,  0],
           [ 4,  0,  0],
           [ 7,  8,  0],
           [10, 11, 12]])

    """
    m = asanyarray(m)
    out = multiply(tri(m.shape[0], m.shape[1], k=k, dtype=m.dtype),m)
    return out

def triu(m, k=0):
    """
    Upper triangle of an array.

    Return a copy of a matrix with the elements below the `k`-th diagonal
    zeroed.

    Please refer to the documentation for `tril` for further details.

    See Also
    --------
    tril : lower triangle of an array

    Examples
    --------
    >>> np.triu([[1,2,3],[4,5,6],[7,8,9],[10,11,12]], -1)
    array([[ 1,  2,  3],
           [ 4,  5,  6],
           [ 0,  8,  9],
           [ 0,  0, 12]])

    """
    m = asanyarray(m)
    out = multiply((1 - tri(m.shape[0], m.shape[1], k - 1, dtype=m.dtype)), m)
    return out

# borrowed from John Hunter and matplotlib
def vander(x, N=None):
    """
    Generate a Van der Monde matrix.

    The columns of the output matrix are decreasing powers of the input
    vector.  Specifically, the `i`-th output column is the input vector
    raised element-wise to the power of ``N - i - 1``.  Such a matrix with
    a geometric progression in each row is named for Alexandre-Theophile
    Vandermonde.

    Parameters
    ----------
    x : array_like
        1-D input array.
    N : int, optional
        Order of (number of columns in) the output.  If `N` is not specified,
        a square array is returned (``N = len(x)``).

    Returns
    -------
    out : ndarray
        Van der Monde matrix of order `N`.  The first column is ``x^(N-1)``,
        the second ``x^(N-2)`` and so forth.

    Examples
    --------
    >>> x = np.array([1, 2, 3, 5])
    >>> N = 3
    >>> np.vander(x, N)
    array([[ 1,  1,  1],
           [ 4,  2,  1],
           [ 9,  3,  1],
           [25,  5,  1]])

    >>> np.column_stack([x**(N-1-i) for i in range(N)])
    array([[ 1,  1,  1],
           [ 4,  2,  1],
           [ 9,  3,  1],
           [25,  5,  1]])

    >>> x = np.array([1, 2, 3, 5])
    >>> np.vander(x)
    array([[  1,   1,   1,   1],
           [  8,   4,   2,   1],
           [ 27,   9,   3,   1],
           [125,  25,   5,   1]])

    The determinant of a square Vandermonde matrix is the product
    of the differences between the values of the input vector:

    >>> np.linalg.det(np.vander(x))
    48.000000000000043
    >>> (5-3)*(5-2)*(5-1)*(3-2)*(3-1)*(2-1)
    48

    """
    x = asarray(x)
    if N is None:
        N=len(x)
    X = ones( (len(x),N), x.dtype)
    for i in range(N - 1):
        X[:,i] = x**(N - i - 1)
    return X


def histogram2d(x, y, bins=10, range=None, normed=False, weights=None):
    """
    Compute the bi-dimensional histogram of two data samples.

    Parameters
    ----------
    x : array_like, shape (N,)
        An array containing the x coordinates of the points to be histogrammed.
    y : array_like, shape (N,)
        An array containing the y coordinates of the points to be histogrammed.
    bins : int or [int, int] or array_like or [array, array], optional
        The bin specification:

          * If int, the number of bins for the two dimensions (nx=ny=bins).
          * If [int, int], the number of bins in each dimension (nx, ny = bins).
          * If array_like, the bin edges for the two dimensions
            (x_edges=y_edges=bins).
          * If [array, array], the bin edges in each dimension
            (x_edges, y_edges = bins).

    range : array_like, shape(2,2), optional
        The leftmost and rightmost edges of the bins along each dimension
        (if not specified explicitly in the `bins` parameters):
        ``[[xmin, xmax], [ymin, ymax]]``. All values outside of this range
        will be considered outliers and not tallied in the histogram.
    normed : bool, optional
        If False, returns the number of samples in each bin. If True, returns
        the bin density, i.e. the bin count divided by the bin area.
    weights : array_like, shape(N,), optional
        An array of values ``w_i`` weighing each sample ``(x_i, y_i)``. Weights
        are normalized to 1 if `normed` is True. If `normed` is False, the
        values of the returned histogram are equal to the sum of the weights
        belonging to the samples falling into each bin.

    Returns
    -------
    H : ndarray, shape(nx, ny)
        The bi-dimensional histogram of samples `x` and `y`. Values in `x`
        are histogrammed along the first dimension and values in `y` are
        histogrammed along the second dimension.
    xedges : ndarray, shape(nx,)
        The bin edges along the first dimension.
    yedges : ndarray, shape(ny,)
        The bin edges along the second dimension.

    See Also
    --------
    histogram : 1D histogram
    histogramdd : Multidimensional histogram

    Notes
    -----
    When `normed` is True, then the returned histogram is the sample density,
    defined such that:

    .. math::
      \\sum_{i=0}^{nx-1} \\sum_{j=0}^{ny-1} H_{i,j} \\Delta x_i \\Delta y_j = 1

    where `H` is the histogram array and :math:`\\Delta x_i \\Delta y_i`
    the area of bin ``{i,j}``.

    Please note that the histogram does not follow the Cartesian convention
    where `x` values are on the abcissa and `y` values on the ordinate axis.
    Rather, `x` is histogrammed along the first dimension of the array
    (vertical), and `y` along the second dimension of the array (horizontal).
    This ensures compatibility with `histogramdd`.

    Examples
    --------
    >>> x, y = np.random.randn(2, 100)
    >>> H, xedges, yedges = np.histogram2d(x, y, bins=(5, 8))
    >>> H.shape, xedges.shape, yedges.shape
    ((5, 8), (6,), (9,))

    We can now use the Matplotlib to visualize this 2-dimensional histogram:

    >>> extent = [yedges[0], yedges[-1], xedges[-1], xedges[0]]
    >>> import matplotlib.pyplot as plt
    >>> plt.imshow(H, extent=extent, interpolation='nearest')
    <matplotlib.image.AxesImage object at ...>
    >>> plt.colorbar()
    <matplotlib.colorbar.Colorbar instance at ...>
    >>> plt.show()

    """
    from numpy import histogramdd

    try:
        N = len(bins)
    except TypeError:
        N = 1

    if N != 1 and N != 2:
        xedges = yedges = asarray(bins, float)
        bins = [xedges, yedges]
    hist, edges = histogramdd([x,y], bins, range, normed, weights)
    return hist, edges[0], edges[1]


def mask_indices(n, mask_func, k=0):
    """
    Return the indices to access (n, n) arrays, given a masking function.

    Assume `mask_func` is a function that, for a square array a of size
    ``(n, n)`` with a possible offset argument `k`, when called as
    ``mask_func(a, k)`` returns a new array with zeros in certain locations
    (functions like `triu` or `tril` do precisely this). Then this function
    returns the indices where the non-zero values would be located.

    Parameters
    ----------
    n : int
        The returned indices will be valid to access arrays of shape (n, n).
    mask_func : callable
        A function whose call signature is similar to that of `triu`, `tril`.
        That is, ``mask_func(x, k)`` returns a boolean array, shaped like `x`.
        `k` is an optional argument to the function.
    k : scalar
        An optional argument which is passed through to `mask_func`. Functions
        like `triu`, `tril` take a second argument that is interpreted as an
        offset.

    Returns
    -------
    indices : tuple of arrays.
        The `n` arrays of indices corresponding to the locations where
        ``mask_func(np.ones((n, n)), k)`` is True.

    See Also
    --------
    triu, tril, triu_indices, tril_indices

    Notes
    -----
    .. versionadded:: 1.4.0

    Examples
    --------
    These are the indices that would allow you to access the upper triangular
    part of any 3x3 array:

    >>> iu = np.mask_indices(3, np.triu)

    For example, if `a` is a 3x3 array:

    >>> a = np.arange(9).reshape(3, 3)
    >>> a
    array([[0, 1, 2],
           [3, 4, 5],
           [6, 7, 8]])
    >>> a[iu]
    array([0, 1, 2, 4, 5, 8])

    An offset can be passed also to the masking function.  This gets us the
    indices starting on the first diagonal right of the main one:

    >>> iu1 = np.mask_indices(3, np.triu, 1)

    with which we now extract only three elements:

    >>> a[iu1]
    array([1, 2, 5])

    """
    m = ones((n,n), int)
    a = mask_func(m, k)
    return where(a != 0)


def tril_indices(n, k=0):
    """
    Return the indices for the lower-triangle of an (n, n) array.

    Parameters
    ----------
    n : int
        The row dimension of the square arrays for which the returned
        indices will be valid.
    k : int, optional
        Diagonal offset (see `tril` for details).

    Returns
    -------
    inds : tuple of arrays
        The indices for the triangle. The returned tuple contains two arrays,
        each with the indices along one dimension of the array.

    See also
    --------
    triu_indices : similar function, for upper-triangular.
    mask_indices : generic function accepting an arbitrary mask function.
    tril, triu

    Notes
    -----
    .. versionadded:: 1.4.0

    Examples
    --------
    Compute two different sets of indices to access 4x4 arrays, one for the
    lower triangular part starting at the main diagonal, and one starting two
    diagonals further right:

    >>> il1 = np.tril_indices(4)
    >>> il2 = np.tril_indices(4, 2)

    Here is how they can be used with a sample array:

    >>> a = np.arange(16).reshape(4, 4)
    >>> a
    array([[ 0,  1,  2,  3],
           [ 4,  5,  6,  7],
           [ 8,  9, 10, 11],
           [12, 13, 14, 15]])

    Both for indexing:

    >>> a[il1]
    array([ 0,  4,  5,  8,  9, 10, 12, 13, 14, 15])

    And for assigning values:

    >>> a[il1] = -1
    >>> a
    array([[-1,  1,  2,  3],
           [-1, -1,  6,  7],
           [-1, -1, -1, 11],
           [-1, -1, -1, -1]])

    These cover almost the whole array (two diagonals right of the main one):

    >>> a[il2] = -10
    >>> a
    array([[-10, -10, -10,   3],
           [-10, -10, -10, -10],
           [-10, -10, -10, -10],
           [-10, -10, -10, -10]])

    """
    return mask_indices(n, tril, k)


def tril_indices_from(arr, k=0):
    """
    Return the indices for the lower-triangle of arr.

    See `tril_indices` for full details.

    Parameters
    ----------
    arr : array_like
        The indices will be valid for square arrays whose dimensions are
        the same as arr.
    k : int, optional
        Diagonal offset (see `tril` for details).

    See Also
    --------
    tril_indices, tril

    Notes
    -----
    .. versionadded:: 1.4.0

    """
    if not (arr.ndim == 2 and arr.shape[0] == arr.shape[1]):
        raise ValueError("input array must be 2-d and square")
    return tril_indices(arr.shape[0], k)


def triu_indices(n, k=0):
    """
    Return the indices for the upper-triangle of an (n, n) array.

    Parameters
    ----------
    n : int
        The size of the arrays for which the returned indices will
        be valid.
    k : int, optional
        Diagonal offset (see `triu` for details).

    Returns
    -------
    inds : tuple, shape(2) of ndarrays, shape(`n`)
        The indices for the triangle. The returned tuple contains two arrays,
        each with the indices along one dimension of the array.  Can be used
        to slice a ndarray of shape(`n`, `n`).

    See also
    --------
    tril_indices : similar function, for lower-triangular.
    mask_indices : generic function accepting an arbitrary mask function.
    triu, tril

    Notes
    -----
    .. versionadded:: 1.4.0

    Examples
    --------
    Compute two different sets of indices to access 4x4 arrays, one for the
    upper triangular part starting at the main diagonal, and one starting two
    diagonals further right:

    >>> iu1 = np.triu_indices(4)
    >>> iu2 = np.triu_indices(4, 2)

    Here is how they can be used with a sample array:

    >>> a = np.arange(16).reshape(4, 4)
    >>> a
    array([[ 0,  1,  2,  3],
           [ 4,  5,  6,  7],
           [ 8,  9, 10, 11],
           [12, 13, 14, 15]])

    Both for indexing:

    >>> a[iu1]
    array([ 0,  1,  2,  3,  5,  6,  7, 10, 11, 15])

    And for assigning values:

    >>> a[iu1] = -1
    >>> a
    array([[-1, -1, -1, -1],
           [ 4, -1, -1, -1],
           [ 8,  9, -1, -1],
           [12, 13, 14, -1]])

    These cover only a small part of the whole array (two diagonals right
    of the main one):

    >>> a[iu2] = -10
    >>> a
    array([[ -1,  -1, -10, -10],
           [  4,  -1,  -1, -10],
           [  8,   9,  -1,  -1],
           [ 12,  13,  14,  -1]])

    """
    return mask_indices(n, triu, k)


def triu_indices_from(arr, k=0):
    """
    Return the indices for the upper-triangle of a (N, N) array.

    See `triu_indices` for full details.

    Parameters
    ----------
    arr : ndarray, shape(N, N)
        The indices will be valid for square arrays.
    k : int, optional
        Diagonal offset (see `triu` for details).

    Returns
    -------
    triu_indices_from : tuple, shape(2) of ndarray, shape(N)
        Indices for the upper-triangle of `arr`.

    See Also
    --------
    triu_indices, triu

    Notes
    -----
    .. versionadded:: 1.4.0

    """
    if not (arr.ndim == 2 and arr.shape[0] == arr.shape[1]):
        raise ValueError("input array must be 2-d and square")
    return triu_indices(arr.shape[0],k)
