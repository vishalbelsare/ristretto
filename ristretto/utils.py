"""
Utility Functions.
"""
# Authors: N. Benjamin Erichson
#          Joseph Knox
# License: GNU General Public License v3.0
from functools import partial
import numbers

import numpy as np
import scipy.sparse as sp


def check_non_negative(X, whom):
    """Check if there is any negative value in an array.
    Parameters
    ----------
    X : array-like or sparse matrix
    Input data.
    whom : string
    Who passed X to this function.
    """
    X = X.data if sp.issparse(X) else X
    if (X < 0).any():
        raise ValueError("Negative values in data passed to %s" % whom)


def check_random_state(seed):
    """Turn seed into a np.random.RandomState instance
    Parameters
    ----------
    seed : None | int | instance of RandomState
    If seed is None, return the RandomState singleton used by np.random.
    If seed is an int, return a new RandomState instance seeded with seed.
    If seed is already a RandomState instance, return it.
    Otherwise raise ValueError.
    """
    if seed is None or seed is np.random:
        return np.random.mtrand._rand
    if isinstance(seed, (numbers.Integral, np.integer)):
        return np.random.RandomState(seed)
    if isinstance(seed, np.random.RandomState):
        return seed
    raise ValueError('%r cannot be used to seed a numpy.random.RandomState'
    ' instance' % seed)


def conjugate_transpose(A):
    """Performs conjugate transpose of A"""
    if A.dtype == np.complexfloating:
        return A.conj().T
    return A.T


def nmf_data(m, n, k, factor_type='normal', noise_type='normal', noiselevel=0):
    _factor_types = ('normal', 'unif')

    if factor_type not in _factor_types:
        raise ValueError('factor_type must be one of %s, not %s'
                         % (' '.join(_factor_types), factor_type))

    if noise_type != 'normal':
        raise ValueError('noise type must be "normal", not %s' % noise_type)

    if factor_type == 'normal':
        #Normal
        Wtue = np.maximum(0, np.random.standard_normal((m, k)))
        Htrue = np.maximum(0, np.random.standard_normal((k, n)))
    else:
        #Unif
        Wtue = np.random.rand(m, k)
        Htrue =  np.random.rand(k, n)

    A = Anoisy = Wtue.dot(Htrue)

    # noise
    Anoisy += noiselevel * np.maximum(0, np.random.standard_normal((m,n)))

    return A, Anoisy
