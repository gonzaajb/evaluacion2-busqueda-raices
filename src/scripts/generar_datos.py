import csv
import numpy as np
from funciones import FUNCIONES
from metodos import TOL, MAX_ITER
from utils import DATA, METODOS, ejecutar, correr_todo

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

por_id = {fd["id"]: fd for fd in FUNCIONES}
pruebas= []
for a, b in [(1, 2), (0, 3), (-10, 10), (-1000, 1000)]:
    for m in ["biseccion", "falsa_posicion"]:
        pruebas.append(("polinomica_simple", m, "[%s, %s]" % (a, b), dict(a=a, b=b)))
for x0 in [1.5, 0.58, 0.5, -1, 5, 50]:
    pruebas.append(("polinomica_simple", "newton", "x0=%s" % x0, dict(x0=x0)))
for x0 in [0.5, 1, 3, 4.7, 10]:
    pruebas.append(("trigonometrica", "newton", "x0=%s" % x0, dict(x0=x0)))
for x0 in [0.01, 2.5, 20]:
    pruebas.append(("logaritmica", "newton", "x0=%s" % x0, dict(x0=x0)))
for x0 in [0.1, 0.5, 1, 3]:
    pruebas.append(("mixta", "punto_fijo", "x0=%s" % x0, dict(x0=x0)))
for s0, s1 in [(0, 1), (0.5, 0.6), (5, 6), (10, 11)]:
    pruebas.append(("exponencial", "secante", "x0=%s x1=%s" % (s0, s1), dict(s0=s0, s1=s1)))

filas= []
for id_f, m, param, kw in pruebas:
    fd = por_id[id_f]
    hist, estado = ejecutar(fd, m, **kw)
    if len(hist) > 0:
        filas.append([id_f, m, param, estado, len(hist), hist[-1][1], abs(hist[-1][1] - fd["raiz"])])
    else:
        filas.append([id_f, m, param, estado, 0, np.nan, np.nan])

guardar("sensibilidad.csv",
        ["funcion", "metodo", "parametros", "estado", "iteraciones", "raiz", "error_real"], filas)

print("CSV generados exitosamente en src/data")
