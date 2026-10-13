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

def punto_fijo(f, g, x0):
    hist = []
    x = x0
    for k in range(1,MAX_ITER+1):
        x_nuevo = g(x)
        if not np.isfinite(x_nuevo) or abs(x_nuevo) > 1e10:
            return hist, "falla"
        fx = f(x_nuevo)
        hist.append((k, x_nuevo, fx))
        if parar(fx, x_nuevo, x):
            return hist, "convergio"
        x= x_nuevo
    return hist, "max_iter"

def secante(f, x0, x1):
    hist = []
    f0 = f(x0)
    f1 = f(x1)
    for k in range(1,MAX_ITER+1):
        if f1 == f0 or not np.isfinite(f1):
            return hist, "falla"
        x2 = x1 - f1*(x1 - x0)/(f1 - f0)
        if not np.isfinite(x2):
            return hist, "falla"
        f2 = f(x2)
        hist.append((k, x2, f2))
        if parar(f2, x2, x1):
            return hist, "convergio"
        x0, f0 = x1, f1
        x1, f1 = x2, f2
    return hist, "max_iter"

def newton(f, df, x0):
    hist = []
    x = x0
    for k in range(1,MAX_ITER+1):
        d = df(x)
        if d == 0 or not np.isfinite(d):
            return hist, "falla"
        x_nuevo = x - f(x)/d
        if not np.isfinite(x_nuevo) or abs(x_nuevo) > 1e10:
            return hist, "falla"
        fx = f(x_nuevo)
        hist.append((k, x_nuevo, fx))
        if parar(fx, x_nuevo, x):
            return hist, "convergio"
        x= x_nuevo
    return hist, "max_iter"

def newton_mejorado(f, df, d2f, x0):
    hist = []
    x = x0
    for k in range(1,MAX_ITER+1):
        fx0 = f(x)
        d = df(x)
        d2 = d2f(x)
        den = d*d - fx0*d2
        if den == 0 or not np.isfinite(den):
            return hist, "falla"
        x_nuevo = x - (fx0*d)/den
        if not np.isfinite(x_nuevo) or abs(x_nuevo) > 1e10:
            return hist, "falla"
        fx = f(x_nuevo)
        hist.append((k, x_nuevo, fx))
        if parar(fx, x_nuevo, x):
            return hist, "convergio"
        x = x_nuevo
    return hist, "max_iter"
