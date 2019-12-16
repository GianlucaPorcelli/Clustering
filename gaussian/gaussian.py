from utili import *
import copy
import random

#Funzione algoritmo misture di gaussiane
def gaussian_mixture(mu, covar, x, pi,num):

    #Devo iterare fino alla convergenza
    for z in range(num):
        # Lista della responsibility
        r = []
        med = []
        covari = []
        pig = []

        # Calcolo la probabilità che la tupla appartenga ad uno dei k cluster
        for j in range(len(mu)):
            #Lista provvisoria di r
            ri = []
            # Per ogni tupla del nostro dataset
            for i in range(x.shape[0]):
                #Calcolo la responsibility, ossia la probabilità che quel valore ricada in un cluster
                #Viene calcolato utilizzando media, covarianza e mixing coefficient ottenuti nell'iterazione precedente
                ri.append(responsibility(mu, covar, x[i], pi, j))
            # print("ri", ri)

            #Inserisco all'interno della lista r i valori delle responsability ottenute per il cluster j su ogni tupla
            r.append(copy.deepcopy(ri))
            # print("r", r)

            #Posso sostituire direttamente perchè all'iterazione successiva mi serviranno solo i valori dell'iterazione precedente
            #Calcolo la media
            med.append(mean(ri, x))
            # print("mean: ",mean(ri, x))
            #Calcolo il mixing coefficient
            pig.append(mix_coeff(ri, x.shape[0]))
            # print("pig: ",mix_coeff(ri, x.shape[0]))
            #Calcolo la covarianza
            covari.append(covarianza(ri, x, mu[j]))
            # print("cov: ",covarianza(ri, x, mu[j]))
        #Aggiorno mu
        mu = med
        # print("mu i-esimo\n",mu)
        #Aggiorno pi
        pi = pig
        # print("pi i-esimo\n",pi)
        #Aggiorno covar
        # print("covarianza i-esima\n",covari)
        covar = covari
        # covar = np.asmatrix(covari)
    return r,mu,pi,covar

def media(X,k):
    lista=[]
    for i in range(0, k):
        media = []
        for i in range(0,X.shape[1]):
            ran=random.randint(0,3)
            media.append(ran)
        lista.append(copy.deepcopy(media))
    return lista

def covarianza_multipla(X,k):
    cov=[]
    for i in range (0,k):
        C=covarianza_singola(X)
        cov.append(copy.deepcopy(C))
    return cov



def covarianza_singola(X):
    cov = np.ones((X.shape[1], X.shape[1]))
    for i in range(cov.shape[0]):
        for j in range(cov.shape[0]):
            if i == j:
                cov[i, j] = random.randint(2,5)
    return cov

def pigreco(k):
    list=[]
    count=0
    for i in range (0,k-1):
        numero=random.uniform(0,1-count)
        list.append(numero)
        count+=numero
    list.append(1-count)
    return list





