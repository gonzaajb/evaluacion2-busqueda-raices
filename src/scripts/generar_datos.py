import csv
import numpy as np
from funciones import FUNCIONES
from metodos import TOL, MAX_ITER
from utils import DATA, METODOS, correr_todo

def guardar(nombre, columnas, filas):
    with open(DATA / nombre, "w", newline="", encoding="utf-8") as archivo:
        w = csv.writer(archivo)
        w.writerow(columnas)
        w.writerows(filas)

def orden(errores):
    e = [x for x in errores if x > 1e-15]
    if len(e) < 3:
        return np.nan
    e1, e2, e3 = e[-3:]
    if not (e1 > e2 > e3):
        return np.nan
    with np.errstate(all="ignore"):
        return float(np.log(e3/e2) / np.log(e2/e1))

resultados = correr_todo()
ambiente= []
resumen= []
historial= []

for fd in FUNCIONES:
    f = fd["f"]
    raiz = fd["raiz"]

    xs = np.linspace(fd["rango"][0], fd["rango"][1], 400)
    with np.errstate(all="ignore"):
        ys = f(xs)
    np.savetxt(DATA / (fd["id"] + ".csv"), np.column_stack([xs, ys]),
               delimiter=",", header="x,f(x)", comments="", fmt="%.10g")

    fa = float(f(fd["a"]))
    fb = float(f(fd["b"]))
    if fa*fb < 0:
        texto = "Bolzano: f(a)*f(b) < 0 -> hay raiz en [a,b]"
    else:
        texto = "f(a)*f(b) > 0 (sin cambio de signo); f(2)=0 y f>=0: la curva toca el eje (raiz doble)"
    ambiente.append([fd["id"], fd["categoria"], fd["a"], fd["b"], fd["xn"], fd["s0"], fd["s1"],
                     fa, fb, fa*fb, TOL, MAX_ITER, texto])

    for m in METODOS:
        hist, estado = resultados[fd["id"]][m]
        errores = [abs(x - raiz) for (k, x, fx) in hist]
        for (k, x, fx), e in zip(hist, errores):
            historial.append([fd["id"], m, k, x, fx, e])
        if len(hist) > 0:
            k, x, fx = hist[-1]
            e = errores[-1]
            if m == "biseccion":
                p = np.nan
            else:
                p = orden(errores)
            resumen.append([fd["id"], m, estado, k, x, e, fx, "si" if e < TOL else "no", p])
        else:
            resumen.append([fd["id"], m, estado, 0, np.nan, np.nan, np.nan, "-", np.nan])

guardar("ambiente_controlado.csv",
        ["funcion", "categoria", "a", "b", "x0_newton_pf", "x0_secante", "x1_secante",
         "f(a)", "f(b)", "f(a)*f(b)", "tol", "max_iter", "verificacion"], ambiente)
guardar("resumen_convergencia.csv",
        ["funcion", "metodo", "estado", "iteraciones", "raiz", "error_real", "f(raiz)",
         "error_real<1e-6", "orden_estimado"], resumen)
guardar("historial_convergencia.csv",
        ["funcion", "metodo", "iteracion", "x", "f(x)", "error"], historial)

print("CSV generados exitosamente en src/data")
