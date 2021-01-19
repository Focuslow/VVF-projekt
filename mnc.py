import numpy as np

""" def mnc(numbPoly, yout, t, data):
    result = np.ones(10)*1e9
    for i in range(10):
        for j in range(i+1):
            fi = []
            nab = max(i, j)
            for k in range(i, 1, -1):
                fi = [fi y]

            result[i][j] = something
    tp = np.polyfit(t, yout, numbPoly)
    aproxData = np.polyval(tp, t)
    return aproxData """

    
from harold import *
import time


def mnc_calc(na, nb, t, yout, u, pri = None):

    if na < 1 or nb < 1 or np.floor(na) != na or np.floor(nb) != nb:
        sumee = 1e9
        return sumee
    try:
        FI = []
        FI = np.array(FI)
        nab = max(na, nb)
        FI.resize((len(u) - nab, na + nb), refcheck=False)
        i=0
        j=0
        for m in range(na-1, -1, -1):
            FI[:, i] = yout[m:- nab + m]
            i+=1

        for n in range(nb-1, -1, -1):
            FI[:, i+j] = u[n: - nab + n]
            j+=1
            Y = yout[nab:]

        if abs(np.linalg.det(np.transpose(FI).dot(FI))) < 1e-6:
            sumee = 1e9
            return sumee

        parametry = np.linalg.inv((np.transpose(FI).dot(FI))).dot(np.transpose(FI)).dot(Y)

        Gz_ident = Transfer(np.transpose(parametry[na:]), np.concatenate((np.array([1]), np.transpose(-parametry[0:na]))), t[1]-t[0])
        Gs_ident = undiscretize(Gz_ident)

        eee = FI.dot(parametry) - Y
        sumee = sum(np.multiply(eee, eee))
        if not pri:
            time.sleep(0.1)
            return sumee
        else:
            y = simulate_linear_system(Gs_ident, u, t)[0]
            y.resize((len(y)), refcheck=False)
            return y

    except:
        sumee = 1e9
        return sumee

def mnc(yout, t, data):
    results = 1e9 * np.ones((10, 10))
    for i in range(1, 11):
        for j in range(1, i + 1):
            results[i - 1, j - 1] = mnc_calc(i, j, t, yout, data)

    min_val = np.amin(results)
    coords_i = np.where(results == min_val)[0]
    coords_j = np.where(results[coords_i,:][0] == min_val)[0]

    time.sleep(3)
    y = mnc_calc(coords_i[0], coords_j[0], t, yout, data, True)
    return y