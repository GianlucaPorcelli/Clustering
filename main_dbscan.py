import pandas as pd
from norm import *
from dbscan import *

#------------------------------- IMPORT CSV + MODIFICHE DATASET -------------------------------#

#Importiamo il csv e lo trasformiamo in una matrice
data = pd.read_csv("candy_1.csv", sep = ",", header=None)
data = data.as_matrix()
#Creiamo la matrice x
X = data[:, :data.shape[1]-1]
#------------------------------------ NORMALIZAZZIONE FEATURE ---------------------------------#

#------------------------------------- ZSCORE -----------------------------------#


mu, sigma = muSigma(X)
X = zScore(X, mu, sigma)

#--------------------------------------------------------------------------------#


#------------------------------------ MINMAX ------------------------------------#

# min, diff, max = minmax(X)
# X = Min_Max(X, min, diff)

#--------------------------------------------------------------------------------#


#-------------------------------- FEATURE SCALING -------------------------------#

# min, diff, max = minmax(X)
# X = Feat_Scaling(X, max)

#--------------------------------------------------------------------------------#
epsylon=2
punti_min=2
centroid=dbscan(X,epsylon,punti_min)
