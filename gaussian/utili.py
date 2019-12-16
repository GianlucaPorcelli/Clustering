import numpy as np
import math
import copy
import random

# def prob(x, mu, covar, pi):
#     print("Todo: calcolo la probabilità")
#     #Calcolo la differenza tra il vettore x e il vettore mu
#     diff_x_mu = (x - mu)
#     #Moltiplico la differenza appena calcolata con la matrice inversa della covarianza
#     z = np.dot(diff_x_mu.T, np.linalg.inv(covar))
#     #Calcolo l'argomento dell'esponente
#     z = -1/2 * np.dot(z, diff_x_mu)
#     #Calcolo il denominatore
#     den = math.sqrt(((2 * pi) ^ len(x)) * np.linalg.det(covar))
#     prob = np.exp(-z) / den
#     return prob

def responsibility(mu, covar, x, pi, j):
    num = numeratore(mu[j], covar[j], pi[j], x)
    den = denominatore(mu, covar, pi, x)
    # print("num,den",num,den)
    r = num / den

    return r

def mean(r, x):
    # media = []
    r_aux = np.asmatrix(r)

    prod = 0
    for i in range(r_aux.shape[1]):
        prod += r_aux[:, i] * x[i]

    mu = prod / sum(r)
    #Trasformo mu in una lista, perchè stavo utilizzando le liste
    mu = mu.tolist()
    return mu[0]
    # prod = 0
    # for i in range(len(r)):
    #     prod += r[i] * x[i]
    # prod = sum(prod)
    #
    # #La media inerente al cluster j è pari alla sommatoria di rij*la i-riga del dataset diviso la sommattoria di tutti gli r appartenenti al cluster in esame
    # mu = prod / sum(r)
    # print(mu)
    # return mu

def covarianza(r, x, mu):
    r_aux = np.asmatrix(r)
    # print(x)
    # print("r_aux", r)
    #prod = []
    num = 0
    # print("adasdadsada",mu)
    for i in range(x.shape[0]):
        diff = (x[i] - mu)
        # print("diff",diff)
        diff = np.asmatrix(diff)
        prod = r_aux[:, i] * diff
        prod = np.dot(prod.T, diff)

        num += prod
    # print("num", num)
    # prod.append(np.dot(diff, diff.T))
    # prod = np.asmatrix(prod)
    cov = num / sum(r)
    # cov = cov.tolist()
    cov = np.asarray(cov).reshape((x.shape[1],x.shape[1]))
    # ==============================================================================================
    # Se la matrice di covarianza è singolare dovrò ripristinarla
    while np.linalg.det(cov) == 0:
        print(cov)
        cov = covarianza_singola(x[0])
        print("Matrice singolare cambio:\n", cov)
    # ==============================================================================================

    # print("nico", cov,"\n",cov)
    return cov

def mix_coeff(r, m):
    pi = (1/m) * sum(r)
    return pi


#Funzione per calcolare il numeratore della responsibility
def numeratore(mu, covar, pi, x):
    # Calcolo la differenza tra il vettore x e il vettore mu
    diff = (x - mu)
    # Moltiplico la differenza appena calcolata con la matrice inversa della covarianza
    # print("covar:\n",covar)
    covar_new=copy.deepcopy(covar)
    #==============================================================================================
    # Se la matrice di covarianza è singolare dovrò ripristinarla
    # if np.linalg.det(covar_new) == 0:
    #     # scelgo di ripristinare la matrice di covarianza in questa maniera
    #     # cov = np.zeros((3, 3))
    #     # for i in range(cov.shape[0]):
    #     #     for j in range(cov.shape[0]):
    #     #         if i == j:
    #     #             cov[i, j] = random.randint(1,3)
    #     cov=covarianza_singola(x)
    #     print("Matrice singolare cambio:\n",cov)
    #     covar_new = copy.deepcopy(cov)
    #==============================================================================================
    z = np.dot(diff.T, np.linalg.inv(covar_new))
    # Calcolo l'argomento dell'esponente
    z = 1 / 2 * np.dot(z, diff)
    # Calcolo il denominatore
    den = math.sqrt(math.pow((2 * 3.14), x.shape[0]) * np.linalg.det(covar_new))
    # print("denominatore1: ",den)
    num = (pi * np.exp(-z) / den)
    return num



def denominatore(mu, covar, pi, x):
    ris = 0
    for j in range(len(pi)):
        diff = (x - mu[j])
        # Moltiplico la differenza appena calcolata con la matrice inversa della covarianza
        covar_new = copy.deepcopy(covar[j])
        # ==============================================================================================
        # # Se la matrice di covarianza è singolare dovrò ripristinarla
        # if np.linalg.det(covar_new) == 0:
        #     # scelgo di ripristinare la matrice di covarianza in questa maniera
        #     # cov = np.zeros((3, 3))
        #     # # print("2")
        #     # for i in range(cov.shape[0]):
        #     #     for j in range(cov.shape[0]):
        #     #         if i == j:
        #     #             cov[i, j] = 1
        #     cov = covarianza_singola(x)
        #     print("Matrice singolare cambio:\n", cov)
        #     covar_new = copy.deepcopy(cov)
        # ==============================================================================================
        z = np.dot(diff.T, np.linalg.inv(covar_new))
        # Calcolo l'argomento dell'esponente
        z = 1 / 2 * np.dot(z, diff)
        # Calcolo il denominatore
        den = math.sqrt(math.pow((2 * 3.14), x.shape[0]) * np.linalg.det(covar_new))
        # print("denominatore 2: ",den)
        ris += (pi[j] * np.exp(-z) / den)

    return ris

def cluster_probabile(mu, covar, pi, x):
    prob=[]
    for j in range(len(pi)):
        diff = (x - mu[j])
        # Moltiplico la differenza appena calcolata con la matrice inversa della covarianza
        covar_new = copy.deepcopy(covar[j])
        # ==============================================================================================
        # # Se la matrice di covarianza è singolare dovrò ripristinarla
        # if np.linalg.det(covar_new) == 0:
        #     # scelgo di ripristinare la matrice di covarianza in questa maniera
        #     # cov = np.zeros((3, 3))
        #     # # print("2")
        #     # for i in range(cov.shape[0]):
        #     #     for j in range(cov.shape[0]):
        #     #         if i == j:
        #     #             cov[i, j] = 1
        #     cov = covarianza_singola(x)
        #     covar_new = copy.deepcopy(cov)
        # ==============================================================================================
        z = np.dot(diff.T, np.linalg.inv(covar_new))
        # Calcolo l'argomento dell'esponente
        z = 1 / 2 * np.dot(z, diff)
        # Calcolo il denominatore
        den = math.sqrt(math.pow((2 * 3.14), x.shape[0]) * np.linalg.det(covar_new))
        # print("denominatore 2: ",den)
        ris = (pi[j] * np.exp(-z) / den)
        prob.append(copy.deepcopy(ris))
    return prob.index(max(prob))

def assegnazioni(X,mu, covar, pi):
    ass=np.ones(X.shape[0])
    for i in range(0,X.shape[0]):
        ass[i]=cluster_probabile(mu, covar, pi, X[i])
    return ass

def covarianza_singola(X):
    cov = np.ones((X.shape[0], X.shape[0]))
    for i in range(cov.shape[0]):
        for j in range(cov.shape[0]):
            if i == j:
                cov[i, j] = random.randint(2,5)
    return cov