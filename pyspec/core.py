import pandas as pd
from matplotlib import pyplot as plt
from sklearn.preprocessing import StandardScaler
import numpy as np
import scipy as sp
import warnings

from pyspec.utils import Hankelize

"""
It might be tempting to think of SSA as merely a procedure for smoothing via moving averages but in fact
the key to this technique is the generation of Hankel matrices that are able to decompose, in an
unsupervised manner, the original time series as the weighted sum of several other time series's. In 
this way, we can examine the contribution of each component individually.
"""

class TimeSeries(object):
    def __init__(self, data):
        """

        :param data:
        :param standardization:
        """
        self.data = np.array(data)
        self.data = self.data-np.mean(self.data)
        self.data = self.data/np.var(self.data)
        self.N = self.data.shape[-1]

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

class SSA(object):
    #TODO: Add a summary plotting function that displays the data, elementary matrices, Hankel matrices, eigentriple magnitudes, and reconstructions
    def __init__(self, TimeSeries, L):
        """

        :param TimeSeries:
        :param L: The window size chosen between 2 and N-1 inclusive.
        """
        self.TS = TimeSeries.data
        self.L = L
        self.K = len(self.TS) - L + 1

    def _embedding(self):
        self.X_traj = np.zeros([self.K,self.L])

        for i in range(self.L):
            self.X_traj[:,i] = self.TS[i:(self.K+i)] #This procedure creates the trajectory matrix

        self.X_cov = (self.X_traj.T@self.X_traj)/self.K #This embedding generates the covariance matrix

        return self.X_cov, self.X_traj

        # X = np.column_stack([F[i:i+L] for i in range(0,K)])
        # HX = Hankelize(X)
        # return HX

    @staticmethod
    def _eigendecomp(X_cov, X_traj):

        eigvals, W = np.linalg.eig(X_cov)
        PCs = (X_traj@W).T

        return PCs, W, eigvals

        # d = np.linalg.matrix_rank(X)
        # U, S, V = np.linalg.svd(X)
        # V = V.T #np.linalg.svd actually returns the transpose of V
        #
        # # X_elem = np.array([S[i] * np.outer(U[:,i], V[:,i]) for i in range(0,d)] )

        # return U, S, V

    # @staticmethod
    # def _grouping(X):
    #     """
    #     This method currently does not support grouping of trajectory matrices into trend, periodic, and aperiodic
    #     regimes.
    #     :param HX:
    #     :return:
    #     """
    #     warnings.warn('Grouping operations currently unsupported; returning argument',UserWarning)
    #
    #     return X

    def _reconstruction(self,PCs,W):
        RCs = np.zeros([len(self.TS),self.L])

        for i in range(self.L):
            buf = PCs[:,i]*W[:,i].T
            buf = buf[-1:1,:]

            for j in range(len(self.TS)):
                RCs[j,i] = np.mean(np.diag(buf,-self.K+j))

        return RCs

    # @staticmethod
    # def _diagonal_averaging(X):
    #     """
    #
    #     :param X:
    #     :return:
    #     """
    #     X_rev = X[::-1]
    #     X_avg = np.array([X_rev.diagonal(i).mean() for i in range(-X.shape[0]+1, X.shape[1])])
    #
    #     return X_avg

    def process(self):
        X_cov, X_traj = self._embedding()
        self.PCs, W, self.eigvals = self._eigendecomp(X_cov,X_traj)
        # self.RCs = self._reconstruction(self.PCs,W)

        return None








