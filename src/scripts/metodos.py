import numpy as np

TOL= 1e-6
MAX_ITER =100

def parar(fx, x, x_ant):
    if abs(fx) < TOL:
        return True
    if x_ant is not None and abs(x - x_ant)<TOL:
        return True
    return False

def biseccion(f, a, b):
    fa = f(a)
    fb= f(b)
    if fa*fb > 0:
        return [], "no aplica"
    hist = []
    x_ant = None
    for k in range(1,MAX_ITER+1):
        c = (a+b)/2
        fc= f(c)
        hist.append((k, c, fc))
        if parar(fc, c, x_ant):
            return hist, "convergio"
        if fa*fc < 0:
            b= c
            fb = fc
        else:
            a = c
            fa = fc
        x_ant= c
    return hist, "max_iter"

def falsa_posicion(f, a, b):
    fa= f(a)
    fb = f(b)
    if fa*fb > 0:
        return [], "no aplica"
    hist = []
    x_ant = None
    for k in range(1,MAX_ITER+1):
        c = (a*fb - b*fa)/(fb - fa)
        fc=f(c)
        hist.append((k, c, fc))
        if parar(fc, c, x_ant):
            return hist, "convergio"
        if fa*fc < 0:
            b = c
            fb= fc
        else:
            a= c
            fa= fc
        x_ant = c
    return hist, "max_iter"
