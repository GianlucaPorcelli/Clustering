import pandas as pd
#import numpy as np

#Per matplot
from utili import *
from norm import *
from kMean import *
from medoids import *
from pca import *

def PCA(X,k):
    Cov=cov(X)
    # print("Cov:\n",Cov)
    U,S,V=np.linalg.svd(Cov,full_matrices=True,compute_uv=True, hermitian=False)
    # print("u",u,"\nd",d,"\nv",v)
    Ureduce = U[:, 0:k]
    Z=np.dot(Ureduce.T,X.T)
    return Z.T,Ureduce,S,V

def cov(X):
    Sigma=np.zeros((X.shape[1],X.shape[1]))
    m = X.shape[0]
    for i in range(0,m):
        aux=copy.deepcopy(np.asmatrix(X[i]))
        Sigma+=np.dot(aux.T,aux)
        # print("Sigma",Sigma)
    Sigma/=m
    return Sigma

def best_k_PCA(X,soglia):
    Z, Ureduce, S, V = PCA(X, 1)
    Stot=sum(S)
    k=0
    while True:
        if 1-(sum(S[:k])/Stot)<=soglia:
            # print("S",S[:k],k)
            # print("hop",1-(sum(S[:k])/Stot))
            return PCA(X,k)
        k+=1