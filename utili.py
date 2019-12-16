import numpy as np
import matplotlib.pyplot as plt

def predict(X, theta):
    return np.dot(X, theta)
    #Y = [m * 1] = h

def predictLog(theta, x, algo):
    z = np.matmul(x, theta)
    y = 1 / (1 + np.exp(-z))
    if algo == 1:
        #print(y)
        #Se il risultato è maggiore di 0.5 appartiene alla classe 1, altrimenti appartiene alla classe 0
        if y > 0.5:
            print("La tupla appartiene alla classe con probabilita': ",format(y*100,'.2f'),"%")
        else:
            print("La tupla NON appartiene alla classe con probabilita': ",format((1-y)*100,'.2f'),"%")
        #return y
    # else:
    #     return y

def Cost(X, y, theta):
    m = len(y)
    h = predict(X, theta)
    diff = h - y
    J = (np.sum(diff ** 2)) / (2 * m)
    return J

def CostLog(h, y):
    m = len(y)
    J = (sum((-y * np.log(h)) - ((1 - y) * np.log(1 - h)))) / m

    return J

def normalEquations(X, y):
    a = np.dot(X.T, X)
    b = np.dot(X.T, y.T)
    theta = np.dot((np.linalg.inv(a)), b)
    return theta

def gradientDescent(X, y, theta, alpha, num_iters):
    m = len(y)
    history = []

    for i in range(0, num_iters):
        h = predict(X, theta)
        diff = h - y
        theta = theta - ((alpha/m) * np.dot(X.T, diff))
        history.append(Cost(X, y, theta))

    return (theta, history)


def gradientDescent_logistic(X, y, theta, alpha, num_iters):
    m = len(y)
    history = []

    for i in range(0, num_iters):
        z = predict(X, theta)
        h = 1 / (1 + np.exp(-z))
        diff = h - y
        theta = theta - ((alpha/m) * np.dot(X.T, diff))
        history.append(CostLog(h, y))

    return (theta, history)

def gradientDescent_logistic_multival(X, y, theta, alpha, num_iters):
    history = []
    for i in range(0, y.shape[1]):
        theta[:, i],  history2 = gradientDescent_logistic(X, y[:, i], theta[:, i], alpha, num_iters)
        history.append([history2])
    return (theta, history)


def stochastic_grad_des(X, y, theta, alpha, num_iters):
    print("inizio stochastic")
    history = []
    J = []
    for a in range(0, num_iters):
        # Derivo per il numero di samples
        for i in range(0, X.shape[0]):
            # Derivo per il numero di features
            for j in range(0, X.shape[1]):
                # Calcolo l'ipotesi
                e = predict(X[i], theta)
                e = e - y[i]
                # Calcolo la derivata (non sono sicuro che sia x[i][j]
                deriv = e * X[i][j]
                # Salvo temporaneamente theta qui, perchè l'update va fatto dopo aver calcolato tutti i theta
                theta[j] = (theta[j] - (alpha * deriv) / X.shape[1])
            history.append(Cost(X, y, theta))
    return (theta, history)

def mini_batch(X, y, theta, alpha, num_iters, b):
    print("Inizio minibatch")
    m = len(y)
    history = []
    z = 0
    for i in range(0, num_iters):
    #Iteriamo fino a qunado non consideriamo tutti i samples
        j=0
        while j < m:
            k = j + b
            theta, history2 = gradientDescent(X[j:k], y[j:k], theta, alpha, 1)
            history.append(history2)
            j += b
            z += 1
    return (theta, history)

def plotLearning(history):
    fig = plt.figure()
    ax = plt.subplot(111)
    plt.plot(np.arange(len(history)), history, '-b')
    plt.xlabel('iteration')
    plt.ylabel('J')
    plt.show(block = False)
    plt.subplot(ax)
    plt.pause(2)
    plt.close()

    return fig

def plotLearningK(history):
    fig = plt.figure()
    ax = plt.subplot(111)
    plt.plot(np.arange(1,(len(history)+1)), history, '-b')
    plt.xlabel('k')
    plt.ylabel('J')
    plt.show(block = False)
    plt.subplot(ax)
    plt.pause(2)
    plt.close()

    return fig

