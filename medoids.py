import random
import pandas as pd
import numpy as np
import copy
from utili import *

def best_k_medoid(X,soglia):
    #il minimo numero di cluster da cui partire è k=1
    k=1
    #inizializzo var a 1 affinchè esso sia maggiore di soglia
    var=1
    #lista contenente tutti i costi finali per ogni valore di k
    costi = []
    #lista contenente il numero di cluster a cui corrisponde il costo
    kappa = []
    #lista contenente le posizioni dei cluster
    centroidi = []
    #calcolo l'errore con un cluster
    centroid, cost = medoids(X, k)
    print("Initial cost:\t",format(cost,".4f"),"\tk:1")
    #aggiungo il primo costo alla lista
    costi.append(cost)
    #aumento il numero k dei cluster fino a che non raggiungo un decremento relativo della cost function minore della soglia prevista
    while var>soglia:
    # for k in range (0,10):
        k+=1
        stop = 0
        #centroid, cost, start = k_mean(X, i)
        centroid, cost = medoids(X, k)
        #salvo la posizione finale dei centroidi
        centroidi.append(centroid)
        #costi contiene l'errore globale minimo associato a k cluster scelti
        costi.append(cost)
        print("Actual error:\t",format(costi[len(costi)-1],".4f"))
        #kappa contiene il relativo numero di cluster
        kappa.append(k)
        #calcolo la variazione relativa fra il costo calcolato e quello trovato nella iterazione precedente
        var=-((costi[len(costi)-1]-costi[len(costi)-2])/costi[len(costi)-2])
        print("variazione: ",format(var*100,".2f"),"%","\tk:",kappa[len(kappa)-1])
    #stampo l'andamento della cost function in relazione all'aumento dei cluster
    plotLearningK(costi)
    #Ritornerà da questa funzione il k scelto, il relativo costo finale associato a quel numero di cluster ed il cluster stesso
    return kappa[len(kappa)-2], costi[len(costi)-2], centroidi[len(centroidi)-2]

#cerco il numero migliore di cluster
def medoids(X,k):
    stop = 0
    #assign contiene il medoid di appartenenza di ogni riga di X
    assign = np.zeros(X.shape[0])
    #medoid contiene la posizione di ogni medoid
    medoid = []
    #ogni medoid inizialmente conterrà una delle righe di X
    medoid = init_centroid(medoid, X, k)
    conto = 0
    while stop!=1:
    # for i in range(0,20):
        #Per ogni riga di X trovo il medoid più vicino
        #dist: contiene la distanza fra ogni x ed il relativo medoid di appartenenza
        #assign: il medoid di appartenenza di tutte le righe di X
        dist,assign = assegna(X,medoid,assign)
        # print("assign\t",assign,"\nmedoid:\t",medoid)
        #calcolo la cost function dividendo la somma delle distanze fra righe e medoid di appartenenza per il numero di righe di X
        cost = (sum(dist))/X.shape[0]
        # print("dist",cost)
        #Ricalibro la posizione di ogni assign
        # print("prima",medoid)
        #seleziono un medoid casuale e provo a trovarne uno migliore all'interno di X
        medoid,stop = ricalibro(medoid, assign, X,cost)
        # print("dopo",medoid)
        #Tengo il conto delle iterazioni utili alla convergenza
        conto += 1
    print("numero iterazioni:",conto,", costo: ",costo(X,medoid,assign))
    return medoid, cost


def init_centroid(medoid, X, k):
    #Scelgo k righe di X da assegnare ai assigni iniziali naturalmente diverse
    scelti=[]
    while(len(scelti) < k):
        rand = random.randint(0, X.shape[0]-1)
        #se non ho già inserito quella riga di X fra i assigni la aggiungo
        if rand not in scelti:
            medoid.append(X[rand])
            #Aggiungo il numero di riga di X aggiunta fra i assigni per poterne controllare la presenza
            scelti.append(rand)
        # print(len(scelti))
    return medoid

def costo(X,medoid,assign):
    dist = np.ones(X.shape[0])
    # Ricordo la configurazione iniziale di assign
    for i in range(0, X.shape[0]):
        dist[i], assign[i] = minimo(X[i], medoid)
    cost = (sum(dist)) / X.shape[0]
    return cost

def assegna(X,medoid,assign):
    dist = np.ones(X.shape[0])
    #Ricordo la configurazione iniziale di assign
    for i in range (0,X.shape[0]):
        dist[i],assign[i]=minimo(X[i],medoid)
    # print(cent,assign)
    return dist,assign

def ricalibro(medoid,assign,X,cost):
    medoid1 = copy.deepcopy(medoid)
    rand = random.randint(0,len(medoid1)-1)
    # se non ho già inserito quella riga di X fra i assigni la aggiungo o se non ripesco la stessa riga di X
    for i in range (0,X.shape[0]):
        stop = 1
        # print("tentativo")
        # print("prima\t",assign)
        #cambio il medoid scelto con la prima X con cui avrei una diminuzione della cost function
        #medoid1: nuova configurazione dei medoid
        medoid1[rand] = cambio(medoid1[rand], X[i],medoid1)
        #prima di calcolare il posto dorvrò riassegnare gli elementi al cluster più vicino della nuova configurazione
        dist, assign = assegna(X, medoid, assign)
        # print("dopo\t",assign)
        #calcolo il costo della differente configurazione dei medoid
        cost1 = costo(X, medoid1, assign)
        # print(cost,cost1)
        #se il costo associato al cambio è inferiore a quello precedente restituisco la nuova configurazione e continuo ad iterare
        if cost1<cost:
            stop=0
            # print("cambio")
            return medoid1,stop
        # else:
        #     print("no changes")
    #Se non trovo alcun medoid da sostituire ritengo di aver terminato l'esecuzione
    return medoid, stop

def cambio(clust,X,medoid):
    bool = True
    #verifico che la riga selezionata sia già un medoid
    for i in range (0,len(medoid)):
        if np.array_equal(X,medoid[i]):
            bool = False
    #se non sto selezionando la stessa riga e se essa non è già un medoid faccio ritornare la riga stessa
    if not(np.array_equal(X,clust)) and bool:
        # print("forse",X,clust)
        clust = copy.deepcopy(X)
        return clust
    return clust

# def diverso(X,Y):
#     bolla=1
#     for i in range(0,len(Y)):
#         if np.array_equal(X,Y[i]):
#             bolla=0
#     if bolla==1:
#         return True



#cerco il medoid più vicino all'elemento X in esame
def minimo (X,medoid):
    #lista contenente le distanze di X con tutti i medoid
    mu=[]
    for i in range (0,len(medoid)):
        #print("ops",medoid[i],"cfhfg",X)
        mu.append(sum((X-medoid[i]))**2)
    # print("mu",mu)
    # print("minimo",min(mu))
    # print("indice",mu.index(min(mu)))

    #ritornerà dalla funzione la distanza minima trovata ed il relativo medoid
    return min(mu),mu.index(min(mu))

def stampa(text, variabile):
    print(text)
    for i in range(0, len(variabile)):
        print(variabile[i])


