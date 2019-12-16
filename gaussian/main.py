import pandas as pd
import sys
from gaussian import *
import random
import copy

#Todo: IMPORTANTE: mu, e pi devono rimanere sempre delle liste


#Importiamo il csv e lo trasformiamo in una matrice
data = pd.read_csv("candy_1.csv", sep=",", header=None)
#Generiamo la matrice del nostro dataset
data = data.as_matrix()
#Creiamo le matrici x e y
X = data[:, 6:data.shape[1]-2]
# print("X", X)

#y = data[:, -1]

# #Variabile per stabilire il numero di cluster che si vogliono ottenere
# K = 2

#Lista media delle gaussiane da cui si vuole partire
# mu = [[1, 1, 1], [0.2, 0.2, 0.2], [0.5, 0.5, 0.5]]
# k=random.randint(2,X.shape[1])
k=3
print("Numero di cluster: ",k)
mu=media(X,k)
print(mu)

# cov = np.zeros((3,3))
# for i in range(cov.shape[0]):
#     for j in range(cov.shape[0]):
#         if i == j:
#             cov[i, j] = 1
#
#
# #Lista covarianza delle gaussiane da cui si vuole partire
# covar = [cov, cov, cov]

covar=covarianza_multipla(X,k)
print(covar)


# print("covarianza iniziale:\n",covar)

#Lista dei mixing coefficient
# pi = [0.1, 0.4, 0.5]

pi=pigreco(k)
print(pi)

# #Controllo sulla dimensione di mu e covar, in quanto deve essere uguale a k
# if len(mu) != K and len(covar) != K:
#     print("mu e covar devono avere la stessa dimensione di k")
#     sys.exit()

#Richiamo la funzione gaussian mixture, per avviare l'algoritmo delle misture delle gaussiane
num_iter=50
r,mu,pi,covar = gaussian_mixture(mu, covar, X, pi,num_iter)
print("pi: \n",pi,"\nmedia:\n ",mu,"\ncovarianza: \n",covar)
ass = assegnazioni(X,mu, covar, pi)
print("Cluster assegnati:\n",ass)