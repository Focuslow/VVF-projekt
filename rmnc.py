import numpy as np
from harold import *

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
    th_pamet2 = th_pamet
    th_pamet3 = th_pamet
    lamb = 0.95
    pametlambda = []
    pametlambda = np.array(pametlambda)
    u = [0, 0, 0, 0]
    u = np.array(u)
    y = [0, 0, 0, 0]
    y = np.array(y)
    for i in range(1, len(data)):
        #u = [u: data[i]]
        #y = [y: yout[i]]
        th, P = rekmnc(u, y, P, th, 0.98)
        th_pamet = [th_pamet, th]
        th2, P2 = rekmnc(u, y, P2, th2, 0.96)
        th_pamet2 = [th_pamet2, th2]
        if math.abs(u[len(u)-1]-u[len(u)-2])>0.2:
            lamb = 0.95
        lamb = 0.99*lamb + (1-0.99)
        pametlambda = [pametlambda, lamb]
        th3, P3 = rekmnc(u, y, P3, th3, lamb)
        th_pamet3 = [th_pamet3, th3]    
    return aproxData

def rekmnc(u, y, p0, th0, lamb):
    fi = [y(len(y)-2), y(len(y)-3), y(len(y)-4), u(len(u)-2), u(len(u)-3), u(len(u)-4)]
    fi = np.array(fi)
    epsilon = y(len(y)-1)-fi*th0
    epsilon = y(len(yout)-1)-fi*th0
    K = p0*fi/(lamb+fi*p0*fi)
    K = p0*fi/(layouti*p0*fi)
    P = 1/lamb*(p0-K*fi*p0)
    P = 1/lamb*(pyoutfi*p0)
    th = th0+K*epsilon
    return th, P