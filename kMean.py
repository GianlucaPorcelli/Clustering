import random
import copy
from utili import *

#Evito di ricadere in un minimo locale usando questa procedura iterativa
def global_min(X,k,num):
    #lista contenente la posizione dei centroidi
    globale = []
    #lista contenente il valore della relativo costo finale
    costo = []
    #init=[]
    #Cerco un minimo globale riassegnando caualmente num volte la posizione iniziale dei centroidi
    for i in range (0,num):
        centroid, cost = k_mean(X,k)
        globale.append(copy.deepcopy(centroid))
        costo.append(copy.deepcopy(cost))
        #init.append(copy.deepcopy(start))
    #salvo in index l'indice in cui è salvata la configrazione dei centroidi a cui corrisponde il costo minore
    index = costo.index(min(costo))
    return globale[index],costo[index]#, init[index]

#cerco il numero migliore di cluster
def best_k(X,soglia,num):
    #il minimo numero di cluster da cui partire è k=1
    k = 1
    #inizializzo var a 1 affinchè esso sia maggiore di soglia
    var = 1
    #lista contenente tutti i costi finali per ogni valore di k
    costi = []
    #lista contenente il numero di cluster a cui corrisponde il costo
    kappa = []
    #lista contenente le posizioni dei cluster
    centroidi = []
    #calcolo l'errore con un cluster
    centroid, cost = global_min(X, k, num)
    print("Initial cost:\t",format(cost,".4f"),"\tk:1")
    #aggiungo il primo costo alla lista
    costi.append(cost)
    #aumento il numero k dei cluster fino a che non raggiungo un decremento relativo della cost function minore della soglia prevista
    while var>soglia:
    # for k in range (0,10):
        k += 1
        stop = 0
        #centroid, cost, start = k_mean(X, i)
        centroid, cost = global_min(X, k, num)
        #salvo la posizione finale dei centroidi
        centroidi.append(centroid)
        #costi contiene l'errore globale minimo associato a k cluster scelti
        costi.append(cost)
        print("Actual error:\t",format(costi[len(costi)-1],".4f"))
        #kappa contiene il relativo numero di cluster
        kappa.append(k)
        #calcolo la variazione relativa fra il costo calcolato e quello trovato nella iterazione precedente
        var =- ((costi[len(costi)-1]-costi[len(costi)-2])/costi[len(costi)-2])
        print("variazione: ",format(var*100,".2f"),"%","\tk:",kappa[len(kappa)-1])
    #stampo l'andamento della cost function in relazione all'aumento dei cluster
    plotLearningK(costi)
    #Ritornerà da questa funzione il k scelto, il relativo costo finale associato a quel numero di cluster ed il cluster stesso
    return kappa[len(kappa)-2], costi[len(costi)-2], centroidi[len(centroidi)-2]


def k_mean(X,k):
    stop = 0
    #assign contiene il centroider di appartenenza di ogni riga di X
    assign =  np.zeros(X.shape[0])
    #centroid contiene la posizione di di ogni centroider
    centroid = []
    #ogni centroid inizialmente conterrà una delle righe di X
    centroid = init_centroid(centroid, X, k)
    #Mantengo in memoria la configurazione iniziale dei centroider
    #init=copy.deepcopy(centroid)
    conto = 0
    while stop != 1:
    # for i in range(0,20):
        #Inizializzazione dei centroider manuale
        #stampa("centroider centre: ", centroid)
        #Per ogni riga di X trovo il centroider più vicino
        #dist: contiene la distanza fra ogni x ed il relativo centroider di appartenenza
        #assign: il centroide di appartenenza di tutte le righe di X
        #stop: variabile bloccante l'algoritmo quando non viene riassegnato alcun elemento di X
        dist,assign,stop = assegna_k(X,centroid,assign)
        #print("assign",assign)
        #calcolo la dost function dividendo la somma delle distanze fra righe e centroider di appartenenza per il numero di righe di X
        cost = (sum(dist))/X.shape[0]
        # print("dist",cost)
        #Ricalibro la posizione di ogni assigne
        centroid = ricalibro(centroid, assign, X,k)
        # print("centroid",centroid[i],"sum",sum,"cont",count)
        #Tengo il conto delle iterazioni utili alla convergenza
        conto += 1
    # print("numero iterazioni:",conto)
    return centroid, cost


def init_centroid(centroid, X, k):
    #Scelgo k righe di X da assegnare ai assigni iniziali naturalmente diverse
    scelti=[]
    while(len(scelti) < k):
        rand = random.randint(0, X.shape[0]-1)
        #se non ho già inserito quella riga di X fra i assigni la aggiungo
        if rand not in scelti:
            centroid.append(X[rand])
            #Aggiungo il numero di riga di X aggiunta fra i assigni per poterne controllare la presenza
            scelti.append(rand)
        # print(len(scelti))
    return centroid


def assegna_k(X,centroid,assign):
    dist = np.ones(X.shape[0])
    #Ricordo la configurazione iniziale di assign
    cent = copy.deepcopy(assign)
    for i in range (0,X.shape[0]):
        dist[i],assign[i] = minimo(X[i],centroid)
    #se la variabile stop non verrà modificato vorrà dire che la convergenza è stata raggiunta
    stop = 1
    for i in range(0,len (cent)):
        #Se c'è stata almeno una variazione della lista assign dovrò continuare ad iterare
        if cent[i] != assign[i]:
            #print("confronto: ",cent[i],assign[i])
            stop = 0
    # print(cent,assign)
    return dist,assign, stop

def ricalibro(centroid,assign,X,k):
    for i in range (0,k):
        sum = np.zeros(X.shape[1])
        #variabile contenete il numero di elementi di cui è composto il centroider i-esimo
        count = 0
        for j in range(0, X.shape[0]):
            #Se il centroider della riga j-esima corrisponde al centroider di cui stiamo calcolando la posizione (centroider i-esimo)
            if assign[j]==i:
                count += 1
                #conteggio nella somma la riga j-esima
                sum += X[j]
        #la nuova posizione del centroider sarà la posizione media degli elementi che lo compongono
        centroid[i] = sum/count
    return centroid

#cerco il centroider più vicino all'elemento X in esame
def minimo (X,centroid):
    #lista contenente le distanze di X con tutti i centroider
    mu = []
    for i in range (0,len(centroid)):
        #print("ops",centroid[i],"cfhfg",X)
        mu.append(sum((X-centroid[i]))**2)
    # print("mu",mu)
    # print("minimo",min(mu))
    # print("indice",mu.index(min(mu)))

    #ritornerà dalla funzione la distanza minima trovata ed il relativo centroider
    return min(mu),mu.index(min(mu))

def stampa(text, variabile):
    print(text)
    for i in range(0, len(variabile)):
        print(variabile[i])


