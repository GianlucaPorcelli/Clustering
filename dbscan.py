import math
from utili import *


def dbscan(X,epsilon,minimo):
    #Conto per ogni punto in quanti appartengono alla sua circonferenza
    Count=conto(X,epsilon)
    #Per ogni punto se esso possiede più di "minimo" elementi nella propria circonferenza esso sarà aggiunto alla lista core
    Core=core(X,Count,minimo)
    #se un punto è nel range di core ma non è egli stesso un core è un border point
    Border=border(X,Core,epsilon)
    #se un punto non è nè un core nè un border allora sarà un noise point
    Noise=noise(X,Core,Border)
    print ("\ncore\n",len(Core),"\nborder\n",len(Border),"\nNoise\n",len(Noise),"\nx\n",X.shape[0])

def conto(X,epsilon):
    Count=np.zeros(X.shape[0])
    #La distanza fra i due punti deve essere minore di epslylon
    for i in range (0,X.shape[0]):
        for j in range(0, X.shape[0]):
            #Conto per ogni elemento quanti sono contenuti nella sua circonferenza
            if cerchio(X[i],X[j],epsilon):
                Count[i]+=1
    return Count

def core(X,Count,minimo):
    Core=[]
    for i in range (0,Count.shape[0]):
        #se posseggo più elementi di minimo nella circonferenza sarò un core point
        if Count[i]>minimo:
            Core.append(X[i])
    return Core

def border(X,Core,Epsilon):
    Border=[]
    for k in range (0,len(Core)):
        for i in range (0,X.shape[0]):
            #se la riga i-esima è nella circonferenza di un core ma non è esso stesso un core point allora farà parte di border
            if cerchio(Core[k],X[i],Epsilon) and non_sta(X[i],Core):
                Border.append(X[i])
                break
    return Border

def noise(X,Core,Border):
    Noise=[]
    for i in range (0,X.shape[0]):
        #punti non appartenente a nessun insieme saranno definiti noise point
        if non_sta(X[i],Core) and non_sta(X[i],Border):
            Noise.append(X[i])
    return Noise



def cerchio(X,Y,raggio):
    sum=0
    for i in range (0,X.shape[0]):
        sum+=pow((X[i]-Y[i]),2)
    if math.sqrt(sum)<raggio:
        #Il punto è all'interno della circonferenza
        return True

def non_sta(X,Core):
    for i in range(0,len(Core)):
        #se X corrisponde ad almeno un elemento di Core allora ritornerà False
        if np.array_equal(X,Core[i]):
            return False
    #se X non è presente in alcun elemento di Core, allora ritornerà True
    return True

def stampa(text, variabile):
    print(text)
    for i in range(0, len(variabile)):
        print(variabile[i])


