import numpy as np

def Feat_Scaling(x, max):
    #Feature Scaling
    x = (x / max)
    return x

def minmax(x):
    max_x = []  # Lista in cui mi salvo il massimo di ciascuna feature
    min_x = []  # Lista in cui mi salvo il minimo di ciascuna feature
    aux = []  # Lista contenente tutti i max - min
    x = x.T  # Effettuo la trasposta di x, altrimenti mi prende il massimo di ogni riga anzichè di ogni colonna
    for columns in x:
        max_x.append(columns.max())
        min_x.append(columns.min())
        aux.append(columns.max() - columns.min())

    return (min_x, aux, max_x)

# Min-Max normalization
def Min_Max(x, min, aux):
    a = 0
    b = 1

    x = ((x - min) / aux)*(b-a)+a

    return x

def muSigma(X):
    return (np.mean(X, axis = 0), np.std(X, axis = 0))

def zScore(X, mu, sigma):
    return np.divide((X - mu), sigma)


