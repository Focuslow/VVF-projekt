import numpy as np
from harold import *
import math

def rmnc(yout, t, data):
    P = 1e6*np.eye(6)
    P2 = P
    P3 = P
    th = [1, 0, 0, 0, 0, 0]
    th = np.array(th)
    th2 = th
    th3 = th
    th_pamet = []
    th_pamet = np.array(th_pamet)
    th_pamet.resize((th.size,1),refcheck=False)
    th_pamet2 = th_pamet
    th_pamet3 = th_pamet
    lamb = 0.95
    time_step = t[1]-t[0]
    pametlambda = []
    pametlambda = np.array(pametlambda)
    u = [0, 0, 0, 0]
    u = np.array(u)
    y = [0, 0, 0, 0]
    y = np.array(y)
    for i in range(1, len(data)):
        u = np.append(u, data[i])
        y = np.append(y, yout[i])
        th, P = rekmnc(u, y, P, th, 0.98)
        th_pamet = np.concatenate((th_pamet, th),axis=1)
        th2, P2 = rekmnc(u, y, P2, th2, 0.96)
        th_pamet2 = np.concatenate((th_pamet2, th2),axis=1)
        if math.fabs(u[len(u)-1]-u[len(u)-2])>0.2:
            lamb = 0.95
        lamb = 0.99*lamb + (1-0.99)
        pametlambda = np.append(pametlambda, lamb)
        th3, P3 = rekmnc(u, y, P3, th3, lamb)
        th_pamet3 = np.concatenate((th_pamet3, th3),axis=1)

    na=3 #idk why
    Gz_ident3 = Transfer(np.transpose(th3[na + 1:len(th3)]),1 -np.transpose(th3[1:na]), time_step)
    Gs_ident = undiscretize(Gz_ident3)

    y = simulate_linear_system(Gs_ident, u[0:len(u)-3], t)[0]
    y.resize((len(y)), refcheck=False)
    return y

    #th_mem = [th_pamet,th_pamet2,th_pamet3]
    #th=[th,th2,th3]


def rekmnc(u, y, p0, th0, lamb):
    fi = [y[len(y)-2], y[len(y)-3], y[len(y)-4], u[len(u)-2], u[len(u)-3], u[len(u)-4]]
    fi = np.array(fi)
    fi.resize((6,1),refcheck=False)
    th0= np.array(th0)
    th0.resize((fi.size, 1), refcheck=False)
    epsilon = y[len(y)-1]-np.dot(np.transpose(fi),th0)
    K = np.dot(p0,fi)/(lamb+np.dot(np.dot(np.transpose(fi),p0),fi))
    P = 1/lamb*(p0-np.dot(np.dot(K,np.transpose(fi)),p0))
    th = th0+K*epsilon
    return th, P