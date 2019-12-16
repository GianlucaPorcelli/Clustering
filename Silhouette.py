import numpy as np
import math
from kMean import  *

def coh(X,assign):
    #contiene la somma delle distanze fra cluster i-esimo ed i punti che esso contiene
    diff=np.zeros(X.shape[0])
    #contiene il numero di punti nel centroide i-esimo
    count=np.zeros(X.shape[0])

    for i in range (0,X.shape[0]):
        for k in range(0, X.shape[0]):
            #index conterrà il cluster di appartenenza della riga i-esima di X
            index=int(assign[i])
            #index_k conterrà il cluster di appartenenza della riga k-esima di X
            k_index=int(assign[k])
            #calcolo la distanza fra la riga i-esima e quella k-esima appartenenti allo stesso cluster
            if index==k_index:
                diff[i] += distanza(X[i],X[k])
                #incremento il contatore del numero di elementi del cluster index-esimo
                count[i] += 1
        # print("diff,count",diff[i],count[i])
        diff[i]/=count[i]
        # print("diff_new",diff[i])
    #ritornerà dalla funzione la somma delle distanze fra ogni cluster ed i suoi componenti fratto il numero dei punti rappresentati
    return diff

def sep(X,assign):
    #contiene la somma delle distanze fra cluster i-esimo ed i punti che esso contiene
    minimo=np.zeros(X.shape[0])

    for i in range (0,X.shape[0]):
        dist=[]
        for k in range(0, X.shape[0]):
            #index conterrà il cluster di appartenenza della riga i-esima di X
            index=int(assign[i])
            #index_k conterrà il cluster di appartenenza della riga k-esima di X
            k_index=int(assign[k])
            #calcolo la distanza fra la riga i-esima e quella k-esima appartenenti a cluster diversi
            if index!=k_index:
                dist.append(distanza(X[i],X[k]))
        minimo[i]=min(dist)
    #ritornerà dalla funzione la somma delle distanze fra ogni cluster ed i suoi componenti fratto il numero dei punti rappresentati
    return minimo

def Si(Coh,Sep):
    Si=np.zeros(Coh.shape[0])
    for i in range(0,Coh.shape[0]):
        if Coh[i]<Sep[i]:
            Si[i] = 1 - (Coh[i]/Sep[i])
        else:
            Si[i] = (Sep[i]/Coh[i]) - 1
    return Si

def distanza (X,Y):
    somma = 0
    for i in range (0,X.shape[0]):
        somma+=pow(X[i]-Y[i],2)
    return math.sqrt(somma)

def silouette(X):
    for k in range (2,X.shape[0]):
        print("\nUtilizzo",k,"cluster")
        centroid, costo = global_min(X, k, 100)
        # print("centroidi: ", centroid, "\n\n")
        assign = np.zeros(X.shape[0])
        dist, assign, stop = assegna_k(X, centroid, assign)
        # print(assign)
        Coh = coh(X, assign)
        Sep = sep(X, assign)
        # print(Coh,"\n\n",Sep)
        S = Si(Coh, Sep)
        # print("Si\n", S)
        print("coefficiente di sagoma: ", np.mean(S))