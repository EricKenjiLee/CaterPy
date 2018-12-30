import pandas as pd
from matplotlib import pyplot as plt
from sklearn.preprocessing import StandardScaler
import numpy as np
import scipy as sp
import warnings

from pyspec.helpers import Hankelize

"""
It might be tempting to think of SSA as merely a procedure for smoothing via moving averages but in fact
the key to this technique is the generation of Hankel matrices that are able to decompose, in an
unsupervised manner, the original time series as the weighted sum of several other time series's. In 
this way, we can examine the contribution of each component individually.
"""

class TimeSeries(object):
    def __init__(self, data, standardization=StandardScaler):
        """

        :param data:
        :param standardization:
        """
        self.data = np.array(data)
        self.N = self.data.shape[1]

        if standardization:
            self.std_data = standardization(self.data)

    def __len__(self):
        """This method returns the number of time points.

        :return:
        """
        return self.N

    def shape(self):
        """

        :return:
        """
        return self.data.shape

    def show(self):
        """

        :return:
        """
        plt.imshow(self.std_data)

class SSA(object):
    #TODO: Add a summary plotting function that displays the data, elementary matrices, Hankel matrices, eigentriple magnitudes, and reconstructions
    def __init__(self, TimeSeries, L):
        """

        :param TimeSeries:
        :param L: The window size chosen between 2 and N-1 inclusive.
        """
        self.F = TimeSeries
        self.L = L
        self.K = len(self.F) - L + 1

    @staticmethod
    def _embedding(F,L,K):
        X = np.column_stack([F[i:i+L] for i in range(0,K)])
        HX = Hankelize(X)
        return HX

    @staticmethod
    def _SVD(X):
        d = np.linalg.matrix_rank(X)
        U, S, V = np.linalg.svd(X)
        V = V.T #np.linalg.svd actually returns the transpose of V

        X_elem = np.array( [S[i] * np.outer(U[:,i], V[:,i]) for i in range(0,d)] )

    @staticmethod
    def _grouping(X):
        """
        This method currently does not support grouping of trajectory matrices into trend, periodic, and aperiodic
        regimes.
        :param HX:
        :return:
        """
        warnings.warn('Grouping operations currenlty unsupported; returning argument',UserWarning)

        return X

    @staticmethod
    def _diagonal_averaging(X):
        """

        :param X:
        :return:
        """
        X_rev = X[::-1]
        X_avg = np.array([X_rev.diagonal(i).mean() for i in range(-X.shape[0]+1, X.shape[1])])

        return X_avg

    def process(self):
        X = self._embedding(self.F,self.L,self.K)






