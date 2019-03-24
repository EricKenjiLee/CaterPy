from numpy import eye, asarray, dot, sum, diag, zeros, array, sin, pi
from numpy.linalg import svd
from numpy.random import randn

def Hankelize(X):
    """ Adapted from Jordan D'Arcy's Kaggle post

    Hankelises the matrix X, returning H(X).
    """
    L, K = X.shape
    transpose = False
    if L > K:
        # The Hankelisation below only works for matrices where L < K.
        # To Hankelise a L > K matrix, first swap L and K and tranpose X.
        # Set flag for HX to be transposed before returning.
        X = X.T
        L, K = K, L
        transpose = True

    HX = zeros((L, K))

    # I know this isn't very efficient...
    for m in range(L):
        for n in range(K):
            s = m + n
            if 0 <= s <= L - 1:
                for l in range(0, s + 1):
                    HX[m, n] += 1 / (s + 1) * X[l, s - l]
            elif L <= s <= K - 1:
                for l in range(0, L - 1):
                    HX[m, n] += 1 / (L - 1) * X[l, s - l]
            elif K <= s <= K + L - 2:
                for l in range(s - K + 1, L):
                    HX[m, n] += 1 / (K + L - s - 1) * X[l, s - l]
    if transpose:
        return HX.T
    else:
        return HX

def synthesize_data(n_timepoints,T,SNR):
    t = array(range(n_timepoints))
    X = sin(2 * pi * t / T)
    noise = SNR * randn(len(X))

    X = X + noise
    return X

def varimax(Phi, gamma = 1, q = 20, tol = 1e-6):
    p,k = Phi.shape
    R = eye(k)
    d=0
    for i in range(q):
        d_old = d
        Lambda = dot(Phi, R)
        u,s,vh = svd(dot(Phi.T,asarray(Lambda)**3 - (gamma/p) * dot(Lambda, diag(diag(dot(Lambda.T,Lambda))))))
        R = dot(u,vh)
        d = sum(s)
        if d/d_old < tol: break
    return dot(Phi, R)