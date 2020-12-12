##MNC

import numpy as np
from harold import *
import time
from matplotlib import pyplot as plt


def mnc_calc(na, nb, num, den, ts, t_max, ax, u=None):

    if na < 1 or nb < 1 or np.floor(na) != na or np.floor(nb) != nb:
        sumee = 1e9
        return sumee, ax

    t = np.arange(0, t_max+ts, ts)
    Gs = Transfer(num, den)

    try:
        if not u:
            u = np.concatenate((np.array([0]), np.ones(len(t)-1)))
            pom = round(len(u) / 10)
            u[3 * pom:5 * pom] = 0
            u = u + 0.03 * np.random.rand(np.size(u)) + np.sin(2 * np.pi / 10 * t)

        y = simulate_linear_system(Gs, u, t)[0]
        y.resize((len(y)), refcheck=False)

        # ax[0].get_lines()[0].set_xdata(t)
        # ax[0].get_lines()[0].set_ydata(u)
        # ax[0].get_lines()[1].set_xdata(t)
        # ax[0].get_lines()[1].set_ydata(y)
        # plt.show()

        FI = []
        FI = np.array(FI)
        nab = max(na, nb)
        FI.resize((len(u) - nab, na + nb), refcheck=False)
        i=0
        j=0
        for m in range(na-1, -1, -1):
            FI[:, i] = y[m:- nab + m]
            i+=1

        for n in range(nb-1, -1, -1):
            FI[:, i+j] = u[n: - nab + n]
            j+=1

            Y = y[nab:]

        if abs(np.linalg.det(np.transpose(FI).dot(FI))) < 1e-6:
            sumee = 1e9
            return sumee, ax


        parametry = np.linalg.inv((np.transpose(FI).dot(FI))).dot(np.transpose(FI)).dot(Y)

        Gz_ident = Transfer(np.transpose(parametry[na:]), np.concatenate((np.array([1]), np.transpose(-parametry[0:na]))), ts)
        Gs_ident = undiscretize(Gz_ident)

        # ax[1].get_lines()[0].set_xdata(t)
        # ax[1].get_lines()[0].set_ydata(y)
        # ax[1].get_lines()[1].set_xdata(t)
        # ax[1].get_lines()[1].set_ydata(simulate_linear_system(Gs_ident, u, t)[0])
        # plt.show()

        #ax2.plot(t, y, 'b', t, simulate_linear_system(Gs_ident, u, t)[0], 'r')

        eee = FI.dot(parametry) - Y
        sumee = sum(np.multiply(eee, eee))

        time.sleep(0.1)
        return sumee, ax

    except:
        sumee = 1e9
        return sumee, ax

def mnc(sys=None,t=None, u=None):

    # line1, = ax1.plot([0], [0], 'k')
    # line2, = ax1.plot([0], [0], 'b')
    # line3, = ax2.plot([0], [0], 'b')
    # line4, = ax2.plot([0], [0], 'r')

    fig, (ax1, ax2) = plt.subplots(2, 1)
    ax = [ax1, ax2]

    results = 1e9 * np.ones((10, 10))
    if not sys:
        num = np.array([1, 2])
        den = np.array([1, 4, 3, 5, 1])
    else:
        num = np.array(sys[0])
        den = np.array(sys[1])

    if not t:
        ts = 0.1
        t_max = 50
    else:
        ts=t[0]
        t_max=t[1]

    for i in range(1, 11):
        for j in range(1, i + 1):
            results[i - 1, j - 1], ax = mnc_calc(i, j, num, den, ts, t_max, ax,u)

    min_val = np.amin(results)
    coords_i = np.where(results == min_val)[0]
    coords_j = np.where(results[coords_i,:][0] == min_val)[0]
    print('value: ' + str(min_val))
    print('a: ' + str(coords_i[0]) + '   b: ' + str(coords_j[0]))

    time.sleep(3)
    mnc_calc(coords_i[0], coords_j[0], num, den, ts, t_max, ax)
